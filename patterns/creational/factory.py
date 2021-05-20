"""*What is this pattern about?
A Factory is an object for creating other objects.
工厂是用于创建其他对象的对象。

*What does this example do?
The code shows a way to localize words in two languages: English and
Greek. "get_localizer" is the factory function that constructs a
localizer depending on the language chosen. The localizer object will
be an instance from a different class according to the language
localized. However, the main code does not have to worry about which
localizer will be instantiated, since the method "localize" will be called
in the same way independently of the language.
代码显示了一种将单词本地化为两种语言的方法:英语和希腊语。
“get_localizer”是工厂函数，它构造本地化程序取决于所选择的语言。
localizer对象会根据语言，成为来自不同类的实例本地化。
不过，主代码不用担心哪一个localizer将被实例化，因为方法“localize”将被调用以同样的方式独立于语言之外。

*Where can the pattern be used practically?
The Factory Method can be seen in the popular web framework Django:
http://django.wikispaces.asu.edu/*NEW*+Django+Design+Patterns For
example, in a contact form of a web page, the subject and the message
fields are created using the same form factory (CharField()), even
though they have different implementations according to their
purposes.
工厂方法可以在流行的web框架Django中看到:
Django http://django.wikispaces.asu.edu/ *新* + +设计+模式
例如，在web页面的联系形式中，主题和消息
字段是使用相同的表单工厂(CharField())创建的
尽管它们有不同的实现目的。

*References:
http://ginstrom.com/scribbles/2007/10/08/design-patterns-python-style/

*TL;DR
Creates objects without having to specify the exact class.
工厂模式 调用者只需调用对应的函数，无需关心内部实现
"""


class GreekLocalizer:
    """A simple localizer a la gettext"""

    def __init__(self) -> None:
        self.translations = {"dog": "σκύλος", "cat": "γάτα"}

    def localize(self, msg: str) -> str:
        """We'll punt if we don't have a translation"""
        return self.translations.get(msg, msg)


class EnglishLocalizer:
    """Simply echoes the message"""

    def localize(self, msg: str) -> str:
        return msg


def get_localizer(language: str = "English") -> object:
    """Factory"""
    localizers = {
        "English": EnglishLocalizer,
        "Greek": GreekLocalizer,
    }

    return localizers[language]()


def main():
    """
    # Create our localizers
    >>> e, g = get_localizer(language="English"), get_localizer(language="Greek")

    # Localize some text
    >>> for msg in "dog parrot cat bear".split():
    ...     print(e.localize(msg), g.localize(msg))
    dog σκύλος
    parrot parrot
    cat γάτα
    bear bear
    """
    e, g = get_localizer(language="English"), get_localizer(language="Greek")
    for msg in "dog parrot cat bear".split():
        print(e.localize(msg), g.localize(msg))


if __name__ == "__main__":
    main()
