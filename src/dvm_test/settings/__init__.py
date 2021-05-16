try:
    from .settings_local import *
except ModuleNotFoundError:
    from .settings import *

