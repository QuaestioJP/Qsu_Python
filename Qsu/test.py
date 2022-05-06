import Lexer
import Parser

while True:
    inputs = input(">> ")
    lexer = Lexer.Lexer(inputs)
    lexer2 = Lexer.Lexer(inputs)
    parser = Parser.Parser(lexer2)
    root = parser.ParseRoot()
    while True:
        token = lexer.NextToken()
        if token.Type == Lexer.TokenType.EOF:
            break
        print(token.Type, "\"" + token.Literal + "\"")

    print(root.ToJSON())
