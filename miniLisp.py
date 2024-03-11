# -*- coding:utf-8 -*-

import operator as op
from functools import reduce

import sys
sys.tracebacklimit=0

Symbol = str #Symbol in minilisp is str in python
Number = int 
Atom = (Symbol, Number) # Atom in minilisp is Symbol or Number in python to make sure that it wont fall apart
List = list # List in minilisp is list in python
Exp = (Atom, List) # Exp in minilisp is Atom or List in python
Env = dict # Env in minilisp is dict in python

class MiniLisp:
    def __init__(self):
        self.AST = None #create Ast with None

    def interprete(self, file):
        # read file if exists
        if file:
            with open(file, 'r') as f:
                lines = f.read().split('\n') # slpit lines
            f.close()
        # or user input :)
        else:
            lines = []
            while True:
                try: 
                    line = input('miniLisp >> ')
                    lines.append(line) # append it
                except EOFError:
                    break # stop until enter finish
        self.AST = self.parse(f'({"".join(lines)})') # def print dont have () so add it QAQ
        env = standard_env() # create env
        for statement in self.AST: #list in list or atom"s" in list (operand and operator) 
            eval(statement, env) # eval it 

    def tokenize(self, line:str)->List: # just to tokenize it
        return line.replace('(', ' ( ').replace(')', ' ) ').split() # replace ( with space(space and split it for better parse
    
    def parse(self, program:str)->Exp: # parse it
        return self.createAST(self.tokenize(program)) # create AST with tokens
    
    def createAST(self, tokens:list)->Exp: # create AST
        if len(tokens) == 0: 
            raise SyntaxError('unexpected EOF while reading')  # eof then give se;-;
        token = tokens.pop(0) # pop it
        if token == '(': # if token is ( then create AST
            AST = []
            while tokens[0] != ')': #find ) then stop
                AST.append(self.createAST(tokens))  # create AST and append it
            tokens.pop(0) # pop )
            return AST
        elif token == ')': # if token is ) then give error
            raise SyntaxError('unexpected )') #;-;
        else:
            return self.atom(token) # if token is not ( or ) then it's atom :O eg. num or symbol
    
    def atom(self, token:str)->Atom:
        try : return int(token) # if int then return int
        except ValueError: # if not int then return ...?
            try: return float(token) # if float then return float
            except ValueError:
                return Symbol(token) # if not float then return Symbol~

class Env(dict): # env is dict in python eg. {a:1, b:2} first is key(or var) second is value
    def __init__(self, params=(), args=(), outer=None): # param is (), args is (), outer is None
        super().__init__(self) #inherit built in dict
        self.update(zip(params, args)) # zip params and args and update it
        self.outer = outer 

    def find(self, var):
        if var in self: # if var in inner then return inner
            return self
        elif self.outer !=None : # if var not in inner then find in outer
            return self.outer.find(var)
        if var not in self and self.outer == None: # if var not in inner and outer is None then give error
            raise NameError(f'{var} is not defined')#;-; the var is not defined yet

def standard_env()->Env:
    env = Env() # create env
    env.update({
        'print-num':print,
        'print-bool':lambda x:print('#t') if x else print('#f'), 
        '+':op_add,
        '-':op_sub,
        '*':op_mul,
        '/':op_div,
        'mod':op_mod,
        '>':op_gt,
        '<':op_lt,
        '=':op_eq,
        'and':op_and,
        'or':op_or,
        'not':op_not,
        '#t':True,
        '#f':False
    }) # predefine some var and func
    return env

def check_args_num(args:str, num:int): # to check number of args is right or not
    if len(args) == 2: 
        if (int(args[0]) > num): # if args is 2* then check if args is bigger than num
            raise SyntaxError('syntax error: wrong number of args') # if bigger then give error
    else: 
        if (int(args) != num): # if args is not 2* then check if args is equal to num
            raise SyntaxError('syntax error: wrong number of arguments')

def check_int_type(args): # to check type of args is right or not
    if not all (type(arg) == int for arg in args): # check if all args is int
        raise TypeError('type error')
    
def check_bool_type(args): # to check type of args is right or not
    if not all (type(arg) == bool for arg in args): # check if all args is bool
        raise TypeError('type error')
    
