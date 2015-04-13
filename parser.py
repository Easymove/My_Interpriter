__author__ = 'Alex'

from lexer import *


def parser(prog_info):
    return program(prog_info)


def program(prog):
    res = Node("program")
    stack = ("Program", proc_id, ";", block, ".")
    for cp in stack:
        if isinstance(cp, basestring):
            if len(prog.tokens) > 0:
                if prog.get(cp) == prog.tokens[0].code:
                    prog.tokens = prog.tokens[1:]
                    pass
                else:
                    raise Exception("'{0}' expected; line: {1}, column: {2} ".format(cp, prog.tokens[0].line, prog.tokens[0].column))
            else:
                raise Exception("'{0}' expected;".format(cp))
        else:
            res.children.append(cp(prog))
    return res


def proc_id(prog):
    res = Node("procedure_id")
    res.children.append(id(prog))
    return res


def const_id(prog):
    res = Node("const_id")
    res.children.append(id(prog))
    return res


def var_id(prog):
    res = Node("var_id")
    res.children.append(id(prog))
    return res


def id(prog):
    if len(prog.tokens) > 0:
        if prog.tokens[0].code < 1000:
            raise Exception("id expected; line {1}, column{2} ".format(prog.tokens[0].line, prog.tokens[0].column))
    else:
        raise Exception("Identifier expected;")
    res_token = prog.tokens[0]
    prog.tokens = prog.tokens[1:]
    return Node("id", res_token.code)


def const(prog):
    res_tokens = []
    if len(prog.tokens) > 0:
        if prog.tokens[0].code == 45:
            res_tokens.append(prog.tokens[0].code)
            prog.tokens = prog.tokens[1:]
        if not (500 < prog.tokens[0].code < 1001):
            raise Exception("const expected; line {1}, column{2} ".format(prog.tokens[0].line, prog.tokens[0].column))
    else:
        raise Exception("Constant expected;")
    res_tokens.append(prog.tokens[0].code)
    prog.tokens = prog.tokens[1:]
    return Node("const", res_tokens)


def block(prog):
    res = Node("block")
    stack = (declarations, "BEGIN", statement_list, "END")
    for cp in stack:
        if isinstance(cp, basestring):
            if len(prog.tokens) > 0:
                if prog.get(cp) == prog.tokens[0].code:
                    prog.tokens = prog.tokens[1:]
                    pass
                else:
                    raise Exception("'{0}' expected; line: {1}, column: {2} ".format(cp, prog.tokens[0].line, prog.tokens[0].column))
            else:
                raise Exception("'{0}' expected;".format(cp))
        else:
            res.children.append(cp(prog))
    return res


def declarations(prog):
    res = Node("declarations")
    func_res = const_declarations(prog)
    res.children.append(func_res)
    return res


def const_declarations(prog):
    res = Node("const_declarations")
    stack = ("CONST", const_declarations_list)
    for cp in stack:
        if isinstance(cp, basestring):
            if len(prog.tokens) > 0:
                if prog.get(cp) == prog.tokens[0].code:
                    prog.tokens = prog.tokens[1:]
                    pass
                else:
                    return res
            else:
                raise Exception("'{0}' expected;".format(cp))
        else:
            res.children.append(cp(prog))
    return res


def const_declarations_list(prog):
    res = Node("const_declarations_list")
    stack = (const_declaration, const_declarations_list)
    if prog.tokens[0].code < 1001:
        return res
    for cp in stack:
        res.children.append(cp(prog))
    return res


def const_declaration(prog):
    res = Node("const_declaration")
    stack = (var_id, "=", const, ";")
    for cp in stack:
        if isinstance(cp, basestring):
            if len(prog.tokens) > 0:
                if prog.get(cp) == prog.tokens[0].code:
                    prog.tokens = prog.tokens[1:]
                    pass
                else:
                    raise Exception("'{0}' expected; line: {1}, column: {2} ".format(cp, prog.tokens[0].line, prog.tokens[0].column))
            else:
                raise Exception("'{0}' expected;".format(cp))
        else:
            res.children.append(cp(prog))
    return res


def statement_list(prog):
    res = Node("statement_list")
    stack = (statement, statement_list)
    if prog.tokens[0].code < 1001:
        return res
    for cp in stack:
        res.children.append(cp(prog))
    return res


def statement(prog):
    res = Node("statement")
    stack = (var_id, ":=", const, ";")
    for cp in stack:
        if isinstance(cp, basestring):
            if len(prog.tokens) > 0:
                if prog.get(cp) == prog.tokens[0].code:
                    prog.tokens = prog.tokens[1:]
                    pass
                else:
                    raise Exception("'{0}' expected; line: {1}, column: {2} ".format(cp, prog.tokens[0].line, prog.tokens[0].column))
            else:
                raise Exception("'{0}' expected;".format(cp))
        else:
            res.children.append(cp(prog))
    return res

tree = parser(lexer('test.txt'))
to_dot(tree, "test_graph.dot")
