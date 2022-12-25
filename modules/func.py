# clean screen
clean = lambda: print("\033c", end="")

# spacer
space = lambda x: "   "+"\b"*(len(x)-1)

# idk
phead = lambda x,y: print(f'\u001b[4m{x}  {space(x)}{y}\033[0m')