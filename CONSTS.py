from enum import Enum

from toolboxs.toolbox import Toolbox

# --
# ... Global Config
# --

PROJECTS_DIR = "/".join(Toolbox.get_root_path().replace("\\", "/").split("/")[:-1])
ROOT_DIR = Toolbox.get_root_path().replace("\\", "/")
APP_DIR = f"{Toolbox.get_root_path()}/app".replace("\\", "/")
CONFIG_JSON = ROOT_DIR + "/config_dictionary/config.json"
EXTERNAL_FILES = ROOT_DIR + "/.external_files"

# --
# ... colors
# --


class COLORS(Enum):
    LOG_PROMPT = "\x1b[35;40;2m"
    DELAY_PROMPT = "\x1b[33;40;2m"
    AQUA_PROMPT = "\x1b[94;40;2m"
    INITIAL_CLASS_PROMPT = "\x1b[96;40;2m"
    DRIVER_PROMPT = "\x1b[92;40;2m"
    WARNUNG_PROMPT = "\x1b[34;43;2m"
    ERROR_PROMPT = "\x1b[31;40;2m"
    ENDC = "\x1b[0m"


# ESC [ 0 m       # reset all (colors and brightness)
# ESC [ 1 m       # bright
# ESC [ 2 m       # dim (looks same as normal brightness)
# ESC [ 22 m      # normal brightness

# # FOREGROUND:
# ESC [ 30 m      # black
# ESC [ 31 m      # red
# ESC [ 32 m      # green
# ESC [ 33 m      # yellow
# ESC [ 34 m      # blue
# ESC [ 35 m      # magenta
# ESC [ 36 m      # cyan
# ESC [ 37 m      # white
# ESC [ 39 m      # reset

# # BACKGROUND
# ESC [ 40 m      # black
# ESC [ 41 m      # red
# ESC [ 42 m      # green
# ESC [ 43 m      # yellow
# ESC [ 44 m      # blue
# ESC [ 45 m      # magenta
# ESC [ 46 m      # cyan
# ESC [ 47 m      # white
# ESC [ 49 m      # reset

# # cursor positioning
# ESC [ y;x H     # position cursor at x across, y down
# ESC [ y;x f     # position cursor at x across, y down
# ESC [ n A       # move cursor n lines up
# ESC [ n B       # move cursor n lines down
# ESC [ n C       # move cursor n characters forward
# ESC [ n D       # move cursor n characters backward

# # clear the screen
# ESC [ mode J    # clear the screen

# # clear the line
# ESC [ mode K    # clear the line

# ESC [ 36 ; 45 ; 1 m     # bright cyan text on magenta background
