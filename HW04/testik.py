
from os import X_OK


def boo():
    lst_boo = [1, 2, 3, 4, 5]
    foo(lst_boo)
    print(lst_boo)


def foo(lst):
    lst[1] = 10000
    kst = lst.copy()
    kst[4] = 10000
    # return lst


def foo2(a):
    b = a
    b = 10
    a = 10
    return a


boo()

lst_glob = [2, 2, 2, 2, 2]
a = 5
foo(lst_glob)

print(lst_glob)

foo2(a)
print(a)
