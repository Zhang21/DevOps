'''A handy python3.4 module

Name: fibo
Des: Fibonacci  numbers module
fun:
  - fib: return series
  - fib2: return list
'''


def fib(n):
    a, b = 0, 1
    while b < n:
        print(b, end=', ')
        a, b =b, a+b
    print()

def fib2(n):
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result


if __name__ == "__main__":
    import sys
    fib(int(sys.argv[1]))
