from multiprocessing import Process
from time import sleep

def f1():
	sleep(2)

def f2():
	input()
	print("s")

t1 = Process(target = f1)
t2 = Process(target = f2)

t1.start()
sleep(5)
t2.start()

while t1.is_alive() and t2.is_alive():
	continue

t2.terminate()

