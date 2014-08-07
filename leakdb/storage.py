# -*- coding: utf-8 -*-

from datetime import datetime
from os import path
from shelve import open as s_open

from leakdb import logger
from leakdb.queue import LeakQueue


class DefaultStorage(dict):

    def __repr__(self):
        return u'{} items in storage memory'.format(len(self))

    def set(self, key, value, key_prefix=None):
        """
        :params key: Key to set.
        :params value: Value to set. The value type can be any value supported by the Python pickle module.
        :params str key_prefix: Prefix to prepend to all keys (default=None).

        :returns: True if insertion succeeds.
        """
        try:
            _key = "{}{}".format(key_prefix, key) if key_prefix else key
            super(DefaultStorage, self).__setitem__(_key, value)
            self.hook(operation="set", item={_key: value})
        except Exception as e:
            logger.critical('unable to set a key :: {}'.format(e))
            return False
        else:
            return True

    def set_multi(self, mapping, key_prefix=None):
        """
        :params dict mapping: Dict of keys to values.
        :params str key_prefix: Prefix to prepend to all keys (default=None).

        :returns: True if all insertion succeeds, false otherwise.
        """
        return all([self.set(k, v, key_prefix) for k, v in mapping.items()])

    def incr(self, key, delta=1, initial_value=None):
        """
        :params key: Key to increment.
        :params int delta: Non-negative integer value to increment key by (default=1).
        :params int initial_value: An initial value to be used if the key does not yet exist in the cache.

        :returns: True if increment succeeds.

        :raises ValueError: increment a non-numeric value.
        """
        try:
            if delta < 0:
                raise ValueError(delta)

            value = self.get(key)
            if not value:
                value = initial_value or delta
            else:
                value += delta
        except ValueError as e:
            raise ValueError('{} cannot increment non-numeric value'.format(e))
        else:
            self.set(key, value)
            return True

    def decr(self, key, delta=1):
        """
        :params key: Key to decrement.
        :params int delta: Non-negative integer value to decrement key by (default=1).

        :returns: True if decrement succeeds.

        :raises ValueError: decrement a non-numeric value.
        """
        # TODO: DRY with the incr method.
        try:
            if delta < 0:
                raise ValueError(delta)

            value = self.get(key)
            if not value:
                return False
            else:
                value -= delta
        except ValueError as e:
            raise ValueError('{} cannot decrement non-numeric value'.format(e))
        else:
            self.set(key, value)
            return True

    def get_multi(self, keys):
        """ Looks up multiple keys from dict in one operation.

        :params list keys: List of keys to look up.

        :returns: Dictionary of the keys and values that were present.
        """
        try:
            return {key: self[key] for key in keys if key in self}
        except Exception as e:
            logger.critical('unable to looks up multiple keys :: {}'.format(e))
            return {}

    def delete(self, key):
        """ Delete a key.

        :params key: Key to delete.

        :returns: The value of the delete key, otherwise False.
        """
        delete = self.pop(key, False)
        if delete:
            self.hook(operation="delete", item=key)

        return delete

    def close(self):
        pass

    def hook(self, operation, item):
        pass


class QueueStorage(LeakQueue, DefaultStorage):

    def __init__(self, *args, **kwargs):
        #: init the gevent queue
        super(QueueStorage, self).__init__(*args, **kwargs)

    def close(self):
        super(QueueStorage, self).close()
        self.flush()

    def hook(self, operation, item):
        self.put(operation=operation, item=item, date=datetime.utcnow())

    def __repr__(self):
        return " :: ".join([x.__repr__(self) for x in QueueStorage.__bases__])


class PersistentStorage(DefaultStorage):

    def __init__(self, filename, writeback=False, *args, **kwargs):
        """

        :params str filename: The filename specified is the base filename for the underlying database.
        :params boolean writeback: All entries accessed are also cached in memory.
        """
        super(PersistentStorage, self).__init__(*args, **kwargs)

        self.filename = filename
        self.shelve_dict = s_open(self.filename, writeback=writeback)
        self.update(self.shelve_dict)

    def close(self):
        super(PersistentStorage, self).close()

        self.shelve_dict.sync()
        self.shelve_dict.close()

    def hook(self, operation, item):
        if operation == "set":
            self.shelve_dict.update(item)
        elif operation == "delete":
            self.shelve_dict.pop(item)

    def __repr__(self):
        size = path.getsize(self.filename)
        return u"{} {} bytes :: {}".format(self.filename, size, super(PersistentStorage, self).__repr__())


class PersistentQueueStorage(PersistentStorage, QueueStorage):

    def __init__(self, *args, **kwargs):
        #: init the gevent queue and the shelve dict
        super(PersistentQueueStorage, self).__init__(writeback=True, *args, **kwargs)

    def close(self):
        #: flush the gevent queue and close the shelve dict
        super(PersistentQueueStorage, self).close()

    def hook(self, operation, item):
        QueueStorage.hook(self, operation, item)

    def worker_process(self, item):
        logger.info('process item :: {}'.format(item))

        item.pop('date', None)
        PersistentStorage.hook(self, **item)

        return True
