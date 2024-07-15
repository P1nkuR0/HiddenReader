import warnings
from PyQt5 import QtWidgets, QtCore, QtGui
from src.util import config, key_map, tk_util
from src import page
from loguru import logger as log

warnings.filterwarnings("ignore", category=DeprecationWarning)


class TransparentTextWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = "【按住右键横向滑动一段距离可退出】\n【按左键开始或恢复文本】\n【左键：下一页  右键：上一页】"
        self.initUI()
        page.init_page()
        key_map.key_config_init(config.conf_dict['key'])

    def initUI(self):
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)  # 无边框且窗口置顶

        self.label = QtWidgets.QLabel(self)
        self.label.setText(self.text)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.label.setFont(QtGui.QFont('微软雅黑', config.fontSize))
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
                    QtCore.QCoreApplication.instance().quit()

    def leaveEvent(self, event):
        self.label.setText("")
        self.update()
        self.isHidden = True

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        log.info(f"keyPressEvent: {event.key()}")
        if event.key() in key_map.qt_key_dict['exit']:
            QtCore.QCoreApplication.instance().quit()
        elif event.key() in key_map.qt_key_dict['nextPage'] and not self.isHidden:
            self.text = page.next_page()
            self.label.setText(self.text)  # 更新标签文本
            self.update()  # 手动触发重绘
        elif event.key() in key_map.qt_key_dict['prevPage'] and not self.isHidden:
            self.text = page.prev_page()
            self.label.setText(self.text)  # 更新标签文本
            self.update()  # 手动触发重绘
        elif event.key() in key_map.qt_key_dict['hide'] and not self.isHidden:
            self.label.setText("")
            self.update()
            self.isHidden = True
        elif event.key() in key_map.qt_key_dict['show'] and self.isHidden:
            self.label.setText(self.text)  # 更新标签文本
            self.update()  # 手动触发重绘
            self.isHidden = False
        elif event.key() in key_map.qt_key_dict['search'] and not self.isHidden:
            word = tk_util.get_user_input("请输入搜索内容:")
            if word is not None and len(word) > 0:
                self.text = page.search_word(word)
                self.label.setText(self.text)
                self.update()
                self.isHidden = False
        else:
            super().keyPressEvent(event)  # 对于其他键，调用基类的keyPressEvent方法