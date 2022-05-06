def ToJSON(Name, p):
    s = ""
    s += "{"
    s += "\"ASTName\":\"" + Name + "\""
    s += ","
    s += "\"Param\""
    s += ":{"

    for i in range(len(p)):
        s += "\"" + p[i][0] + "\":" + p[i][1]
        if len(p) - 1 != i:
            s += ","

    s += "}"
    s += "}"
    return s
