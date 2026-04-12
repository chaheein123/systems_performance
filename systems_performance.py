# kernel, process, thread, main memory, virtual memory, context switch, mode switch, syscall, 

class Core:
    def __init__(self, name):
        self.hardware_thread_1 = HardwareThread(f"{name}-hardware_thread_1")
        self.hardware_thread_2 = HardwareThread(f"{name}-hardware_thread_2")


class HardwareThread:
    def __init__(self, name):
        self.name = name
        self.mode = "user_mode"


class PlatformThread:
    def __init__(self):
        pass

class Proc:
    def __init__(self, task):
        self.task = task
    def begin_task(self):
        process_thread = PlatformThread()
        
class MainMem:
    mem = [None] * 10
    @classmethod
    def add_to_mem(cls, proc):
        for i in range(len(cls.mem)):
            if cls.mem[i] == None:
                cls.mem[i] = proc
                break



my_core = Core("C1")
print(my_core.hardware_thread_1.name)
MainMem.add_to_mem("awa")
print(MainMem().mem)