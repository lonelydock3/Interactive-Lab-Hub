import sys
import time

t= time.strftime("%m/%d/%Y %H:%M:%S")


if sys.argv[1] == "date":
    print(t[0:10])
 

if sys.argv[1] == "time":
    print(t[11:19])
 
 
 
if sys.argv[1] == "todo_add":
    print("addnow") 
# 
#  
#  
# if sys.argv[1] == "todo_play":
