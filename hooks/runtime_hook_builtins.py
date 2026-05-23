import builtins
import sys

# PyInstaller frozen bundles don't include the 'site' module that provides
# exit() and quit() as builtins. flet/utils/pip.py calls exit(1) on failure,
# so we inject it here before any app code runs.
if not hasattr(builtins, "exit"):
    builtins.exit = sys.exit
if not hasattr(builtins, "quit"):
    builtins.quit = sys.exit
