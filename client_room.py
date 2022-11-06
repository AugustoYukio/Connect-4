# SuperFastPython.com
# example determining if the main process can see the manager's process
from multiprocessing import active_children
from multiprocessing import Manager

# protect the entry point
if __name__ == '__main__':
    # create and start the manager
    with Manager() as manager:
        # report all active child processes
        for child in active_children():
            print(child)