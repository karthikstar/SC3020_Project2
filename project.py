import sys
from PyQt6 import QtWidgets
from explore import get_database_names, LoginDetails, QueryDetails, retrieve_query_data, retrieve_aqp_data, \
    retrieve_content_for_block_no, AnnotatorHelper, retrieve_buffer_access_data, retrieve_block_access_count, \
    retrieve_other_stats
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

        login_ui = Login(self.login_details)  # Pass login details into Login class instance

        login_ui.setupUi(loginpage) # Helper function to set UI layouts
        loginpage.show() # Show login window
        program.exec() #Runs main event loop

        return login_ui.login_details # Returns the inputted login details to be updated in our Main class

    def load_main_page(self, db_list):
        """
        Start main program interface logic
        """
        program = QtWidgets.QApplication(sys.argv)
        main_page = QtWidgets.QWidget()
        main_ui = MainUI(self.login_details, db_list) # Assign main_ui to instance of MainUI class

        main_ui.setupUi(main_page) # Call class method to setup its UI
        main_page.show()
        program.exec()

    def main(self):
        """
        Main application logic controller
        """
        db_list = get_database_names(self.login_details) # Function returns list of database names

        # Load main page of app
        self.load_main_page(db_list)

    def get_qep_from_query(self, database, query):
        """
        Function called when user submits a query input.
        """
        # initialise
        query_details = QueryDetails
        query_details.database = database
        query_details.query = query

        #print(Main.get_content_in_specified_block(self, database, query, 10))
        # print(Main.get_other_stats(self, database, query))

        qep = retrieve_query_data(self.login_details, query_details) # Gets output from EXPLAIN function
        if qep is None:
            return "Query is not valid. Try again.", -1
        buffer_data = retrieve_buffer_access_data(self.login_details, query_details)
        qep_with_details = AnnotatorHelper().procedure_string(qep, buffer_data) # Helper function to get natural langauge of qep
        return str(qep_with_details), qep[0][0][0]['Plan']['Total Cost'] # Return natural lang + total cost info

    def get_aqp(self, perm_list, database, query):
        """
        Function called to get generated alternative query plans
        """
        # initialise
        querydetails = QueryDetails
        querydetails.database = database
        querydetails.query = query

        aqp = retrieve_aqp_data(self.login_details, querydetails, perm_list) # Passes in details and parameters list and get AQP Plan
        return aqp # Return this plan

    #Returns a dictionary {block 0 : count , block1: count.. } - this is the no. of the times each block got accsed for this query
    def get_block_access_data(self, database, query):
        # initialise
        querydetails = QueryDetails
        querydetails.database = database
        querydetails.query = query

        block_data = retrieve_block_access_count(self.login_details, querydetails)
        return block_data

    def get_total_block_access_count(self, database, query):
        # initialise
        querydetails = QueryDetails
        querydetails.database = database
        querydetails.query = query

        block_data = retrieve_block_access_count(self.login_details, querydetails)
        return sum(block_data.values())

    # Returns a dictionary with key:value where key is table name, and value is the table's content for the specified block
    def get_content_in_specified_block(self, database, query, block):
        # initialise
        querydetails = QueryDetails
        querydetails.database = database
        querydetails.query = query

        block_content = retrieve_content_for_block_no(self.login_details, querydetails, block)
        return block_content

    def get_other_stats(self, database, query):
        querydetails = QueryDetails
        querydetails.database = database
        querydetails.query = query

        other_stats = retrieve_other_stats(self.login_details, querydetails)
        return other_stats

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
