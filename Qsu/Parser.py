import Lexer
import AST
import Statements
import Expressions
from enum import IntEnum


class Precedence(IntEnum):
    LOWEST = 1
    EQUALS = 2
    LESSGREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7


class Parser:
    def __init__(self, _lexer):
        self.lexer = _lexer

        self.CurrentToken = self.lexer.NextToken()
        self.NextToken = self.lexer.NextToken()
        self.Errors = []

        self.PrefixParseFns = {}
        self.InfixParseFns = {}

        self.RegisterPrefixParseFns()
        self.RegisterInfixParseFns()

    # region 前置演算子
    def RegisterPrefixParseFns(self):
        self.PrefixParseFns = {Lexer.TokenType.IDENT: self.ParseIdentifier,
                               Lexer.TokenType.INT: self.ParseIntegerLiteral,
                               Lexer.TokenType.BANG: self.ParsePrefixExpression,
                               Lexer.TokenType.MINUS: self.ParsePrefixExpression,
                               Lexer.TokenType.TRUE: self.ParseBooleanLiteral,
                               Lexer.TokenType.FALSE: self.ParseBooleanLiteral,
                               Lexer.TokenType.LPAREN: self.ParseGroupedExpression}

    # endregion

    # region 中置演算子
    Precedences = {
        Lexer.TokenType.EQ: Precedence.EQUALS,
        Lexer.TokenType.NOT_EQ: Precedence.EQUALS,
        Lexer.TokenType.LT: Precedence.LESSGREATER,
        Lexer.TokenType.GT: Precedence.LESSGREATER,
        Lexer.TokenType.PLUS: Precedence.SUM,
        Lexer.TokenType.MINUS: Precedence.SUM,
        Lexer.TokenType.SLASH: Precedence.PRODUCT,
        Lexer.TokenType.ASTERISK: Precedence.PRODUCT
    }

    @property
    def CurrentPrecedence(self):
        if self.Precedences.get(self.CurrentToken.Type):
            return self.Precedences[self.CurrentToken.Type]
        return Precedence.LOWEST

    @property
    def NextPrecedence(self):
        if self.Precedences.get(self.NextToken.Type):
            return self.Precedences[self.NextToken.Type]
        return Precedence.LOWEST

    def RegisterInfixParseFns(self):
        self.InfixParseFns = {Lexer.TokenType.PLUS: self.ParseInfixExpression,
                              Lexer.TokenType.MINUS: self.ParseInfixExpression,
                              Lexer.TokenType.SLASH: self.ParseInfixExpression,
                              Lexer.TokenType.ASTERISK: self.ParseInfixExpression,
                              Lexer.TokenType.EQ: self.ParseInfixExpression,
                              Lexer.TokenType.NOT_EQ: self.ParseInfixExpression,
                              Lexer.TokenType.LT: self.ParseInfixExpression,
                              Lexer.TokenType.GT: self.ParseInfixExpression}

    # endregion

    # region エクスプレッション
    def ParseExpression(self, precedence):
        fn = self.PrefixParseFns.get(self.CurrentToken.Type)
        if fn is None:
            self.AddPrefixParseFnError(self.CurrentToken.Type)
            return None

        leftExpression = fn()

        while self.NextToken.Type != Lexer.TokenType.SEMICOLON and precedence < self.NextPrecedence:
            infix = self.InfixParseFns.get(self.NextToken.Type)
            if infix is None:
                return leftExpression

            self.ReadToken()
            leftExpression = infix(leftExpression)

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

    def ParseBooleanLiteral(self):
        booleanliteral = Expressions.BooleanLiteral()
        booleanliteral.Token = self.CurrentToken
        booleanliteral.Value = self.CurrentToken.Type == Lexer.TokenType.TRUE

        return booleanliteral

    def ParsePrefixExpression(self):
        expression = Expressions.PrefixExpression()
        expression.Token = self.CurrentToken
        expression.Operator = self.CurrentToken.Literal

        self.ReadToken()

        expression.Right = self.ParseExpression(Precedence.PREFIX)
        return expression

    def ParseInfixExpression(self, left):
        expression = Expressions.InfixExpression()
        expression.Token = self.CurrentToken
        expression.Operator = self.CurrentToken.Literal
        expression.Left = left

        precedence = self.CurrentPrecedence
        self.ReadToken()
        expression.Right = self.ParseExpression(precedence)

        return expression

    def ParseGroupedExpression(self):
        self.ReadToken()

        expression = self.ParseExpression(Precedence.LOWEST)

        if not self.ExpectPeek(Lexer.TokenType.RPAREN):
            return None

        return expression

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

    def AddPrefixParseFnError(self, Tokentype):
        self.Errors.append(Tokentype + "に関連付けられたprefixparsefunctionはありません")

    # endregion

    # region ステートメント
    def ParseStatement(self):
        match self.CurrentToken.Type:
            case Lexer.TokenType.LET:
                return self.ParseLetStatement()
            case Lexer.TokenType.RETURN:
                return self.ParseReturnStatement()
            case Lexer.TokenType.IF:
                return self.ParseIfStatement()
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

    def ParseReturnStatement(self):
        statement = Statements.ReturnStatement()
        statement.Token = self.CurrentToken

        self.ReadToken()

        # 式
        statement.Value = self.ParseExpression(Precedence.LOWEST)
        # セミコロン
        if self.NextToken.Type != Lexer.TokenType.SEMICOLON:
            return None
        self.ReadToken()

        return statement

    def ParseBlockStatement(self):
        block = Statements.BlockStatement()
        block.Token = self.CurrentToken
        block.Statements = []

        self.ReadToken()

        while self.CurrentToken.Type != Lexer.TokenType.RBRACE and self.CurrentToken.Type != Lexer.TokenType.EOF:
            statement = self.ParseStatement()
            if statement is not None:
                block.Statements.append(statement)

            self.ReadToken()

        return block

    def ParseIfStatement(self):
        statement = Statements.IfStatement()
        statement.Token = self.CurrentToken

        if not self.ExpectPeek(Lexer.TokenType.LPAREN):
            return None

        self.ReadToken()

        statement.Condition = self.ParseExpression(Precedence.LOWEST)

        if not self.ExpectPeek(Lexer.TokenType.RPAREN):return None
        if not self.ExpectPeek(Lexer.TokenType.LBRACE):return None

        statement.Consequence = self.ParseBlockStatement()

        if self.NextToken.Type is Lexer.TokenType.ELSE:
            self.ReadToken()
            if not self.ExpectPeek(Lexer.TokenType.LBRACE):return None

            statement.Alternative = self.ParseBlockStatement()

        return statement
    # endregion
