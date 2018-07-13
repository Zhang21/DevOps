
'''
while True:
   try:
       x = int(input('Input a number: '))
       break
   except:
   #except ValueError:
       print('Error,Try again...')
'''

'''
import sys

try:
    f = open('/tmp/1.txt')
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print('OS error: {}'.format(err))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected erros", sys.exc_info()[0])
    raise
'''

try:
    sum = 'a' + 'b'
except TypeError:
    print('TypeError')
else:
    print('else: ', sum)
