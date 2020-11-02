"""
Reference:
http://www.slideshare.net/ishraqabd/publish-subscribe-model-overview-13368808
Author: https://github.com/HanWenfang

发布订阅模式 构造如下数据结构 通过双层for循环发送消息
"""


class Provider:
    def __init__(self):
        self.msg_queue = []  # 消息队列
        self.subscribers = {}
        """
        {
            'cartoon': [<__main__.Subscriber object at 0x10bc63e90>],
             'music': [<__main__.Subscriber object at 0x10a004890>],
             'movie': [<__main__.Subscriber object at 0x10bc63ad0>, <__main__.Subscriber object at 0x10be84810>]
        }
        """

    def notify(self, msg):
        self.msg_queue.append(msg)

    def subscribe(self, msg, subscriber):
        self.subscribers.setdefault(msg, []).append(subscriber)

    def unsubscribe(self, msg, subscriber):
        self.subscribers[msg].remove(subscriber)

    def update(self):
        # 两层for循环 模拟消息队列（msg_queue）中每个信息发送到订阅人那里，并清空消息队列
        for msg in self.msg_queue:
            for sub in self.subscribers.get(msg, []):  # 订阅人
                sub.run(msg)
        self.msg_queue = []


class Publisher:
    def __init__(self, msg_center):
        self.provider = msg_center

    def publish(self, msg):
        self.provider.notify(msg)


class Subscriber:
    def __init__(self, name, msg_center):
        self.name = name
        self.provider = msg_center

    def subscribe(self, msg):
        self.provider.subscribe(msg, self)

    def unsubscribe(self, msg):
        self.provider.unsubscribe(msg, self)

    def run(self, msg):
        print("{} got {}".format(self.name, msg))


def main():
    """
    >>> message_center = Provider()

    >>> fftv = Publisher(message_center)

    >>> jim = Subscriber("jim", message_center)
    >>> jim.subscribe("cartoon")
    >>> jack = Subscriber("jack", message_center)
    >>> jack.subscribe("music")
    >>> gee = Subscriber("gee", message_center)
    >>> gee.subscribe("movie")
    >>> vani = Subscriber("vani", message_center)
    >>> vani.subscribe("movie")
    >>> vani.unsubscribe("movie")

    # Note that no one subscirbed to `ads`
    # and that vani changed their mind

    >>> fftv.publish("cartoon")
    >>> fftv.publish("music")
    >>> fftv.publish("ads")
    >>> fftv.publish("movie")
    >>> fftv.publish("cartoon")
    >>> fftv.publish("cartoon")
    >>> fftv.publish("movie")
    >>> fftv.publish("blank")

    >>> message_center.update()
    jim got cartoon
    jack got music
    gee got movie
    jim got cartoon
    jim got cartoon
    gee got movie
    """

    message_center = Provider()

    fftv = Publisher(message_center)

    jim = Subscriber("jim", message_center)
    jim.subscribe("cartoon")
    jack = Subscriber("jack", message_center)
    jack.subscribe("music")
    gee = Subscriber("gee", message_center)
    gee.subscribe("movie")
    vani = Subscriber("vani", message_center)
    vani.subscribe("movie")
    vani.unsubscribe("movie")

    # Note that no one subscirbed to `ads`
    # and that vani changed their mind

    fftv.publish("cartoon")
    fftv.publish("music")
    fftv.publish("ads")
    fftv.publish("movie")
    fftv.publish("cartoon")
    fftv.publish("cartoon")
    fftv.publish("movie")
    fftv.publish("blank")

    message_center.update()


if __name__ == "__main__":
    # import doctest
    #
    # doctest.testmod()
    main()
