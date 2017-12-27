class KhipuError(Exception):

    def __init__(self, result):
        Exception.__init__(self, result)
