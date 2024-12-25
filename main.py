from MainWindow import MainWindow

import PyQt6.QtWidgets as qtw
import sys


def main():
    app = qtw.QApplication(sys.argv)
    window = MainWindow("addressbook.json")
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
