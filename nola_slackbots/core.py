from python_bot import python_rtm
from bash_bot import bash_rtm
from git_bot import git_rtm

import multiprocessing
import threading

one = threading.Process(target=python_rtm.start)
two = threading.Process(target=bash_rtm.start)
three = threading.Process(target=git_rtm.start)

one.start()
two.start()
three.start()


one.join()
two.join()
three.join()
