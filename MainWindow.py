from DataHandler import DataHandler
from logConfig import logger
from EventDialog import AddContactDialog
from EventDialog import DelContactDialog
from EventDialog import FindContactDialog
from EventDialog import UpdateContactDialog
from EventDialog import ShowContactDialog

import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc


class MainWindow(qtw.QMainWindow):
    contactChanged = qtc.pyqtSignal()

    def __init__(self, dataPath: str):
        super().__init__()

        self.dataHandler = DataHandler(dataPath)
        self.setWindowTitle("通讯录")
        self.setCentralWidget(qtw.QWidget())
        self.layout = qtw.QVBoxLayout()
        self.centralWidget().setLayout(self.layout)

        self.layout.addWidget(self.mkToolBar())

        self.contactTable = self.mkContactTable() if len(
            self.dataHandler.addressbook) > 0 else self.mkEmptyContact()
        self.layout.addWidget(self.contactTable)
        self.contactChanged.connect(self.updateContactTable)

        self.setFixedSize(460, 600)

    def mkEmptyContact(self) -> qtw.QTextEdit:
        text = qtw.QTextEdit()
        text.setPlainText("通讯录为空")
        text.setReadOnly(True)
        text.setAlignment(qtc.Qt.AlignmentFlag.AlignCenter)
        text.setStyleSheet("""QTextEdit {
            font-size: 20px;
            font-weight: bold;
        }""")
        return text

    def mkContactTable(self) -> qtw.QTableWidget:
        tableWidget = qtw.QTableWidget()
        tableWidget.setColumnCount(4)
        tableWidget.setHorizontalHeaderLabels(
            ["姓名", "电话", "信息", "操作"])

        # 设置表格无法选中
        tableWidget.setSelectionMode(
            qtw.QAbstractItemView.SelectionMode.NoSelection)
        tableWidget.setSelectionBehavior(
            qtw.QAbstractItemView.SelectionBehavior.SelectItems)

        contacts = self.dataHandler.getContacts()
        tableWidget.setRowCount(len(contacts))

        for row, contact in enumerate(contacts):
            nameItem = qtw.QTableWidgetItem(contact.name)
            phoneItem = qtw.QTableWidgetItem(contact.phone)
            infoItem = qtw.QTableWidgetItem(contact.info)

            # 设置单元格为不可编辑
            nameItem.setFlags(nameItem.flags() & ~
                              qtc.Qt.ItemFlag.ItemIsEditable)
            phoneItem.setFlags(phoneItem.flags() & ~
                               qtc.Qt.ItemFlag.ItemIsEditable)
            infoItem.setFlags(infoItem.flags() & ~
                              qtc.Qt.ItemFlag.ItemIsEditable)

            tableWidget.setItem(row, 0, nameItem)
            tableWidget.setItem(row, 1, phoneItem)
            tableWidget.setItem(row, 2, infoItem)

            button = qtw.QPushButton("查看")
            button.clicked.connect(lambda _, r=row: self.showContact(r))
            tableWidget.setCellWidget(row, 3, button)

        return tableWidget

    def updateContactTable(self):
        self.layout.removeWidget(self.contactTable)
        self.contactTable = self.mkContactTable() if len(
            self.dataHandler.addressbook) > 0 else self.mkEmptyContact()
        self.layout.addWidget(self.contactTable)

    def showContact(self, row: int):
        contact = self.dataHandler.getContacts()[row]
        dialog = ShowContactDialog(contact=contact, mainWindow=self)
        dialog.exec()

    def addContact(self):
        logger.info("添加联系人")

        dialog = AddContactDialog()
        if dialog.exec() == qtw.QDialog.DialogCode.Rejected:
            logger.info("取消添加联系人")
            return
        try:
            contact = dialog.getContact()
            self.dataHandler.addContact(contact)
            self.contactChanged.emit()
            logger.info("添加联系人成功: %s", contact)
        except ValueError:
            logger.error("添加联系人失败")
            # 弹出错误对话框
            qtw.QMessageBox.critical(self, "错误", "联系人已存在")

    def delContact(self):
        logger.info("删除联系人")

        dialog = DelContactDialog()
        if dialog.exec() == qtw.QDialog.DialogCode.Rejected:
            logger.info("取消删除联系人")
            return
        try:
            name = dialog.getContact()
            self.dataHandler.removeContact(name)
            self.contactChanged.emit()
            logger.info("删除联系人成功: %s", name)
        except ValueError:
            logger.error("删除联系人失败")
            # 弹出错误对话框
            qtw.QMessageBox.critical(self, "错误", "联系人不存在")

    def findContact(self):
        logger.info("查找联系人")

        dialog = FindContactDialog()
        if dialog.exec() == qtw.QDialog.DialogCode.Rejected:
            logger.info("取消查找联系人")
            return
        try:
            name = dialog.getContact()
            contact = self.dataHandler.getContact(name)
            logger.info("查找联系人成功: %s", contact)
            dialog = ShowContactDialog(contact=contact, mainWindow=self)
            dialog.exec()
        except ValueError:
            logger.error("查找联系人失败")
            # 弹出错误对话框
            qtw.QMessageBox.critical(self, "错误", "联系人不存在")

    def updateContact(self):
        logger.info("更新联系人")

        dialog = UpdateContactDialog()
        if dialog.exec() == qtw.QDialog.DialogCode.Rejected:
            logger.info("取消更新联系人")
            return
        try:
            name, contact = dialog.getContact()
            self.dataHandler.updateContact(name, contact)
            self.contactChanged.emit()
            logger.info("更新联系人成功: %s", contact)
        except ValueError:
            # 弹出错误对话框
            qtw.QMessageBox.warning(self, "警告", "联系人不存在，将添加新联系人")
            contact = dialog.getContact()
            self.dataHandler.addContact(contact)
            self.contactChanged.emit()
            logger.info("添加联系人成功: %s", contact)

    def mkToolBar(self) -> qtw.QToolBar:
        toolBar = qtw.QToolBar()
        toolBar.addAction("添加联系人", self.addContact)
        toolBar.addAction("删除联系人", self.delContact)
        toolBar.addAction("查找联系人", self.findContact)
        toolBar.addAction("更新联系人", self.updateContact)
        return toolBar
