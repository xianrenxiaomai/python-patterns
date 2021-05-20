"""
注册模式

BaseRegisteredClass（metaclass=RegistryHolder），继承父类RegistryHolder(继承type， 并改写__new__)
通过继承BaseRegisteredClass实现注册

# 研究源码 探究python在继承的时候发生了什么
"""


class RegistryHolder(type):
    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        """
            Here the name of the class is used as key but it could be any class
            parameter.
        """
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)


class BaseRegisteredClass(metaclass=RegistryHolder):
    """
    Any class that will inherits from BaseRegisteredClass will be included
    inside the dict RegistryHolder.REGISTRY, the key being the name of the
    class and the associated value, the class itself.
    """


def main():
    """
    Before subclassing
    >>> sorted(RegistryHolder.REGISTRY)
    ['BaseRegisteredClass']

    >>> class ClassRegistree(BaseRegisteredClass):
    ...    def __init__(self, *args, **kwargs):
    ...        pass

    After subclassing
    >>> sorted(RegistryHolder.REGISTRY)
    ['BaseRegisteredClass', 'ClassRegistree']
    """


if __name__ == "__main__":
    # import doctest
    #
    # doctest.testmod(optionflags=doctest.ELLIPSIS)
    print(sorted(RegistryHolder.REGISTRY))

    class ClassRegistree(BaseRegisteredClass): # 只要

        def __init__(self, *args, **kwargs):
            pass


    print(sorted(RegistryHolder.REGISTRY))
