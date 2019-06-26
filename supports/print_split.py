# coding: utf-8

####################################################################################################
# print split
####################################################################################################

split = '-' * 20

def print_war(s):
    print('||:' + s)

def print_log(s):
    print(split + '[ ' + s + ' ]' + split)

def print_head():
    print('\n+' + split + '+')

def print_sep():
    print('+' + split + '+')

def print_foot():
    print('+' + split + '+\n')

def print_body(s):
    print('|' + s)

