
class PyphyError(Exception):
    """ Base Class for all-engine related errors """
    pass

class ComponentError(PyphyError):
    pass

class DupeComponentError(ComponentError):
    pass

class MissionComponentError(ComponentError):
    pass

class StageObjectError(PyphyError):
    pass

class ArgumentError(PyphyError):
    pass

class NotExpectedArgumentType(ArgumentError):
    pass

class IncorrectArgumentFormat(ArgumentError):
    pass




