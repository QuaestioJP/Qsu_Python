import AST
import Lexer
import JsonUtility


class Identifier(AST.IExpression):
    def __init__(self, token, value):
        self.Token = token
        self.Value = value

    def ToJSON(self):
        return JsonUtility.ToJSON("return", [
            ("Value", "\"" + self.Value + "\"")
        ])
