def shop(kind, *arguments, **keywords):
    print("-- Do you have any ", kind, "?")
    print("-- I'm sorry, we're all out of ", kind)
    for arg in arguments:
        print(arg)
    print('\n ----- \n')
    for kw in keywords:
        print(kw, ':', keywords[kw])


shop('Kind', 'arg1', 'arg2', kw1='KW1', kw2='KW2', kw3='KW3')
