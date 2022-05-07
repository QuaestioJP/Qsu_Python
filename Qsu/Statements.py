import AST
import Lexer
import Expressions
import JsonUtility


class LetStatement(AST.IStatement):
    def __init__(self):
        self.Token: Lexer.Token = None
        self.Name: Expressions.Identifier = None
        self.Value: AST.IExpression = None

    def ToJSON(self):
        return JsonUtility.ToJSON("let", [
            ("Name", self.Name.ToJSON()),
            ("Value", self.Value.ToJSON())
        ])


class ReturnStatement(AST.IStatement):
    def __init__(self):
        self.Token: Lexer.Token = None
        self.Value: AST.IExpression = None

    def ToJSON(self):
        return JsonUtility.ToJSON("Return", [
            ("Value", self.Value.ToJSON())
        ])


class BlockStatement(AST.IStatement):
    def __init__(self):
        self.Token: Lexer.Token = None
        self.Statements: list = None

    def ToJSON(self):
        param = []
        for a in self.Statements:
            param.append(a.ToJSON())

        return JsonUtility.ToJSON("Block", [
            ("statements", "[" + ",".join(param) + "]")
        ])


class IfStatement(AST.IStatement):
    def __init__(self):
        self.Token: Lexer.Token = None
        self.Condition: AST.IExpression = None
        self.Consequence: BlockStatement = None
        self.Alternative: BlockStatement = None

    def ToJSON(self):
        if self.Alternative is None:
            return JsonUtility.ToJSON("if", [
                ("Consequence", self.Consequence.ToJSON())
            ])
        else:
            return JsonUtility.ToJSON("if-else", [
                ("Consequence", self.Consequence.ToJSON()),
                ("Alternative", self.Alternative.ToJSON())
            ])
