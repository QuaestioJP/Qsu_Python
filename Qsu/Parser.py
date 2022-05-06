import Lexer
import AST
import Statements
import Expressions
from enum import Enum


class Parser:
    def __init__(self, _lexer):
        self.lexer = _lexer

        self.CurrentToken = self.lexer.NextToken()
        self.NextToken = self.lexer.NextToken()
        self.Errors = []

        self.PrefixParseFns = {}

        self.RegisterPrefixParseFns()

    # region 前置演算子
    def RegisterPrefixParseFns(self):
        self.PrefixParseFns = {}
        self.PrefixParseFns[Lexer.TokenType.IDENT] = self.ParseIdentifier
        self.PrefixParseFns[Lexer.TokenType.INT] = self.ParseIntegerLiteral

    # endregion

    # region エクスプレッション
    def ParseExpression(self,precedence):
        fn = self.PrefixParseFns.get(self.CurrentToken.Type)
        if fn is None:
            self.AddPrefixParseFnError(self.CurrentToken.Type)
            return None

        leftExpression = fn()
        return leftExpression

        # todo infixがまだできてない

    def ParseIdentifier(self):
        return Expressions.Identifier(self.CurrentToken, self.CurrentToken.Literal)

    def ParseIntegerLiteral(self):
        if self.CurrentToken.Literal.isdecimal():
            Token = self.CurrentToken
            Value = int(self.CurrentToken.Literal)
            integerliteral = Expressions.IntegerLiteral()

            integerliteral.Token = Token
            integerliteral.Value = Value

            return integerliteral

        self.Errors.append(self.CurrentToken.Literal + "をintに変換できません。")
        return None

    # endregion

    # region ユーティリティ
    def ReadToken(self):
        self.CurrentToken = self.NextToken
        self.NextToken = self.lexer.NextToken()

    def ParseRoot(self):
        root = AST.Root()
        root.Statements = []
        while self.CurrentToken.Type != Lexer.TokenType.EOF:
            statement = self.ParseStatement()
            if statement is not None:
                root.Statements.append(statement)

            self.ReadToken()
        return root

    def ExpectPeek(self, _type):
        if self.NextToken.Type == _type:
            self.ReadToken()
            return True

        self.AddNextTokenError(_type, self.NextToken.Type)
        return False

    def AddNextTokenError(self, expected, actual):
        self.Errors.append(str(actual) + "ではなく" + str(expected) + "が来なければなりません")

    def AddPrefixParseFnError(self,Tokentype):
        self.Errors.append(Tokentype + "に関連付けられたprefixparsefunctionはありません")

    # endregion

    # region ステートメント
    def ParseStatement(self):
        match self.CurrentToken.Type:
            case Lexer.TokenType.LET:
                return self.ParseLetStatement()
            case _:
                return None

    def ParseLetStatement(self):
        statement = Statements.LetStatement()
        statement.Token = self.CurrentToken
        # 識別子
        if not self.ExpectPeek(Lexer.TokenType.IDENT):
            return None
        statement.Name = Expressions.Identifier(self.CurrentToken, self.CurrentToken.Literal)
        # イコール
        if not self.ExpectPeek(Lexer.TokenType.ASSIGN):
            return None
        self.ReadToken()
        # 式
        statement.Value = self.ParseExpression(Precedence.LOWEST)

        # セミコロン
        if self.NextToken.Type != Lexer.TokenType.SEMICOLON:
            return None

        self.ReadToken()

        return statement
    # endregion

class Precedence(Enum):
    LOWEST = 1
    EQUALS = 2
    LESSGREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7
