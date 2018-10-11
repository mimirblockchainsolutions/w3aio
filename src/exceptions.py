

class Web3AIOException(Exception):
    """
    Base Exception class for Web3AIO
    """
    pass


class JsonRPCError(Exception):
    """
    JSONRPC response error
    """
    def __init__(self, error):
        self.code = error.code
        self.message = error.message

class BadLength(Exception):
    """
    This error is raised of a type encoding fails due to data length.
    """

class BadInitialType(Exception):
    """
    This error is raised if the object can not be encoded to the requested type.
    """


class BadComparisonType(Exception):
    """
    This error is raised if the compared object is of a different type than the item compared to.
    """
