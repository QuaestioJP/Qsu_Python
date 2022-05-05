from enum import Enum

class Lexer:
    Input = ""
    CurrentChar = ""
    NextChar = ""
    Position = 0

    def NextToken(self):
        pass

    def SkipWhiteSpace(self):
        pass

    def ReadNumber(self):
        number = self.CurrentChar

        while self.IsDigit(self.NextChar):
            number += self.NextChar;

            self.ReadChar()

    def IsDigit(self, c):
        return '0' <= c <= '9'

    def ReadIdentifier(self):
        identifier = self.CurrentChar;

        while self.IsLetter(self.NextChar):
            identifier += self.NextChar
            self.ReadChar()

    def IsLetter(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    def ReadChar(self):
        # CurrentCharをセット
        if self.Position >= len(self.Input):
            self.CurrentChar = "";
        else:
            self.CurrentChar = self.Input[self.Position]

        #NextCharをセット
        if self.Position + 1 >= len(self.Input):
            self.NextChar = "";
        else:
            self.NextChar = self.Input[self.Position + 1]

        #Positionを一つ進める
        self.Position += 1

    def __init__(self,SourceCode):
        Input = SourceCode
        self.ReadChar()

class TokenType(Enum):
    # 不正なトークン = 終端
    ILLEGAL = 1
    EOF =2
    # 識別子
    IDENT =3
    # リテラル
    INT =4
    # 演算子
    ASSIGN =5
    PLUS =6
    MINUS =7
    ASTERISK =8
    SLASH =9
    BANG =10
    LT =11
    GT =12
    EQ =13
    NOT_EQ =14
    # デリミタ
    COMMA =15
    SEMICOLON =16
    # 括弧(){}
    LPAREN = 17
    RPAREN =18
    LBRACE =19
    RBRACE =20
    # キーワード
    FUNCTION =21
    LET =22
    IF =23
    ELSE =24
    RETURN =25
    TRUE =26
    FALSE =27

class Token:
    Type = TokenType.ILLEGAL
    Literal = ""
    KeyWords = {
        "let": TokenType.LET,
        "fn": TokenType.FUNCTION,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "return": TokenType.RETURN,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE
    }

    def __init__(self,tokentype, literal):
        Type = tokentype
        Literal = literal

    def LookupIdentifier(self,identifier):
        if self.KeyWords.get(identifier) != None:
            return self.KeyWords[identifier]

        return  TokenType.IDENT
        pass
