# kernel, process, thread, main memory, virtual memory, context switch, mode switch, syscall, 

from enum import Enum

class App:
    def __init__(self, proc):
        # Let the kernel check the memory


        # Let the kernel create the child process of the parent process by forking


        # Let the kernel create the thread (Main thread) inside the process


        # Let the kernel load the process onto the memory



        proc
        pass

    def do_math(self, str_query):
        pass
        # self.core.hardware_thread_1.do_math(str_query)

    @staticmethod
    def main_thread_action():
        print("Hello world")

# class Core:
#     def __init__(self):
#         self.hardware_thread_1 = HardwareThread("hardware_thread_1")
#         self.hardware_thread_2 = HardwareThread("hardware_thread_2")

class HardwareThread:
    class _CPUMODE(Enum):
        USER = 1
        KERNEL = 2
    def __init__(self):
        self.mode = self._CPUMODE.USER
    
    def user_mode(self):
        self.mode = self._CPUMODE.USER

    def kernel_mode(self):
        self.mode = self._CPUMODE.KERNEL

    def has_available_mem(self):
        if self.mode == self._CPUMODE.KERNEL:
            for i in range(len(MainMem.mem)):
                if MainMem.mem[i] == None:
                    return True
            return False
    
    def calculate(self, str_query):
        self.user_mode()
        print("Calculating")



    def do_math(self, str_query):
        # Go into kernel mode and then check the memory. If the memory is available, then create the process, which creates the 
        self.kernel_mode()
        proc = Proc(PlatformThread(0, App.main_thread_action))
        proc.add_thread(self.calculate, str_query)
        if self.has_available_mem():
            MainMem.add_to_mem(proc)
        # print(proc.threadstack)
        


class PlatformThread:
    def __init__(self, priority, action):
        self.priority  = priority
        self.action = action
        

class Proc:
    def __init__(self, mainthread):
        self.threadstack = [mainthread]
    def add_thread(self, func, *args):
        print(*args, "yo")
        self.threadstack.append(func)
        
class MainMem:
    mem = [None] * 10
    @classmethod
    def add_to_mem(cls, proc):
        for i in range(len(cls.mem)):
            if cls.mem[i] == None:
                cls.mem[i] = proc
                break


parent_process = Proc(lambda: print("Hello world."))

# Creating the myapp object only means you've just done "java -c app" on the terminal
myapp = App()
# myapp.do_math("1+3")
