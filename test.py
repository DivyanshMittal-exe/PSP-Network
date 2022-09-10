a = 1

def f():
    global a 
    a = 2

f()
print(a)