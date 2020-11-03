"""
*What is this pattern about?
Define a family of algorithms, encapsulate each one, and make them interchangeable.
Strategy lets the algorithm vary independently from clients that use it.
定义一系列算法，封装每一个算法，并使它们可互换。
策略让算法独立于使用它的客户而变化。

*TL;DR
Enables selecting an algorithm at runtime.

订单模式：通过传入函数 ，实现不同折扣
"""


class Order:
    def __init__(self, price, discount_strategy=None):
        self.price = price
        self.discount_strategy = discount_strategy  # 折扣政策

    def price_after_discount(self):
        if self.discount_strategy:
            discount = self.discount_strategy(self)
        else:
            discount = 0
        return self.price - discount

    def __repr__(self):
        fmt = "<Price: {}, price after discount: {}>"
        return fmt.format(self.price, self.price_after_discount())


def ten_percent_discount(order):
    return order.price * 0.10


def on_sale_discount(order):
    return order.price * 0.25 + 20


def main():
    """
    >>> Order(100)
    <Price: 100, price after discount: 100>

    >>> Order(100, discount_strategy=ten_percent_discount)
    <Price: 100, price after discount: 90.0>

    >>> Order(1000, discount_strategy=on_sale_discount)
    <Price: 1000, price after discount: 730.0>
    """
    print(Order(100))
    print(Order(100, discount_strategy=ten_percent_discount))
    print(Order(1000, discount_strategy=on_sale_discount))


if __name__ == "__main__":
    # import doctest
    #
    # doctest.testmod()
    main()
