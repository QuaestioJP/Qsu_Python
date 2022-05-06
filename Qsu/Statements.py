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



