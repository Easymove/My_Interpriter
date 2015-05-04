__author__ = 'Alex'

from graphviz import Digraph


class Node(object):

    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []
        self.numb = None


class ProgramInfo(object):

    def __init__(self, tokens, user_vars, user_consts, rwords, delimiters, m_delimiters, whitespace):
        self.tokens = tokens
        self.user_vars = user_vars
        self.user_consts = user_consts
        self.rwords = rwords
        self.delimiters = delimiters
        self.m_delimiters = m_delimiters
        self.whitespace = whitespace
        self.tree = None

    def get_delim_rword_code(self, name):
        res = None
        if name.upper() in self.rwords.keys():
            res = self.rwords[name.upper()]
        elif name.upper() in self.delimiters.keys():
            res = self.delimiters[name.upper()]
        elif name.upper() in self.m_delimiters.keys():
            res = self.m_delimiters[name.upper()]
        return res

    def get_const(self, code):
        for i in self.user_consts.keys():
            if self.user_consts[i] == code:
                return i
        return 0

    def get_var(self, code):
        for i in self.user_vars.keys():
            if self.user_vars[i] == code:
                return i
        return 0

    def set_tree(self, tree):
        self.tree = tree

    def print_tables(self):
        print('__________ RWORDS __________________')
        print_dict(self.rwords)
        print('__________ DELIMITERS ______________')
        print_dict(self.delimiters)
        print('__________ M_DELIMITERS ____________')
        print_dict(self.m_delimiters)
        print('__________ VARS ____________________')
        print_dict(self.user_vars)
        print('__________ CONSTS __________________')
        print_dict(self.user_consts)
        print('__________ LEXEMS TABLE ____________')

    def print_tokens(self):
        for i in self.tokens:
            print("Code: {0}; Line: {1}; Pos: {2}".format(i.code, i.line, i.column))


class Token(object):

    def __init__(self, cd, ln, col):
        self.code = cd
        self.line = ln
        self.column = col


def gen_id(dict, from_n):
    if dict:
        return max(dict.values()) + 1
    else:
        return from_n


def parse_id(program_text, i):
    start_i = i
    res = program_text[i]
    i += 1
    if i >= len(program_text):
        return [res, i, i - start_i]
    while ord(program_text[i].upper()) in range(ord('A'), ord('Z')) or ord(program_text[i]) in range(ord('0'), ord('9')):
        res += program_text[i]
        i += 1
        if i >= len(program_text):
            break
    return [res, i, i - start_i]


def parse_digit(program_text, i):
    start_i = i
    res = program_text[i]
    i += 1
    if i >= len(program_text):
            return [res, i]
    while ord(program_text[i]) in range(ord('0'), ord('9')):
        res += program_text[i]
        i += 1
        if i >= len(program_text):
            break
    return [res, i, i - start_i]


def parse_com(program_text, i, cur_line, inline_pos):
    lines = 0
    tmp_inline_pos = inline_pos
    if program_text[i] + program_text[i+1] == '(*':
        i += 2
        while len(program_text) > i + 1:
            if program_text[i] + program_text[i+1] == '*)':
                i += 2
                tmp_inline_pos += 2
                break
            elif program_text[i] == '\n':
                lines += 1
                tmp_inline_pos = 0
            i += 1
            tmp_inline_pos += 1
        if program_text[i - 2] + program_text[i - 1] != '*)':
            raise Exception("Unclosed commentary detected; line: {0}; column: {1};".format(cur_line + lines, tmp_inline_pos))
            return [i + 1, tmp_inline_pos, lines + cur_line]
    else:
        raise Exception("Incorrect commentary beginning detected; line: {0}; column: {1};".format(cur_line + lines, tmp_inline_pos))
        return [i, tmp_inline_pos, lines + cur_line]
    return [i, tmp_inline_pos, lines + cur_line]


def print_dict(dictionary):
    for i in dictionary.keys():
        print("Key: {0} Value: {1}".format(i, dictionary[i]))


node_n = 0


def to_dot(node, name):
    output = open(name, 'w')
    res = Digraph(comment="resulting tree")
    to_dot_add_nodes(node, res)
    to_dot_add_edges(node, res)
    output.write(res.source)
    return 0


def to_dot_add_nodes(node, graph):
    global node_n
    if node.value:
        if isinstance(node.value, list):
            res_str = str(node.type) + ':'
            for i in node.value:
                res_str += ' ' + str(i)
        else:
            res_str = node.type + ': ' + str(node.value)
        graph.node(str(node_n), res_str)
    else:
        graph.node(str(node_n), node.type)
    node.numb = node_n
    node_n += 1
    if not node.children:
        return
    else:
        for cp in node.children:
            to_dot_add_nodes(cp, graph)


def to_dot_add_edges(node, graph):
    if not node.children:
        return
    else:
        for cp in node.children:
            graph.edge(str(node.numb), str(cp.numb))
            to_dot_add_edges(cp, graph)


