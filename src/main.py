import sys
from PyQt5 import QtWidgets
from src.util import config, loguru_config
from src.window import TransparentTextWindow

def start():
    loguru_config.setup_logger("HiddenReader")
    config.config_init()
    app = QtWidgets.QApplication(sys.argv)
    w = TransparentTextWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    start()