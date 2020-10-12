import threading 
  
class mythread(threading.Thread): 
    def __init__(self, thread_name, thread_ID): 
        threading.Thread.__init__(self) 
        self.thread_name = thread_name 
        self.thread_ID = thread_ID 
    
    # Overrriding of run() method in the subclass 
    def run(self): 
        print("Thread name: "+str(self.thread_name) +"  "+ "Thread id: "+str(self.thread_ID)); 
  
thread1 = mythread("thread1", 1) 
thread2 = mythread("thread2", 2); 
  
thread1.start() 
thread2.start()

######################下面是函数实现

def thread_1(i):
    print('Value by Thread 1:', i)
 
def thread_2(i):
    print('Value by Thread 2:', i)
 
def thread_3(i):
    print('Value by Thread 3:', i)    
 
    
# Creating three sample threads 
thread1 = threading.Thread(target=thread_1, args=(1,))
thread2 = threading.Thread(target=thread_2, args=(2,))
thread3 = threading.Thread(target=thread_3, args=(3,))
 
# Running three thread object
thread1.start()
thread2.run()
thread3.run()


