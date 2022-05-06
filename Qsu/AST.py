import abc


class INode(metaclass=abc.ABCMeta):
    @abs.abstractmethod
    def ToJSON(self):
        pass


class IStatement(INode, metaclass=abc.ABCMeta):
    pass


class IExpression(INode, metaclass=abc.ABCMeta):
    pass


class Root(INode, metaclass=abc.ABCMeta):
    Statements = []

    def ToJSON(self):
        s = ""
        s += "{ \"root\":["

        for a in range(len(self.Statements)):
            self.s += self.Statements[a].ToJSON()

            if a != len(self.Statements) - 1:
                self.s += ","
        self.s += "]}"

        return s
