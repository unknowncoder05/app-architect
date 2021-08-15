class CustomLogging(object):
    def log(msg:str):
        print("LOG:",msg)
    def error(msg:str):
        raise NameError(msg)
    def warning(msg:str):
        print("WARNING:",msg)