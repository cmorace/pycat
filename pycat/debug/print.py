class _DebugCode:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAILURE = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_header(msg: str):
    print(_DebugCode.HEADER + msg + _DebugCode.ENDC)


def print_warning(msg: str):
    print(_DebugCode.WARNING + msg + _DebugCode.ENDC)


def print_failure(msg: str):
    print(_DebugCode.FAILURE + msg + _DebugCode.ENDC)
