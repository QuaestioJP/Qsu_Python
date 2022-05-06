import Lexer
import AST
import Statements
import Expressions


class Parser:
    def __init__(self, _lexer):
        self.lexer = _lexer

        self.CurrentToken = self.lexer.NextToken()
        self.NextToken = self.lexer.NextToken()

    def ReadToken(self):
        self.CurrentToken = self.NextToken
        self.NextToken = self.lexer.NextToken()

    def ParseRoot(self):
        root = AST.Root()
        root.Statements = []
        while self.CurrentToken.Type != Lexer.TokenType.EOF:
            statement = self.ParseStatement()
            print(statement)
            if statement is not None:
                root.Statements.append(statement)

            self.ReadToken()
        print(len(root.Statements))
        return root

    def ExpectPeek(self, _type):
        if self.NextToken.Type == _type:
            self.ReadToken()
            return True

        return False

    def ParseStatement(self):
        print(self.CurrentToken.Type,Lexer.TokenType.LET,self.CurrentToken.Type==Lexer.TokenType.LET)
        match self.CurrentToken.Type:
            case Lexer.TokenType.LET:
                return self.ParseLetStatement()
            case _:
                return None

    def ParseLetStatement(self):
        statement = Statements.LetStatement()
        statement.Token = self.CurrentToken
        print(self.CurrentToken.Type,self.NextToken.Type)
        # 識別子
        if not self.ExpectPeek(Lexer.TokenType.IDENT):
            print("ちがーう1")
            return None
        statement.Name = Expressions.Identifier(self.CurrentToken, self.CurrentToken.Literal)
        print(self.CurrentToken.Type,self.NextToken.Type)
        # イコール
        if not self.ExpectPeek(Lexer.TokenType.ASSIGN):
            print("ちがーう2")
            return None

        # 式
        # Todo 後で実装する
        while self.CurrentToken.Type != Lexer.TokenType.SEMICOLON:
            # セミコロンが見つかるまで
            self.ReadToken()

        return statement
