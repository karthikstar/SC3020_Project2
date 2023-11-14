import sys
from PyQt6 import QtWidgets
from explore import get_database_names, LoginDetails, QueryDetails, retrieve_query_data, retrieve_aqp_data, AnnotatorHelper
from interface import Login, Error, MainUI


class Main:
    def __init__(self):
        self.login_details = LoginDetails
        self.login_details.host = "localhost"
        self.login_details.port = "5433"
        self.login_details.user = "postgres"
        self.login_details.password = "postgres"
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
        db_list = get_database_names(self.login_details)

        # Obtain chosen database information & awaits user input
        self.load_main_page(db_list)

    def get_qep_from_query(self, database, query):
        """
        Function called when user submits a query input.
        """
        query_details = QueryDetails
        query_details.database = database
        query_details.query = query

        qep = retrieve_query_data(self.login_details, query_details)
        if qep is None:
            return "Query is not valid. Try again.", -1
        qep_with_details = AnnotatorHelper().procedure_string(qep)
        return str(qep_with_details), qep[0][0][0]['Plan']['Total Cost']

    def get_aqp(self, perm_list, database, query):
        """
        Function called to get generated alternative query plans
        """
        querydetails = QueryDetails
        querydetails.database = database
        querydetails.query = query

        aqp = retrieve_aqp_data(self.login_details, querydetails, perm_list)
        return aqp

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


if __name__ == '__main__':
    main = Main()
    main.main()
