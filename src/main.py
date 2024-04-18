import sys, warnings
from PyQt5 import QtWidgets, QtCore, QtGui
from src.util import config, loguru_config
from src import page
from loguru import logger as log

warnings.filterwarnings("ignore", category=DeprecationWarning)


class TransparentTextWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = "【按住右键横向滑动一段距离可退出】\n【按左键开始或恢复文本】\n【左键：下一页  右键：上一页】"
        self.initUI()

    def initUI(self):
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)  # 无边框且窗口置顶

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.text)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.setFont(QtGui.QFont('微软雅黑', config.font_size))
        self.label.setStyleSheet("color: white; background-color: rgba(255, 255, 255, 2);")
        self.label.setGeometry(0, 0, config.width, config.height)  # 设置标签覆盖整个窗口

        self.setGeometry(config.x, config.y, config.width, config.height)  # 设置窗口大小
        self.show()
        self.isDragging = False  # 用于判断是否在拖动
        self.isHidden = False

    def mousePressEvent(self, event):
        self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
        self.mouseTravelledPosition = event.globalPos()
        self.isDragging = False  # 开始按下时假设不是拖拽操作，除非移动鼠标
        self.mouseTravelledX = 0

    def mouseMoveEvent(self, event):
        self.isDragging = True  # 鼠标移动时确定为拖拽操作
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
        # 自定义手势
        self.mouseTravelledX += abs((event.globalPos() - self.mouseTravelledPosition).x())
        self.mouseTravelledPosition = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if not self.isDragging:
                if not self.isHidden:
                    self.text = page.next_page()
                self.label.setText(self.text)  # 更新标签文本
                self.update()  # 手动触发重绘
                self.isHidden = False
            else:
                config.x = self.geometry().x()
                config.y = self.geometry().y()
                config.width = self.geometry().width()
                config.height = self.geometry().height()
                config.save_all()
        elif event.button() == QtCore.Qt.RightButton:
            if not self.isDragging:
                if not self.isHidden:
                    self.text = page.prev_page()
                self.label.setText(self.text)  # 更新标签文本
                self.update()  # 手动触发重绘
                self.isHidden = False
            else:
                # 自定义手势
                log.info(f"rightMouseReleaseEvent: mouseTravelled = {self.mouseTravelledX}")
                if self.mouseTravelledX > 300:
                    # self.close()
                    QtCore.QCoreApplication.instance().quit()

    def leaveEvent(self, event):
        self.label.setText("")
        self.update()
        self.isHidden = True

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        # 检查按下的键是否是Esc
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        # 检查按下的键是否是Enter
        elif (event.key() == QtCore.Qt.Key_Right or
              event.key() == QtCore.Qt.Key_D or
              event.key() == QtCore.Qt.Key_S
            ) and not self.isHidden:
            self.text = page.next_page()
            self.label.setText(self.text)  # 更新标签文本
            self.update()  # 手动触发重绘
        elif (event.key() == QtCore.Qt.Key_Left or
            event.key() == QtCore.Qt.Key_A or
            event.key() == QtCore.Qt.Key_W
            ) and not self.isHidden:
            self.text = page.prev_page()
            self.label.setText(self.text)  # 更新标签文本
            self.update()  # 手动触发重绘
        elif event.key() == QtCore.Qt.Key_Q and not self.isHidden:
            self.label.setText("")
            self.update()
            self.isHidden = True
        elif event.key() == QtCore.Qt.Key_E and self.isHidden:
            self.label.setText(self.text)  # 更新标签文本
            self.update()  # 手动触发重绘
            self.isHidden = False
        else:
            super().keyPressEvent(event)  # 对于其他键，调用基类的keyPressEvent方法

def start():
    loguru_config.setup_logger("HiddenReader")
    config.config_init()
    app = QtWidgets.QApplication(sys.argv)
    w = TransparentTextWindow()
    sys.exit(app.exec_())
