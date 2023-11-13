import sys
from PyQt6 import QtWidgets

class Main:
    def __init__(self):
        self.login_details = LoginDetails
        self.login_details.host = "localhost"
        self.login_details.port = "5433"
        self.login_details.user = "postgres"
        self.login_details.password = ""
        self.login_details = self.login()

    def login(self):
        """
        Show login interface
        """
        program = QtWidgets.QApplication(sys.argv)
        loginpage = QtWidgets.QWidget()
        login_ui = Login(self.login_details)

        login_ui.setupUi(loginpage)
        loginpage.show()
        program.exec()

        return login_ui.login_details

    def load_main_page(self, db_list):
        """
        Start main program interface logic
        """
        program = QtWidgets.QApplication(sys.argv)
        main_page = QtWidgets.QWidget()
        main_ui = MainUI(self.login_details, db_list)

        main_ui.setupUi(main_page)
        main_page.show()
        program.exec()

    def main(self):
        """
        Main application logic controller
        """
        # Connect to db using login details
        db_list = get_dbs(self.login_details)

        # Obtain chosen database information & awaits user input
        self.load_main_page(db_list)

    # Standard error static method to be called throughout the 3 files
    @staticmethod
    def show_error(msg):
        """
        Show error dialog
        """
        program = QtWidgets.QApplication(sys.argv)
        errordialog = QtWidgets.QWidget()
        error_ui = Error(msg)
        error_ui.setupUi(errordialog)

        errordialog.show()
        program.exec()
