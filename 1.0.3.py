# activation.py
import sys
import os
import logging
from functools import partial
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QLabel, QGridLayout, QWidget, QMessageBox)
from PyQt6.QtCore import QProcess, pyqtSlot
import ctypes

from PyQt6.uic.properties import QtGui

# 配置日志系统
logging.basicConfig(
    filename='activation.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w',
    encoding='utf-8'
)


def resource_path(relative_path):
    """ 获取资源的绝对路径（适配打包环境） """
    try:
        # PyInstaller创建的临时文件夹路径
        base_path = sys._MEIPASS
    except AttributeError:
        # 开发环境路径
        base_path = os.path.abspath(".")

    # 处理路径分隔符和编码
    full_path = os.path.normpath(os.path.join(base_path, relative_path))
    # 处理中文路径编码问题
    try:
        return full_path.encode('utf-8').decode('utf-8')
    except UnicodeEncodeError:
        return full_path


class ActivationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 检查管理员权限
        self.check_admin_privileges()

        # 初始化界面
        self.init_ui()

        # 加载脚本配置
        self.script_mapping = self.load_scripts_config()

        logging.info("应用程序初始化完成")

    def check_admin_privileges(self):
        """ 检查管理员权限 """
        if sys.platform == 'win32':
            if not ctypes.windll.shell32.IsUserAnAdmin():
                QMessageBox.critical(
                    None,
                    "权限错误",
                    "请以管理员身份运行本程序！\n"
                    "右键点击程序图标，选择'以管理员身份运行'"
                )
                sys.exit(1)

    def init_ui(self):
        """ 初始化用户界面 """
        self.setWindowTitle("JetBrains全家桶激活工具 v3.0")
        self.setMinimumSize(800, 600)

        # 设置窗口图标
        icon_path = resource_path('jetbrains.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))
        else:
            logging.warning(f"图标文件未找到: {icon_path}")

        # 显示用户协议
        self.show_eula()

        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)

        # 状态标签
        self.status_label = QLabel("✅ 准备就绪 | 请选择需要激活的开发工具")
        self.layout.addWidget(self.status_label, 5, 0, 1, 2)

    def show_eula(self):
        """ 显示最终用户许可协议 """
        msg = QMessageBox()
        msg.setWindowTitle("用户协议")
        msg.setText("""
            <b>JetBrains 激活工具使用协议</b>
            <p>1. 本工具仅用于学习研究目的</p>
            <p>2. 禁止用于商业用途</p>
            <p>3. 使用后24小时内请自行删除</p>
            <p>4. 造成的一切后果由使用者承担</p>
        """)

        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.button(QMessageBox.StandardButton.Yes).setText("同意")

        # 在代码开头添加白名单提示
        QMessageBox.information(
            None,
            "安全提示",
            "请将本程序添加到杀毒软件白名单\n"
            "否则可能无法正常执行激活操作",
            QMessageBox.StandardButton.Ok
        )

        if msg.exec() == QMessageBox.StandardButton.No:
            sys.exit(0)

    def load_scripts_config(self):
        """ 动态加载脚本配置 """
        script_names = [
            "CLion", "DataGrip", "GoLand", "IDEA",
            "PhpStorm", "PyCharm", "Rider", "WebStorm"
        ]

        script_mapping = {}
        for name in script_names:
            script_file = f"{name}激活.vbs"
            script_path = resource_path(os.path.join("scripts", script_file))
            script_mapping[name] = script_path
            logging.debug(f"加载脚本: {name} -> {script_path}")

        return script_mapping

    def create_activation_buttons(self):
        """ 创建带状态检测的激活按钮 """
        row, col = 0, 0
        for ide_name, script_path in self.script_mapping.items():
            btn = QPushButton(ide_name, self)
            btn.setMinimumSize(180, 60)
            btn.setToolTip(f"点击激活 {ide_name}")

            # 设置按钮状态
            if self.check_script_valid(script_path):
                btn.clicked.connect(partial(self.execute_activation, script_path))
                btn.setStyleSheet("QPushButton:hover { background-color: #e6f3ff; }")
            else:
                btn.setEnabled(False)
                btn.setText(f"{ide_name} (缺失)")
                btn.setStyleSheet("""
                    QPushButton { 
                        background-color: #ffe6e6;
                        color: #666;
                    }
                """)
                logging.error(f"脚本文件缺失: {script_path}")

            self.layout.addWidget(btn, row, col)

            # 更新网格位置
            col = (col + 1) % 2
            if col == 0:
                row += 1

    def check_script_valid(self, path):
        """ 增强型脚本验证 """
        try:
            if not os.path.exists(path):
                logging.warning(f"文件不存在: {path}")
                return False

            if not path.lower().endswith('.vbs'):
                logging.warning(f"非VBS脚本文件: {path}")
                return False

            return True
        except Exception as e:
            logging.error(f"脚本验证失败: {str(e)}")
            return False

    @pyqtSlot(str)
    def execute_activation(self, script_path):
        """ 执行激活操作 """
        if not self.check_script_valid(script_path):
            QMessageBox.critical(
                self,
                "文件错误",
                f"无效的脚本文件路径：\n{script_path}",
                QMessageBox.StandardButton.Ok
            )
            return

        ide_name = os.path.basename(script_path).split('激活')[0]
        self.status_label.setText(f"🔄 正在激活 {ide_name}...")
        QApplication.processEvents()

        try:
            process = QProcess(self)
            process.finished.connect(
                lambda exit_code, status: self.handle_activation_result(exit_code, ide_name)
            )

            # 使用明确的路径执行
            process.start("wscript.exe", [script_path])
            logging.info(f"启动进程: wscript.exe {script_path}")

        except Exception as e:
            logging.error(f"进程启动失败: {str(e)}")
            QMessageBox.critical(
                self,
                "运行时错误",
                f"无法执行脚本：\n{str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def handle_activation_result(self, exit_code, ide_name):
        """ 处理激活结果 """
        if exit_code == 0:
            msg = f"{ide_name} 激活成功！"
            self.status_label.setText(f"✅ {msg}")
            QMessageBox.information(self, "成功", msg)
            logging.info(msg)
        else:
            error_msg = f"{ide_name} 激活失败 (错误码: {exit_code})"
            self.status_label.setText(f"❌ {error_msg}")
            QMessageBox.critical(
                self,
                "错误",
                f"{error_msg}\n建议操作：\n1. 关闭杀毒软件\n2. 检查网络连接\n3. 重新尝试",
                QMessageBox.StandardButton.Ok
            )
            logging.error(error_msg)


if __name__ == "__main__":
    # 配置高DPI支持
    if sys.platform == 'win32':
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

    app = QApplication(sys.argv)
    window = ActivationApp()

    # 延迟加载按钮以确保资源初始化完成
    window.create_activation_buttons()
    window.show()

    sys.exit(app.exec())
