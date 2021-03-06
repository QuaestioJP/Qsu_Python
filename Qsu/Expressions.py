import AST
import Lexer
import JsonUtility


class Identifier(AST.IExpression):
    def __init__(self, token, value):
        self.Token = token
        self.Value = value

    def ToJSON(self):
        return JsonUtility.ToJSON("Ident", [
            ("Value", "\"" + self.Value + "\"")
        ])


class PrefixExpression(AST.IExpression):
    def __init__(self):
        self.Token: Lexer.Token = None
        self.Operator: str = None
        self.Right: AST.IExpression = None

    def ToJSON(self):
        return JsonUtility.ToJSON("Prefix", [
            ("Operator", "\"" + self.Operator + "\""),
            ("Right", self.Right.ToJSON())
        ])


class IntegerLiteral(AST.IExpression):
    def __init__(self):
        self.Token: Lexer.Token = None
        self.Value: int = None

    def ToJSON(self):
        return JsonUtility.ToJSON("Integer", [
            ("Value", "\"" + str(self.Value) + "\"")
        ])


class BooleanLiteral(AST.IExpression):
    def __init__(self):
        self.Token: Lexer.Token = None
        self.Value: bool = None

    def ToJSON(self):
        return JsonUtility.ToJSON("Boolean",[
            ("Value", "\"" + str(self.Value) + "\"")
        ])


class InfixExpression(AST.IExpression):
    def __init__(self):
        self.Token: Lexer.Token = None
        self.Left: AST.IExpression = None
        self.Operator: str = None
        self.Right: AST.IExpression = None

    def ToJSON(self):
        return JsonUtility.ToJSON("Infix",[
            ("Operator","\"" + self.Operator + "\""),
            ("Left", self.Left.ToJSON()),
            ("Right", self.Right.ToJSON())
        ])