def op_add(*args): # 12
    check_args_num("2*",len(args)) # check if args is bigger or eq to than 2
    check_int_type(args) # check if all args is int
    return reduce(op.add, args) #  if args is [1, 2, 3, 4, 5], reduce(op.add, args) calculates ((((1+2)+3)+4)+5), which is 15.

def op_sub(*args):
    check_args_num("2",len(args)) #check if args is equal to 2
    check_int_type(args) # check if all args is int
    return op.sub(*args) #if args is [10, 3, 2], reduce(op.sub, args) would calculate ((10 - 3) - 2), which is 5.

def op_mul(*args): 
    check_args_num("2*",len(args)) # check if args is bigger than or eq to 2
    check_int_type(args) # check if all args is int
    return reduce(op.mul, args, 1) # if args is [1, 2, 3, 4, 5], reduce(op.mul, args, 1) calculates (((((1*2)*3)*4)*5)*1), which is 120.

def op_div(*args):
    check_args_num("2",len(args)) # check if args is equal to 2
    check_int_type(args) # check if all args is int
    return op.floordiv(*args) # / 8 3 => 2.6666666666666665 => 2

def op_mod(*args):
    check_args_num("2",len(args)) # ?check if args is equal to 2
    check_int_type(args) # check if all args is int
    return op.mod(*args) # mod 10 3 => 1

def op_gt(*args):
    check_args_num("2",len(args)) # check if args is equal to 2
    check_int_type(args) # check if all args is int
    return op.gt(*args) # return True if args[0] > args[1] else False

def op_lt(*args):
    check_args_num("2",len(args)) # check if args is equal to 2
    check_int_type(args) # check if all args is int
    return op.lt(*args) # return True if args[0] < args[1] else False

def op_eq(*args):
    check_args_num("2*",len(args)) # check if args is equal to 2
    check_int_type(args) # check if all args is int
    return all(args[0]==arg for arg in args) # return True if all args is equal else False

def op_and(*args):
    check_args_num("2*",len(args)) # check if args is bigger than or eq to 2
    check_bool_type(args) # check if all args is bool
    return reduce(op.and_,args) # return True if all args is True else False

def op_or(*args):
    check_args_num("2*",len(args)) # check if args is bigger than or eq to 2
    check_bool_type(args) # check if all args is bool
    return reduce(op.or_, args) # return True if any args is True else False

def op_not(*args):
    check_args_num("1",len(args)) # check if args is equal to 1
    check_bool_type(args) # check if arg is bool
    return op.not_(*args)# return True if args is False else False

class func: # user defined function
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env  # store as instance var

    def __call__(self, *args):
        func_env = Env(self.params, args, self.env) # create env
        func_res = None # create res
        for statement in self.body:
            func_res = eval(statement, func_env) 
        return func_res # return res
    
def eval(exp: Exp, env: Env): # eval it
    if isinstance(exp, Symbol): # if exp is Symbol
        return env.find(exp)[exp] # if exp is in env then return it else give error
    elif isinstance(exp, Number): # if exp is Number
        return exp # return it
    
    op, *args = exp # expression is op and args

    if op == 'define': # when op is define #define a 1 
        (var, exp) = args # var is args[0] and exp is args[1] #var a exp 1
        env[var] = eval(exp, env) # eval exp and store it in env #env[a] = 1

    elif op == 'fun': # when op is fun # define a (fun (x) (+ x 1))
        (params, *body) = args # params is args[0] and body is args[1:] #params x body (+ x 1)
        return func(params, body, env) # return func
        
    elif op == 'if': # when op is if # if (> 1 2) 1 2
        (test, conseq, alt) = args # test is args[0], conseq is args[1] and alt is args[2]
        res = eval(test, env) # eval test and store it in res
        if not isinstance(res, bool): # if res is not bool then give error
            raise SyntaxError('syntax error: "boolean" expected not "number"')
        exp = (conseq if res else alt) # if res is True then exp is conseq else exp is alt
        return eval(exp, env) # eval exp and return it
    
    
    else: # when op is not define, fun, if # (+ 1 2)
        proc = eval(op, env) # eval op and store it in proc
        vals = [eval(arg, env) for arg in args] # eval args and store it in vals
        return proc(*vals) 