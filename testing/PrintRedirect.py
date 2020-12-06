# from contextlib import redirect_stdout

# with open('out.txt', 'w') as f:
#     with redirect_stdout(f):
#         print('data')

# print("hmm")

import sys
sys.stdout=open("test.txt","a")
for i in range(4):
    print ("hell2o")
a = 1
b = "a"
try:
    print(a+b)
except Exception as e:
    print("error: " + str(e))
#sys.stdout.close()