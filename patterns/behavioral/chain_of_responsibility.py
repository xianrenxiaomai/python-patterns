"""
*What is this pattern about?

The Chain of responsibility is an object oriented version of the
`if ... elif ... elif ... else ...` idiom, with the
benefit that the condition–action blocks can be dynamically rearranged
and reconfigured at runtime.

This pattern aims to decouple the senders of a request from its
receivers by allowing request to move through chained
receivers until it is handled.

Request receiver in simple form keeps a reference to a single successor.
As a variation some receivers may be capable of sending requests out
in several directions, forming a `tree of responsibility`.

if ... elif ... elif ... else ...的面向对象版本
好处是条件-动作块可以动态地重新排列 并在运行时重新配置。

此模式旨在将请求的发送方与请求的发送方解耦
通过允许接收者通过链接移动请求 直到它被处理。

简单形式的请求接收方保留对单个继承方的引用。
作为一种变体，一些接收者可能能够将请求发送出去，在几个方面，形成了“责任树”。

*TL;DR
Allow a request to pass down a chain of receivers until it is handled.

责任链模式 通过继承ABC类 遍历其子类
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple, TypeVar

T = TypeVar("T")


class Handler(ABC):
    def __init__(self, successor: Optional[T] = None):
        self.successor = successor

    def handle(self, request: int) -> None:
        """
        Handle request and stop.
        If can't - call next handler in chain.

        As an alternative you might even in case of success
        call the next handler.
        """
        res = self.check_range(request)
        if not res and self.successor:
            self.successor.handle(request)

    @abstractmethod
    def check_range(self, request: int) -> Optional[bool]:
        """Compare passed value to predefined interval"""


class ConcreteHandler0(Handler):
    """Each handler can be different.
    Be simple and static...
    """

    @staticmethod
    def check_range(request: int) -> Optional[bool]:
        if 0 <= request < 10:
            print(f"request {request} handled in handler 0")
            return True


class ConcreteHandler1(Handler):
    """... With it's own internal state"""

    start, end = 10, 20

    def check_range(self, request: int) -> Optional[bool]:
        if self.start <= request < self.end:
            print(f"request {request} handled in handler 1")
            return True


class ConcreteHandler2(Handler):
    """... With helper methods."""

    def check_range(self, request: int) -> Optional[bool]:
        start, end = self.get_interval_from_db()
        if start <= request < end:
            print(f"request {request} handled in handler 2")
            return True

    @staticmethod
    def get_interval_from_db() -> Tuple[int, int]:
        return (20, 30)


class FallbackHandler(Handler):
    @staticmethod
    def check_range(request: int) -> Optional[bool]:
        print(f"end of chain, no handler for {request}")
        return False


def main():
    """
    >>> h0 = ConcreteHandler0()
    >>> h1 = ConcreteHandler1()
    >>> h2 = ConcreteHandler2(FallbackHandler())
    >>> h0.successor = h1
    >>> h1.successor = h2

    >>> requests = [2, 5, 14, 22, 18, 3, 35, 27, 20]
    >>> for request in requests:
    ...     h0.handle(request)
    request 2 handled in handler 0
    request 5 handled in handler 0
    request 14 handled in handler 1
    request 22 handled in handler 2
    request 18 handled in handler 1
    request 3 handled in handler 0
    end of chain, no handler for 35
    request 27 handled in handler 2
    request 20 handled in handler 2
    """


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
