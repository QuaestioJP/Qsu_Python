import Lexer
import AST


class Parser:
    CurrentToken = Lexer.Token(Lexer.TokenType.ILLEGAL, "")
    NextToken = Lexer.Token(Lexer.TokenType.ILLEGAL,"")
    lexer = Lexer.Lexer

    def __init__(self,_lexer):
        self.lexer = _lexer

        self.CurrentToken = self.lexer.NextToken()
        self.NextToken = self.NextToken()

