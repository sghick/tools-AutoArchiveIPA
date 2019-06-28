# coding: utf-8

####################################################################################################
# print split
####################################################################################################

split = '-' * 20

def print_war(s):
    print('||:' + s)

def print_log(s):
    print(get_log(s))

def print_head():
    print('\n+' + split + '+')

def print_sep():
    print(get_sep())

def print_foot():
    print('+' + split + '+\n')

def print_body(s):
    print('|' + s)

def get_log(s):
    return split + '[ ' + s + ' ]' + split

def get_sep():
    return '+' + split + '+'
