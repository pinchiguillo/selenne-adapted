import Selenne
import sys

sys.dont_write_bytecode = True #? Prevent .pyc files from being written

if __name__ == '__main__':
    Selenne.Core().boot()
    #Selenne.setup()
