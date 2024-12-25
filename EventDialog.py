from ContactPerson import ContactPerson
from logConfig import logger

import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg


class PhoneValidator(qtg.QValidator):
    def validate(self, input: str, pos: int):
        if input.isdigit() and not input.startswith("-") or input == "":
            return qtg.QValidator.State.Acceptable, input, pos
        return qtg.QValidator.State.Invalid, input, pos


class AddContactDialog(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加联系人")
        self.layout = qtw.QFormLayout()
        self.setLayout(self.layout)

        self.name = qtw.QLineEdit()
        self.phone = qtw.QLineEdit()
        self.info = qtw.QLineEdit()
        self.phone.setValidator(PhoneValidator())

        self.layout.addRow("姓名", self.name)
        self.layout.addRow("电话", self.phone)
        self.layout.addRow("信息", self.info)

        self.buttonBox = qtw.QDialogButtonBox()
        self.okButton = self.buttonBox.addButton(
            qtw.QDialogButtonBox.StandardButton.Ok)
        self.cancelButton = self.buttonBox.addButton(
            qtw.QDialogButtonBox.StandardButton.Cancel)
        self.deleteButton = qtw.QPushButton("删除")

        self.buttonBox.addButton(
            self.deleteButton, qtw.QDialogButtonBox.ButtonRole.ActionRole)

        self.layout.addWidget(self.buttonBox)

        self.okButton.clicked.connect(self.validate)
        self.cancelButton.clicked.connect(self.reject)
        self.buttonBox.rejected.connect(self.reject)

    def validate(self):
        if all([self.name.text(), self.phone.text()]):
            self.accept()
        else:
            qtw.QMessageBox.critical(
                self, "警告", "姓名和电话不能为空",
                qtw.QMessageBox.StandardButton.Ok)

    def getContact(self) -> ContactPerson:
        return ContactPerson(
            name=self.name.text(),
            phone=self.phone.text(),
            info=self.info.text(),
        )


class DelContactDialog(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("删除联系人")
        self.layout = qtw.QFormLayout()
        self.setLayout(self.layout)

        self.name = qtw.QLineEdit()
        self.layout.addRow("姓名", self.name)

        self.buttonBox = qtw.QDialogButtonBox(
            qtw.QDialogButtonBox.StandardButton.Ok |
            qtw.QDialogButtonBox.StandardButton.Cancel)
        self.layout.addRow(self.buttonBox)

        self.buttonBox.accepted.connect(self.validate)
        self.buttonBox.rejected.connect(self.reject)

    def validate(self):
        if self.name.text():
            self.accept()
        else:
            qtw.QMessageBox.critical(
                self, "警告", "姓名不能为空",
                qtw.QMessageBox.StandardButton.Ok)

    def getContact(self) -> str:
        return self.name.text()


class FindContactDialog(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("查找联系人")
        self.layout = qtw.QFormLayout()
        self.setLayout(self.layout)

        self.name = qtw.QLineEdit()
        self.layout.addRow("姓名", self.name)

        self.buttonBox = qtw.QDialogButtonBox(
            qtw.QDialogButtonBox.StandardButton.Ok |
            qtw.QDialogButtonBox.StandardButton.Cancel)
        self.layout.addRow(self.buttonBox)

        self.buttonBox.accepted.connect(self.validate)
        self.buttonBox.rejected.connect(self.reject)

    def validate(self):
        if self.name.text():
            self.accept()
        else:
            qtw.QMessageBox.critical(
                self, "警告", "姓名不能为空",
                qtw.QMessageBox.StandardButton.Ok)

    def getContact(self) -> str:
        return self.name.text()


class UpdateContactDialog(qtw.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("更新联系人")
        self.layout = qtw.QFormLayout()
        self.setLayout(self.layout)

        self.name = qtw.QLineEdit()
        self.phone = qtw.QLineEdit()
        self.info = qtw.QLineEdit()
        self.phone.setValidator(PhoneValidator())

        self.layout.addRow("姓名", self.name)
        self.layout.addRow("电话", self.phone)
        self.layout.addRow("信息", self.info)

        self.buttonBox = qtw.QDialogButtonBox(
            qtw.QDialogButtonBox.StandardButton.Ok |
            qtw.QDialogButtonBox.StandardButton.Cancel)
        self.layout.addRow(self.buttonBox)

        self.buttonBox.accepted.connect(self.validate)
        self.buttonBox.rejected.connect(self.reject)

    def validate(self):
        if all([self.name.text(), self.phone.text()]):
            self.accept()
        else:
            qtw.QMessageBox.critical(
                self, "警告", "姓名和电话不能为空",
                qtw.QMessageBox.StandardButton.Ok)

    def getContact(self) -> ContactPerson:
        return ContactPerson(
            name=self.name.text(),
            phone=self.phone.text(),
            info=self.info.text(),
        )


class ShowContactDialog(qtw.QDialog):
    def __init__(self, contact: ContactPerson, mainWindow, parent=None):
        super().__init__(parent)

        self.mainWindow = mainWindow
        self.preContact = contact
        self.setWindowTitle("联系人信息")
        self.layout = qtw.QFormLayout()
        self.setLayout(self.layout)

        self.name = qtw.QLineEdit()
        self.phone = qtw.QLineEdit()
        self.info = qtw.QLineEdit()

        self.name.setText(contact.name)
        self.phone.setText(contact.phone)
        self.info.setText(contact.info)
        self.phone.setValidator(PhoneValidator())

        self.layout.addRow("姓名", self.name)
        self.layout.addRow("电话", self.phone)
        self.layout.addRow("信息", self.info)

        self.buttonBox = qtw.QDialogButtonBox()
        self.okButton = self.buttonBox.addButton(
            qtw.QDialogButtonBox.StandardButton.Ok)
        self.deleteButton = qtw.QPushButton("删除")
        self.buttonBox.addButton(
            self.deleteButton, qtw.QDialogButtonBox.ButtonRole.ActionRole)
        self.deleteButton.clicked.connect(self.deleteContact)
        self.cancelButton = self.buttonBox.addButton(
            qtw.QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.validate)
        self.buttonBox.rejected.connect(self.reject)

    def getContact(self) -> ContactPerson:
        return ContactPerson(
            name=self.name.text(),
            phone=self.phone.text(),
            info=self.info.text(),
        )

    def validate(self):
        if not all([self.name.text(), self.phone.text()]):
            qtw.QMessageBox.critical(
                self, "警告", "姓名和电话不能为空",
                qtw.QMessageBox.StandardButton.Ok)
            return
        nowContact = self.getContact()
        if nowContact != self.preContact:
            if nowContact.name != self.preContact.name:
                if self.mainWindow.dataHandler.existContact(nowContact.name):
                    qtw.QMessageBox.critical(
                        self, "错误", "联系人已存在",
                        qtw.QMessageBox.StandardButton.Ok)
                    return
                self.mainWindow.dataHandler.removeContact(self.preContact.name)
                self.mainWindow.dataHandler.addContact(nowContact)
            else:
                self.mainWindow.dataHandler.updateContact(
                    self.preContact.name, nowContact)
            self.mainWindow.contactChanged.emit()
            logger.info("更新联系人成功: %s -> %s", self.preContact, nowContact)
        self.accept()

    def deleteContact(self):
        logger.info("删除联系人")

        self.mainWindow.dataHandler.removeContact(self.preContact.name)
        self.mainWindow.contactChanged.emit()
        logger.info("删除联系人成功: %s", self.preContact)
        self.accept()
