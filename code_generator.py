__author__ = 'Alex'


def code_gen(program_info, file_name):
    list_file = open(file_name, 'w')
    res_program = []
    res_program.append('.386\n')
    gen_data_segment(program_info, res_program)
    gen_code_segment(program_info, res_program)
    list_file.writelines(res_program)


def gen_data_segment(program_info, res_program):
    res_program.append('data SEGMENT\n')
    generate_data(program_info.tree, program_info, res_program, [])
    res_program.append('data ENDS\n')


def gen_code_segment(program_info, res_program):
    res_program.append('code SEGMENT\n')
    generate_code(program_info.tree, program_info, res_program)
    res_program.append('code ENDS\n')


def generate_data(node, program_info, res_program, black_list):
    if node.type == 'const_declaration':
        id = program_info.get_var(node.children[0].children[0].value)
        if id not in black_list:
            res_program.append('\t' + id + ' DD ' + str(program_info.get_const(node.children[1].value)) + '\n')
            black_list.append(id)
        else:
            raise Exception('Const redefining detected')
    elif node.type == 'statement':
        id = program_info.get_var(node.children[0].children[0].value)
        if id not in black_list:
            res_program.append('\t' + id + ' DD ' + '0' + '\n')
            black_list.append(id)
        else:
            raise Exception('Assignment to const detected')
    else:
        for i in node.children:
            generate_data(i, program_info, res_program, black_list)


def generate_code(node, program_info, res_program):
    if node.type == 'statement':
        id = program_info.get_var(node.children[0].children[0].value)
        value = str(program_info.get_const(node.children[1].value))
        res_program.append('\t' + 'MOV AX, ' + value + '\n')
        res_program.append('\t' + 'MOV ' + id + ', AX' + '\n')
    else:
        for i in node.children:
            generate_code(i, program_info, res_program)



