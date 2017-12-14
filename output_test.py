import colorama as cr
    
print(cr.Fore.RED + 'some red text')
print(cr.Back.GREEN + 'and with a green background')
print(cr.Style.DIM + 'and in dim text')
print(cr.Style.RESET_ALL)
print('back to normal now')

input()