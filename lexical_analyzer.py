__author__ = 'Alex'

from utils import *


def lexer(path):
    lexems = []
    whitespace = {'\t': 9, '\n': 10, '\r': 13, ' ': 32, '\x0b': 11}
    rwords = {'PROGRAM': 401, 'BEGIN': 402, 'END': 403, 'CONST': 404}
    delimiters = {';': 59, '+': 43, '*': 42, '/': 47, '=': 61,  ':': 58, '.': 46}
    m_delimiters = {':=': 301}
    user_vars = {}
    user_consts = {}

    file = open(path, "r+")

    program_text = file.read()
    if len(program_text) == 0:
        return 0

    i = 0
    cur_line = 1
    inline_pos = 0

    while i < len(program_text):
        cur_char = program_text[i]

        if cur_char in whitespace:
            if cur_char == '\n':
                cur_line += 1
                inline_pos = 0
            i += 1
            inline_pos += 1

        elif ord(cur_char.upper()) in range(ord('A'), ord('Z')):
            tmp_id_info = parse_id(program_text, i)
            if tmp_id_info[0].upper() in rwords:
                lexems.append(Token(rwords[tmp_id_info[0].upper()], cur_line, inline_pos))
            else:
                if not tmp_id_info[0] in user_vars.keys():
                    user_vars[tmp_id_info[0]] = gen_id(user_vars, 1001)
                lexems.append(Token(user_vars[tmp_id_info[0]], cur_line, inline_pos))
            inline_pos += tmp_id_info[2]
            i = tmp_id_info[1]

        elif cur_char == '-' or ord(cur_char) in range(ord('0'), ord('9')):
            tmp_dig_info = parse_digit(program_text, i)
            if not tmp_dig_info[0] in user_consts.keys():
                tmp_id = gen_id(user_consts, 501)
                user_consts[tmp_dig_info[0]] = tmp_id
            else:
                tmp_id = user_consts[tmp_dig_info[0]]
            lexems.append(Token(tmp_id, cur_line, inline_pos))
            if len(program_text) - tmp_dig_info[1] > 0:
                if ord(program_text[tmp_dig_info[1]].upper()) in range(ord('A'), ord('Z')):
                    raise Exception("incorrect digit detected; line: {0}, column: {1} ".format(cur_line, inline_pos))
            inline_pos += tmp_dig_info[2]
            i = tmp_dig_info[1]

        elif cur_char in delimiters:
            if len(program_text) - i > 1:
                if cur_char + program_text[i + 1] in m_delimiters:
                    lexems.append(Token(m_delimiters[cur_char + program_text[i + 1]], cur_line, inline_pos))
                    i += 2
                    inline_pos += 2
                    continue
            lexems.append(Token(delimiters[cur_char], cur_line, inline_pos))
            i += 1
            inline_pos += 1

        elif cur_char == '(':
            tmp_com_info = parse_com(program_text, i, cur_line, inline_pos)
            i = tmp_com_info[0]
            inline_pos = tmp_com_info[1]
            cur_line = tmp_com_info[2]

        else:
            raise Exception("Unknown symbol detected; line: {0}, column: {1} ".format(cur_line, inline_pos))
            i += 1
            inline_pos += 1

    return ProgramInfo(lexems, user_vars, user_consts, rwords, delimiters, m_delimiters, whitespace)






