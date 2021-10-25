import time


t1= time.time()
print(time.asctime(time.localtime(t1)))

time.sleep(5)

t2= time.time()
print(time.asctime(time.localtime(t1)))

t3= t2-t1 

print(time.asctime(time.localtime(t3)))
