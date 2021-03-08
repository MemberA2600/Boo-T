import random
from datetime import datetime
import time

def sorting(the_list):
    starter=0
    smallest=9999
    index=0

    while starter<len(the_list):
        for number in range(starter, len(the_list)):
            if smallest>the_list[number]:
                smallest=the_list[number]
                index=number

        the_list[starter], the_list[index] = the_list[index], the_list[starter]
        starter+=1
        smallest = 9999

    return(the_list)

random.seed(int(str(datetime.now()).split(".")[1]))

ourlist=[]
for num in range(0,10000):
    ourlist.append(random.randint(0,100))

print(ourlist)
start_time = time.time()

print(sorting(ourlist))

print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
ourlist.sort()
print(ourlist)
print("--- %s seconds ---" % (time.time() - start_time))

