import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QMainWindow, QLineEdit, QWidget, QListWidgetItem
from PyQt5.uic import loadUi

from connection import Data

class LoginApp(QMainWindow):
    def __init__(self):
        super(LoginApp, self).__init__()
        loadUi('pyqt5/budget_tracker/ui/AuthWindow.ui', self)

        self.show()

        self.conn = Data()
        self.reg_window = RegistrApp()
        self.dashboard_window = DashboardApp()

        self.btnToSignUp.clicked.connect(self.to_registr_window)
        self.btnLogin.clicked.connect(self.login)

    def to_registr_window(self):
        self.reg_window.show()
        self.hide()

    def login(self):
        log_email = self.emailTxtEdit.text()
        log_pswrd = self.pswrdTxtEdit.text()

        user = self.conn.get_user(log_email, log_pswrd)

        if user:
            current_user_info = self.conn.get_user_id(log_email, log_pswrd)

            with open('pyqt5/budget_tracker/current_user_info.txt', 'w') as file:
                file.write(str(current_user_info))
            
            self.dashboard_window.show()
            self.close()

            self.dashboard_window.txtUsername.setText(str(current_user_info[1]))
            QMessageBox.information(self, 'Login form', 'You succesfully logined')
        else:
            QMessageBox.information(self, 'Login form', "Doesn't exist")
            self.to_registr_window()

class RegistrApp(QMainWindow):
    def __init__(self):
        super(RegistrApp, self).__init__()
        loadUi('pyqt5/budget_tracker/ui/RegWindow.ui', self)

        self.conn = Data()

        self.btnToLogin.clicked.connect(self.to_login)
        self.btnToDashboard.clicked.connect(self.registr_user)

    def to_login(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.hide()

    def registr_user(self):
        u_email = self.txtEditEmailReg.text()
        u_username = self.txtEditNameReg.text()
        u_password = self.txtEditPswrdReg.text()
        flag = True

        # проверка валидации
        if '@' not in u_email and '.' not in u_email:
            self.txtEmailValidation.setText('Enter correctly email')
            flag = False

        if len(u_username) < 2:
            self.txtNameValidation.setText('Enter more then 2 letters')
            flag = False

        if len(u_password) < 6:
            self.txtPswrdValidation.setText('Must be more than 6 characters')
            flag = False

        if flag:
            res = self.conn.get_user(u_email, u_password)

            if res:
                QMessageBox.information(self, 'Registr form', 'User already registered')
                self.txtEditEmailReg.setText('')
                self.txtEditNameReg.setText('')
                self.txtEditPswrdReg.setText('')
            else:
                self.conn.add_new_user(u_email, u_username, u_password)
                QMessageBox.information(self, "Registr form", "Gongratulations! You succesfully registered.")

                self.to_login()

class DashboardApp(QMainWindow):
    def __init__(self):
        super(DashboardApp, self).__init__()
        loadUi('pyqt5/budget_tracker/ui/DashboardWindow.ui', self)

        self.conn = Data()
        self.transaction_dialog = NewTransaction()

        self.btnToExpence.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btnToIncomes.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btnLogOut.clicked.connect(self.log_out)

        self.btnAddIncome.clicked.connect(self.add_new_income_transaction)
        self.btnAddExpence.clicked.connect(self.add_new_expence_transaction)

        self.btnNewCategory.clicked.connect(self.add_new_category)
        self.btnNewCategoryIncome.clicked.connect(self.add_new_category)

    def log_out(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()

    def add_new_income_transaction(self):
        self.transaction_dialog.show()
        self.transaction_dialog.label.setText('Income')

    def add_new_expence_transaction(self):
        self.transaction_dialog.show()
        self.transaction_dialog.label.setText('Expence')

    def add_new_category(self):
        self.category_dialog = NewCategory()
        self.category_dialog.show()

class NewTransaction(QDialog):
    def __init__(self):
        super(NewTransaction, self).__init__()
        loadUi('pyqt5/budget_tracker/ui/NewTransactionDialog.ui', self)

        self.conn = Data()

        self.update_category_list()

    def update_category_list(self):
        with open('pyqt5/budget_tracker/current_user_info.txt', 'r') as file:
            user_info = file.read()
        user_id = list(user_info)

        results = self.conn.get_all_expence_categories(user_id[1])

        for result in results:
            item = ''.join(result)
            self.comboBox.addItem(item)

    def add_new_transaction(self):
        pass


class NewCategory(QDialog):
    def __init__(self):
        super(NewCategory, self).__init__()
        loadUi('pyqt5/budget_tracker/ui/NewCategoryDialog.ui', self)

        self.conn = Data()

        self.btnSaveNewCategory.clicked.connect(self.save_new_category)

    def get_category_type(self):
        if self.radioBtnExpence.isChecked():
            return 'Expence'
        if self.radioBtnIncome.isChecked():
            return 'Income'

    def save_new_category(self):
        with open('pyqt5/budget_tracker/current_user_info.txt', 'r') as file:
            user_info = file.read()

        user_id = list(user_info)

        category = self.txtEdit.text()
        c_type = self.get_category_type()
        self.conn.add_new_category(category, c_type, user_id[1])
        self.txtEdit.setText('')
        self.txtSaved.setText('Category succesfully saved!')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())