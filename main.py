__author__ = 'Alex'


from syntax_analyzer import *
from lexical_analyzer import *
from code_generator import *
from utils import *


signal_program = parser(lexer('Tests/test.txt'))
to_dot(signal_program.tree, "Generated/test_graph.dot")
code_gen(signal_program, 'Generated/generated.asm')