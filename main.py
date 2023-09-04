import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QMainWindow, QLineEdit, QWidget, QListWidgetItem, QCalendarWidget
from PyQt5.uic import loadUi

from connection import Data

class LoginApp(QMainWindow):
    def __init__(self):
        super(LoginApp, self).__init__()
        loadUi('ui/AuthWindow.ui', self)

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

            with open('current_user_info.txt', 'w') as file:
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
        loadUi('ui/RegWindow.ui', self)

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
        loadUi('ui/DashboardWindow.ui', self)

        self.conn = Data()
        self.transaction_dialog = NewTransaction()

        self.btnToExpence.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btnToIncomes.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btnTransactions.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btnTransactions.clicked.connect(self.load_all_transactions)

        #self.load_all_transactions()

        self.btnLogOut.clicked.connect(self.log_out)

        self.btnAddIncome.clicked.connect(self.add_new_transaction)
        self.btnAddExpence.clicked.connect(self.add_new_transaction)

        self.btnNewCategory.clicked.connect(self.add_new_category)
        self.btnNewCategoryIncome.clicked.connect(self.add_new_category)

    def log_out(self):
        self.login_window = LoginApp()
        self.login_window.show()
        self.close()

    def add_new_transaction(self):
        self.transaction_dialog.show()

    def add_new_category(self):
        self.category_dialog = NewCategory()
        self.category_dialog.show()

    def load_all_transactions(self):
        # задаю размеры хэдеров
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 70)
        self.tableWidget.setColumnWidth(2, 50)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 70)
        self.tableWidget.setColumnWidth(5, 50)
        self.tableWidget.setColumnWidth(6, 90)

        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Type', 'Sum', 'Comment', 'Date', 'User ID', 'Category ID'])
        
        with open('current_user_info.txt', 'r') as file:
            user_info = file.read()
        user_id = list(user_info)

        all_transactions_db = self.conn.get_all_transactions(user_id[1])

        self.tableWidget.setRowCount(25)
        table_row = 0
        for row in all_transactions_db:
            self.tableWidget.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(table_row, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(table_row, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tableWidget.setItem(table_row, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(table_row, 4, QtWidgets.QTableWidgetItem(row[4]))
            self.tableWidget.setItem(table_row, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.tableWidget.setItem(table_row, 6, QtWidgets.QTableWidgetItem(str(row[6])))

            table_row += 1

class NewTransaction(QDialog):
    def __init__(self):
        super(NewTransaction, self).__init__()
        loadUi('ui/NewTransactionDialog.ui', self)

        self.conn = Data()

        self.radioBtnExpenceTr.toggled.connect(self.update_expence_categories)
        self.radioBtnIncomeTr.toggled.connect(self.update_income_categories)

        self.btnSaveTransaction.clicked.connect(self.save_new_transaction)

    def update_expence_categories(self):
        self.comboBox.clear()
        with open('current_user_info.txt', 'r') as file:
            user_info = file.read()
        user_id = list(user_info)

        results = self.conn.get_all_expence_categories(user_id[1])

        for result in results:
            item = ''.join(result)
            self.comboBox.addItem(item)

    def update_income_categories(self):
        self.comboBox.clear()
        with open('current_user_info.txt', 'r') as file:
            user_info = file.read()
        user_id = list(user_info)

        results = self.conn.get_all_income_categories(user_id[1])

        for result in results:
            item = ''.join(result)
            self.comboBox.addItem(item)

    def get_category_type_tr(self):
        if self.radioBtnExpenceTr.isChecked():
            return 'Expence'
        if self.radioBtnIncomeTr.isChecked():
            return 'Income'

    def save_new_transaction(self):
        type_tr = self.get_category_type_tr()
        summ = self.txtEditSum.text()
        comment = self.txtEditComment.text()
        date = self.dateEdit.date().toPyDate()

        with open('current_user_info.txt', 'r') as file:
            user_info = file.read()

        user_id = list(user_info)

        category_tittle = self.comboBox.currentText()
        category_id = self.conn.get_category_id(category_tittle, type_tr, user_id[1])

        self.conn.add_new_transaction(type_tr, summ, comment, str(date), user_id[1], category_id)

        print(type_tr, summ, comment, date, user_id[1], category_id)


class NewCategory(QDialog):
    def __init__(self):
        super(NewCategory, self).__init__()
        loadUi('ui/NewCategoryDialog.ui', self)

        self.conn = Data()

        self.btnSaveNewCategory.clicked.connect(self.save_new_category)

    def get_category_type(self):
        if self.radioBtnExpence.isChecked():
            return 'Expence'
        if self.radioBtnIncome.isChecked():
            return 'Income'

    def save_new_category(self):
        with open('current_user_info.txt', 'r') as file:
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