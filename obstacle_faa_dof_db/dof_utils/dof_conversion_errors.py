""" Custom Digital Obstacle File data conversion errors. """

class DOFConversionBaseError(Exception):
    """ Base class for other exceptions """
    def __init__(self, value):
        self.value = value
        self.message = message

    def __str__(self):
        return "{} Actual value: {}".format(self.message, self.value)


class FloatNumberRequired(DOFConversionBaseError):
    """ Raised when the value cannot be converted to float number """
    def __init__(self, value):
        self.value = value
        self.message = "Float number required."


class PositiveIntegerNumberRequired(DOFConversionBaseError):
    """ Raised when the value cannot be converted to positive integer number """
    def __init__(self, value):
        self.value = value
        self.message = "Positive integer number required."


class UnknownLightingCode(DOFConversionBaseError):
    """ Raised when the value cannot be converted to positive integer number """
    def __init__(self, value):
        self.value = value
        self.message = "Unknown lighting code."


class UnknownMarkingCode(DOFConversionBaseError):
    """ Raised when the value cannot be converted to positive integer number """
    def __init__(self, value):
        self.value = value
        self.message = "Unknown marking code."


class UnknownVertAccCode(DOFConversionBaseError):
    """ Raised when the value cannot be converted to positive integer number """
    def __init__(self, value):
        self.value = value
        self.message = "Unknown vertical accuracy code."


class UnknownHorAccCode(DOFConversionBaseError):
    """ Raised when the value cannot be converted to positive integer number """
    def __init__(self, value):
        self.value = value
        self.message = "Unknown horizontal accuracy code."

class UnknownVerifStatus(DOFConversionBaseError):
    """ Raised when the value cannot be converted to positive integer number """
    def __init__(self, value):
        self.value = value
        self.message = "Unknown verification status."


class LongitudeConversionError(DOFConversionBaseError):
    """ Raised when the value cannot be converted to positive integer number """
    def __init__(self, value):
        self.value = value
        self.message = "Can not convert source longitude to DD."


class LattitiudeConversionError(DOFConversionBaseError):
    """ Raised when the value cannot be converted to positive integer number """
    def __init__(self, value):
        self.value = value
        self.message = "Can not convert source lattitude to DD."
