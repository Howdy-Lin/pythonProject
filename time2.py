import time
def countdown(n):
    print("次執行緒執行中")
    while n>0:
        print('countdown',n)
        n-=1
        time.sleep(5)
countdown(10)

from threading import  Thread
t = Thread(target=countdown,args=(5,),daemon=True)
t.start()

while t.is_alive():
    print('次執行緒執行中')
    time.sleep(1)
else:
    print('次執行緒完成')