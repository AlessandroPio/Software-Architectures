import subprocess
import sys
from config import t_f as list_microservices
import ply.lex as lex
import ply.yacc as yacc

# token
tokens = [
    'ONEOF',
    'SEQ',
    'AND',
    'OR',
    'f',            # per gestire le stringhe terminali
    'LPARENT',      # per gestire la [
    'RPARENT',      # per gestire la ]
    'SEMICOLON'     # per gestire ;
]

"""
prec ‘ticket_availability’ > ((‘event_booking’ ⪰ ‘parking_recommendation’) | ‘weather_checking’)
"""
# regole dei token
t_ONEOF = r'one_of'
t_SEQ = r'seq'
t_AND = r'and'
t_OR = r'or'
t_LPARENT = r'\['
t_RPARENT = r'\]'
t_SEMICOLON = r'\;'
t_f = list_microservices
t_ignore = ' \t'    # per ignorare gli spazi

# regole di precedenza
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
)

# per errori dei token
def t_error(t):
    print(f"Token non riconosciuto: {t.value[0]}")
    t.lexer.skip(1)

# regole parsing
def p_start(p):
    '''
    G_user : F1
           | f
    '''

def p_F1(p):
    '''
    F1 : LPARENT F2 RPARENT
       | ONEOF LPARENT F3 RPARENT
       | SEQ LPARENT F3 RPARENT
    '''

def p_F2(p):
    '''
    F2 : F2 AND F2
       | F2 OR F2
       | f
    '''

def p_F3(p):
    '''
    F3 : f SEMICOLON F3
       | f
    '''

# per errori parsing
def p_error(p):
    print(f"Errore di parsing inatteso a livello di token: {p}")

lexer = lex.lex()
parser = yacc.yacc()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <user_input>")
        sys.exit(1)

    user_input = sys.argv[1]

    try: # gestire errore
        result = parser.parse(user_input, lexer=lexer)
        script_path = "priority.py"
        subprocess.run(["python", script_path, user_input])
    except Exception as e:
        print(f"Errore durante il parsing: {e}")

"""
examples = [
    "GUser ::= one_of['weather_checking';'parking_recommendation']",
    "GUser ::= seq['parking_recommendation'; 'event_booking']",
    "GUser ::= ['ticket_availability' and 'event_booking']",
    ['ticket_avaiability' OR 'event_booking' AND 'parking_recommendation']
    'ticket_availability'
]
"""
