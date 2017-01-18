import os
import sys
# Author ~ WileTheCoyote

    
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)
    
def absolute_path(relative_path):
    if getattr(sys, 'frozen', False):
        APPLICATION_PATH = os.path.dirname(sys.executable)
    elif __file__:
        APPLICATION_PATH = os.path.dirname(__file__)
        
    return os.path.join(APPLICATION_PATH, relative_path)


