class CustomLogin(object):
    def error(msg:str):
        raise NameError(msg)
    def warning(msg:str):
        print("WARNING:",msg)