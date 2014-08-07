# -*- coding: utf-8 -*-

from unittest import TestCase


class TestDefaultStorage(TestCase):

    def test_set_multiple_value(self):
        """ Set key with multiple type value.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()

        self.assertTrue(leak.set(key="foobar", value="foo"))
        self.assertTrue(leak.set(key="foobar", value=1))
        self.assertTrue(leak.set(key="foobar", value=["foo", "bar"]))
        self.assertTrue(leak.set(key="foobar", value=("foo",)))
        self.assertTrue(leak.set(key="foobar", value={"foo": "bar"}))

    def test_set_multiple_key(self):
        """ Set key with multiple type key.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()

        self.assertTrue(leak.set(key="foobar", value="foo"))
        self.assertTrue(leak.set(key=1, value="foo"))

        self.assertFalse(leak.set(key={}, value="foo"))

    def test_set_multi_key(self):
        """ set_multi with multiple type key.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()

        keys = {
            "foobar": "foo",
            "foobar": 1,
            "foobar": {"foo": "bar"}
        }
        self.assertTrue(leak.set_multi(mapping=keys))

    def test_set_prefix(self):
        """ Set key with a prefix.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()

        self.assertTrue(leak.set(key="foo", value="bar", key_prefix="coconut_"))
        self.assertTrue(leak.set(key="foo", value="bar", key_prefix=1))
        self.assertTrue(leak.set(key="foo", value="bar", key_prefix={}))

    def test_increment(self):
        """ Simple increment.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()
        leak.set(key="foo", value=1)

        leak.incr(key="foo")
        self.assertEqual(leak.get("foo"), 2)

        leak.incr(key="foo", delta=2)
        self.assertEqual(leak.get("foo"), 4)

    def test_increment_empty(self):
        """ Increment empty key.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()

        leak.incr(key="foo")
        leak.incr(key="bar", delta=2)

        self.assertEqual(leak.get("foo"), 1)
        self.assertEqual(leak.get("bar"), 2)

    def test_increment_initial(self):
        """ Increment key with initial value.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()

        leak.incr(key="foo", initial_value=666)
        self.assertEqual(leak.get("foo"), 666)

        leak.incr(key="foo", initial_value=666)
        self.assertEqual(leak.get("foo"), 667)

        leak.incr(key="foo", delta=2, initial_value=666)
        self.assertEqual(leak.get("foo"), 669)

    def test_invalid_increment(self):
        """ Increment with a wrong value.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()
        with self.assertRaises(ValueError) as e:
            leak.incr(key="foo", delta=-1)

        self.assertSequenceEqual(
            "-1 cannot increment non-numeric value", e.exception.message)

    def test_decrement(self):
        """ Simple decrement.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()
        leak.set(key="foo", value=1)
        leak.set(key="bar", value=10)

        leak.decr(key="foo")
        self.assertEqual(leak.get("foo"), 0)

        leak.decr(key="bar", delta=5)
        self.assertEqual(leak.get("bar"), 5)

        leak.decr(key="bar", delta=10)
        self.assertEqual(leak.get("bar"), -5)

    def test_invalid_decrement(self):
        """ Decrement with a wrong value.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()
        with self.assertRaises(ValueError) as e:
            leak.decr(key="foo", delta=-1)

        self.assertSequenceEqual(
            "-1 cannot decrement non-numeric value", e.exception.message)

    def test_get_multi(self):
        """ Looks up multiple keys.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()
        leak.set(key="foo", value=1)
        leak.set(key="bar", value=1)

        expected_result = {"foo": 1, "bar": 1}
        self.assertSequenceEqual(leak.get_multi(keys=["foo", "bar", "unknown"]), expected_result)
        self.assertSequenceEqual(leak.get_multi(keys=("foo", "bar", "unknown",)), expected_result)
        self.assertSequenceEqual(leak.get_multi(keys={"foo": 1, "bar": 1, "unknown": 1}), expected_result)

    def test_get_multi_bad_keys(self):
        """ Looks up multiple keys with bad argument.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()
        leak.set(key="foo", value=1)
        leak.set(key="bar", value=1)

        self.assertFalse(leak.get_multi(keys="foo, bar"))
        self.assertFalse(leak.get_multi(keys=None))

    def test_delete(self):
        """ Simple delete.
        """
        from leakdb.storage import DefaultStorage

        leak = DefaultStorage()
        leak.set(key="foo", value=1)

        self.assertEqual(leak.delete(key="foo"), 1)
        self.assertFalse(leak.get("foo"))

        self.assertFalse(leak.delete(key="foo"))
