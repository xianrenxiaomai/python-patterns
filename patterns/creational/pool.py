"""
*What is this pattern about?
This pattern is used when creating an object is costly (and they are
created frequently) but only a few are used at a time. With a Pool we
can manage those instances we have as of now by caching them. Now it
is possible to skip the costly creation of an object if one is
available in the pool.
A pool allows to 'check out' an inactive object and then to return it.
If none are available the pool creates one to provide without wait.
此模式用于创建开销很大的对象(确实经常创建)，但只有少数使用一次。我们有一个对象池，可以通过缓存来管理我们目前拥有的实例。
现在，如果池中有可用的对象，则可以跳过代价高昂的对象创建。。

对象池允许‘签出’一个不活动的对象，然后返回它。
如果没有可用的，池将创建一个来提供，而不需要等待。

*What does this example do?
In this example queue.Queue is used to create the pool (wrapped in a
custom ObjectPool object to use with the with statement), and it is
populated with strings.
As we can see, the first string object put in "yam" is USED by the
with statement. But because it is released back into the pool
afterwards it is reused by the explicit call to sample_queue.get().
Same thing happens with "sam", when the ObjectPool created inside the
function is deleted (by the GC) and the object is returned.

我们可以看到，with语句使用了放入“yam”中的第一个字符串对象。
但是因为它在之后被释放回池中，所以它在显式调用sample_queue.get()时被重用。
当删除(由GC)函数中创建的ObjectPool并返回对象时，“sam”也会发生同样的事情

*Where is the pattern used practically?

*References:
http://stackoverflow.com/questions/1514120/python-implementation-of-the-object-pool-design-pattern
https://sourcemaking.com/design_patterns/object_pool

*TL;DR
Stores a set of initialized objects kept ready to use.
存储一组随时准备使用的初始化对象
"""


class ObjectPool:
    def __init__(self, queue, auto_get=False):
        self._queue = queue
        self.item = self._queue.get() if auto_get else None

    def __enter__(self):
        if self.item is None:
            self.item = self._queue.get()
        return self.item

    def __exit__(self, Type, value, traceback):
        if self.item is not None:
            self._queue.put(self.item)
            self.item = None

    def __del__(self):
        if self.item is not None:
            self._queue.put(self.item)
            self.item = None


def main():
    """
    >>> import queue

    >>> def test_object(queue):
    ...    pool = ObjectPool(queue, True)
    ...    print('Inside func: {}'.format(pool.item))

    >>> sample_queue = queue.Queue()

    >>> sample_queue.put('yam')
    >>> with ObjectPool(sample_queue) as obj:
    ...    print('Inside with: {}'.format(obj))
    Inside with: yam

    >>> print('Outside with: {}'.format(sample_queue.get()))
    Outside with: yam

    >>> sample_queue.put('sam')
    >>> test_object(sample_queue)
    Inside func: sam

    >>> print('Outside func: {}'.format(sample_queue.get()))
    Outside func: sam

    if not sample_queue.empty():
        print(sample_queue.get())
    """

    import queue

    def test_object(queue):
        pool = ObjectPool(queue, True)
        print('Inside func: {}'.format(pool.item))

    sample_queue = queue.Queue()

    sample_queue.put('yam')
    with ObjectPool(sample_queue) as obj:
        print('Inside with: {}'.format(obj))

    print('Outside with: {}'.format(sample_queue.get()))

    sample_queue.put('sam')
    test_object(sample_queue)

    print('Outside func: {}'.format(sample_queue.get()))


if __name__ == "__main__":
    # import doctest
    #
    # doctest.testmod()
    main()
