'''
    ** cminus language lexical analyzer **
    *** This code uses PLY module's lex.py file to identify tokens. So make sure you have the lex.py file in the lex folder in the current directory. Download lex.py from: https://github.com/dabeaz/ply/blob/master/src/ply/lex.py
'''

from ply import lex

# Define token types
tokens = (
    'KEYWORD',
    'IDENTIFIER',
    'CONSTANT_FLOAT',
    'CONSTANT_INT',
    'STRING_LITERAL',
    'ARITH_OP',
    'LOGIC_OP',
    'RELATIONAL_OP',
    'SEPARATOR',
)


# Define regular expressions for token types
t_KEYWORD = r'(int|float|if|else|exit|while|read|write|return)'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'

t_CONSTANT_FLOAT = r'\d+\.\d+'
t_CONSTANT_INT = r'\d+'
t_STRING_LITERAL = r'\'[^\']*\''

t_ARITH_OP = r'[+\-*/=]'
t_LOGIC_OP = r'!|&&|\|\|'
t_RELATIONAL_OP = r'==|!=|<=|>=|<|>'
t_SEPARATOR = r'[(),{}[\];]'


# Declare the states for our cminus comments
states = (
    ('cmcomment', 'exclusive'),
)

# Match the comment start /*. Enter cmcomment state.
def t_cmcomment(t):
    r'/\*'
    t.lexer.code_start = t.lexer.lexpos        # Record the starting position
    t.lexer.level = 1                          # Initial brace level
    t.lexer.begin('cmcomment')                 # Enter 'cmcomment' state

# --- Rules for cmcomment state ---

# Rule for start of the comment
def t_cmcomment_start(t):
    r'/\*'
    t.lexer.level +=1 

# Rule for end of the comment
def t_cmcomment_end(t):
    r'\*/'
    t.lexer.level -=1

    # If comment ends, return type as COMMENT and value ...
    if t.lexer.level == 0:
         t.value = "..."
         t.type = "COMMENT"
         t.lexer.lineno += t.value.count('\n')
         t.lexer.begin('INITIAL')           
         return t


# Rule for cmcomment string
def t_cmcomment_string(t):
   r'\"([^\\\n]|(\\.))*?\"'

# Rule for cmcomment character literal
def t_cmcomment_char(t):
   r'\'([^\\\n]|(\\.))*?\''

# Rule for cmcomment non-whitespace characters (Any sequence of non-whitespace characters)
def t_cmcomment_nonspace(t):
   r'[^\s\'\"]+'

# Rule for cmcomment ignored characters (whitespace)
t_cmcomment_ignore = " \t\n"

# Rule for cmcomment for bad characters, we just skip over it
def t_cmcomment_error(t):
    t.lexer.skip(1)

def t_whitespace(t):
    # Defining a rule to skip whitespace
    r'\s+'
    pass

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


def lexical_analyzer(input_file: str) -> list:

    # initializing ply's lex engine
    lexer = lex.lex()

    # reading and storing source code line by line into a buffer
    source_code_lines = []
    with open(input_file) as f:
        source_code_lines = f.readlines()
    
    # buffer to store tokens
    source_code_tokens = []

    for line in source_code_lines:

        # feeding one line at a time to the lexer
        lexer.input(line)
    
        # identify all tokens in the line
        while True:
            token = lexer.token()
            if not token:
                break
            source_code_tokens.append((token.type, token.value))
    
    return source_code_tokens


if __name__ == "__main__":
    
    source_code_tokens = lexical_analyzer('/Users/saichandrarapolu/Downloads/input.cminus')
    print(source_code_tokens)
