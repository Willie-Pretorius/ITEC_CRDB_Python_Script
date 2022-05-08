from ftsetup import configLoader,routineStart

try:
    configLoader()
    routineStart()
except:
    print("An error has occurred please check the logs")