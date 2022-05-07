from enum import Enum


class Lexer:
    def NextToken(self):
        # 空白をぶっ飛ばす
        self.SkipWhiteSpace()

        token = Token(TokenType.ILLEGAL, "")
        a = ""
        match self.CurrentChar:
            case "=":
                if self.NextChar == "=":
                    token = Token(TokenType.EQ, "==")
                    self.ReadChar()
                else:
                    token = Token(TokenType.ASSIGN, self.CurrentChar)
            case "+":
                token = Token(TokenType.PLUS, self.CurrentChar)
            case "-":
                token = Token(TokenType.MINUS, self.CurrentChar)

            case "*":
                token = Token(TokenType.ASTERISK, self.CurrentChar)

            case "/":
                token = Token(TokenType.SLASH, self.CurrentChar)

            case "!":
                if self.NextChar == "=":
                    token = Token(TokenType.NOT_EQ, "!=")
                    self.ReadChar()
                else:
                    token = Token(TokenType.BANG, self.CurrentChar)

            case ">":
                token = Token(TokenType.GT, self.CurrentChar)

            case "<":
                token = Token(TokenType.LT, self.CurrentChar)

            case ",":
                token = Token(TokenType.COMMA, self.CurrentChar)

            case ";":
                token = Token(TokenType.SEMICOLON, self.CurrentChar)

            case "(":
                token = Token(TokenType.LPAREN, self.CurrentChar)

            case ")":
                token = Token(TokenType.RPAREN, self.CurrentChar)

            case "{":
                token = Token(TokenType.LBRACE, self.CurrentChar)

            case "}":
                token = Token(TokenType.RBRACE, self.CurrentChar)

            case "":
                token = Token(TokenType.EOF, "")

            case _:  # 識別子候補生たち
                if self.IsLetter(self.CurrentChar):
                    _identifier = self.ReadIdentifier()
                    Type = LookupIdentifier(_identifier)
                    token = Token(Type, _identifier)
                elif self.IsDigit(self.CurrentChar):
                    number = self.ReadNumber()
                    token = Token(TokenType.INT, number)
                else:
                    token = Token(TokenType.ILLEGAL, self.CurrentChar)

        self.ReadChar()

        return token

    def SkipWhiteSpace(self):
        while self.CurrentChar == ' ' or self.CurrentChar == '\t' or self.CurrentChar == '\r' or self.CurrentChar == '\n':
            self.ReadChar()

    def ReadNumber(self):
        number = self.CurrentChar

        while self.IsDigit(self.NextChar):
            number += self.NextChar

            self.ReadChar()

        return number

    def IsDigit(self, c):
        return '0' <= c <= '9'

    def ReadIdentifier(self):
        identifier = self.CurrentChar

        while self.IsLetter(self.NextChar):
            identifier += self.NextChar
            self.ReadChar()

        return identifier

    def IsLetter(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    def ReadChar(self):
        # CurrentCharをセット
        if self.Position >= len(self.Input):
            self.CurrentChar = ""
        else:
            self.CurrentChar = self.Input[self.Position]

        # NextCharをセット
        if self.Position + 1 >= len(self.Input):
            self.NextChar = ""
        else:
            self.NextChar = self.Input[self.Position + 1]

        # Positionを一つ進める
        self.Position += 1

    def __init__(self, SourceCode):
        self.Input = ""
        self.CurrentChar = ""
        self.NextChar = ""
        self.Position = 0

        self.Input = SourceCode
        self.ReadChar()


class TokenType(Enum):
    # 不正なトークン = 終端
    ILLEGAL = 1
    EOF = 2
    # 識別子
    IDENT = 3
    # リテラル
    INT = 4
    # 演算子
    ASSIGN = 5
    PLUS = 6
    MINUS = 7
    ASTERISK = 8
    SLASH = 9
    BANG = 10
    LT = 11
    GT = 12
    EQ = 13
    NOT_EQ = 14
    # デリミタ
    COMMA = 15
    SEMICOLON = 16
    # 括弧(){}
    LPAREN = 17
    RPAREN = 18
    LBRACE = 19
    RBRACE = 20
    # キーワード
    WHILE = 21
    LET = 22
    IF = 23
    ELSE = 24
    RETURN = 25
    TRUE = 26
    FALSE = 27


def LookupIdentifier(identifier):
    KeyWords = {
        "let": TokenType.LET,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "return": TokenType.RETURN,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "while": TokenType.WHILE
    }

    if KeyWords.get(identifier) is not None:
        return KeyWords[identifier]

    return TokenType.IDENT


class Token:
    def __init__(self, tokentype, literal):
        self.Type = tokentype
        self.Literal = literal
