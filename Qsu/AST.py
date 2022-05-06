import abc


class INode(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def ToJSON(self):
        pass


class IStatement(INode, metaclass=abc.ABCMeta):
    pass


class IExpression(INode, metaclass=abc.ABCMeta):
    pass


class Root(INode, metaclass=abc.ABCMeta):
    def __init__(self):
        self.Statements = []

    def ToJSON(self):
        s = ""
        s += "{ \"root\":["

        print(len(self.Statements))
        for a in range(len(self.Statements)):
            s += self.Statements[a].ToJSON()

            if a != len(self.Statements) - 1:
                s += ","
        s += "]}"

        return s
