import Lexer

while True:
    lexer = Lexer.Lexer(input(">> "))

    while True:
        token = lexer.NextToken()
        if token.Type == Lexer.TokenType.EOF:
            break
        print(token.Type,"\"" + token.Literal + "\"")