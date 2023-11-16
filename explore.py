import numpy as np
import re
import interface
import psycopg2
import itertools
from typing import TypedDict, List


class LoginDetails(TypedDict):
    host: str
    port: int
    user: str
    password: str


class QueryDetails(TypedDict):
    database: str
    query: str


class DatabaseConnector(object):
    """
    psycopg2 connector to the postgresql database
    """

    def __init__(self, login_details: LoginDetails, databasename=None):
        if databasename is None:
            self.connector = psycopg2.connect(host=login_details.host, port=login_details.port,
                                              user=login_details.user, password=login_details.password).cursor()
        else:
            self.connector = psycopg2.connect(host=login_details.host, port=login_details.port,
                                              user=login_details.user, password=login_details.password,
                                              dbname=databasename).cursor()

    def __enter__(self):
        return self.connector

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connector.close()


class AnnotatorHelper:
    def __init__(self):
        self.tablenumber = 0
        self.stepnumber = 0

    def procedure_string(self, qep, buffer_data):
        processingsteps = self.extract_natural_language(qep[0][0][0]['Plan'], True, buffer_data)[1]
        processingsteps = processingsteps[:-3]
        processingsteps += " and output our final results!"
        return processingsteps

    def extract_natural_language(self, query, first_run, buffer_data):
        joined_tables_list = []
        procedure = ""

        if "Plans" in query:
            for plan in query["Plans"]:
                temp = self.extract_natural_language(plan, False, buffer_data)
                joined_tables_list.append(temp[0])
                procedure += temp[1]

        self.stepnumber += 1
        procedure += "{}. ".format(self.stepnumber)

        if query["Node Type"] == 'Seq Scan':
            table = query["Relation Name"]
            name = query["Alias"]
            line_description = "Conduct SEQUENTIAL SCAN on table '{}' as '{}'".format(table, name)
            if "Filter" in query:
                line_description += " under the condition {}".format(query["Filter"])
            line_description += ". ------ Buffer Shared Hits = {}".format(buffer_data['Seq Scan'])
            line_description += "\n"
            return table, procedure + line_description

        elif query["Node Type"] == 'Index-Only Scan':
            table = query["Relation Name"]
            name = query["Alias"]
            line_description = "Conduct INDEX SCAN on table '{}' as '{}' using the index on '{}'".format(table, name,
                                                                                                         query[
                                                                                                             "Index Name"])
            if "Index Cond" in query:
                line_description += " for {}".format(query["Index Cond"])
            if "Filter" in query:
                line_description += " under the condition {}".format(query["Filter"])
            line_description += ". ------ Buffer Shared Hits = {}".format(buffer_data['Index-Only Scan'])
            line_description += "\n"
            return table, procedure + line_description

        elif query["Node Type"] == 'Index Scan':
            table = query["Relation Name"]
            name = query["Alias"]
            line_description = "Conduct INDEX SCAN on table '{}' as '{}' using the index on '{}'".format(table, name,
                                                                                                         query[
                                                                                                             "Index Name"])
            if "Index Cond" in query:
                line_description += " for {}".format(query["Index Cond"])
            if "Filter" in query:
                line_description += " under the condition {}".format(query["Filter"])
            line_description += ". ------ Buffer Shared Hits = {}".format(buffer_data['Index Scan'])
            line_description += "\n"
            return table, procedure + line_description

        elif query["Node Type"] == 'Foreign Scan':
            table = query["Relation Name"]
            name = query["Alias"]
            line_description = "Conduct FOREIGN SCAN on table '{}' from schema '{}' as '{}'. \n".format(table,
                                                                                                        query["Schema"],
                                                                                                        name)
            return table, procedure + line_description

        elif query["Node Type"] == 'CTE Scan':
            table = query["CTE Name"]
            name = query["Alias"]
            line_description = "Conduct CTE SCAN on table '{}' as '{}'".format(table, name)
            if "Filter" in query:
                line_description += " under the condition that {}".format(query["Filter"])
            line_description += ". \n"
            return table, procedure + line_description

        elif query["Node Type"] == 'Function Scan':
            table = query["Schema"]
            name = query["alias"]
            line_description = "Conduct FUNCTION {} on schema '{}' and return the results in '{}'".format(
                query["Function Name"], table,
                name)
            if "Filter" in query:
                line_description += " under the condition that {}".format(query["Filter"])
            line_description += ". \n"
            return table, procedure + line_description

        elif query["Node Type"] == 'Subquery Scan':
            line_description = "The previous operation's subquery results are read"
            if "Filter" in query:
                line_description += " under the condition that {}".format(query["Filter"])
            line_description += ". \n"
            return joined_tables_list[0], procedure + line_description

        elif query["Node Type"] == 'Nested Loop':
            self.tablenumber += 1
            line_description = "Execute NESTED LOOP JOIN on tables '{}' and '{}'".format(joined_tables_list[0],
                                                                                         joined_tables_list[1])
            if "Join Filter" in query:
                line_description += " on join filter {}".format(joined_tables_list[0], joined_tables_list[1],
                                                                query["Join Filter"])
            if "Filter" in query:
                line_description += " under the condition that {}".format(query["Filter"])
            if not first_run:
                line_description += " to get intermediate table T{}. \n".format(self.tablenumber)
            else:
                line_description += ". \n"
            return "T" + str(self.tablenumber), procedure + line_description

        elif query["Node Type"] == 'TID Scan':
            table = query["Relation"]
            name = query["Alias"]
            line_description = "Execute a TUPLE ID SCAN on table '{}' as '{}'. \n".format(table, name)
            return table, procedure + line_description

        elif query["Node Type"] == 'Hash Join':
            self.tablenumber += 1
            line_description = "Execute a HASH JOIN on tables '{}' and '{}'".format(joined_tables_list[0],
                                                                                    joined_tables_list[1])
            if "Hash Cond" in query:
                line_description += " on hash condition {}".format(query["Hash Cond"])
            if "Filter" in query:
                line_description += " under the condition that {}".format(query["Filter"])
            if not first_run:
                line_description += " to get intermediate table T{}. \n".format(self.tablenumber)
            else:
                line_description += ". \n"
            return "T" + str(self.tablenumber), procedure + line_description

        elif query["Node Type"] == 'Merge Join':
            self.tablenumber += 1
            line_description = "Execute a MERGE JOIN on tables '{}' and '{}'".format(joined_tables_list[0],
                                                                                     joined_tables_list[1])
            if "Merge Cond" in query:
                line_description += " on merge condition {}".format(query["Merge Cond"])
            if "Filter" in query:
                line_description += " under the condition that {}".format(query["Filter"])
            line_description += ". \n"
            if not first_run:
                line_description += " to get intermediate table T{}. \n".format(self.tablenumber)
            else:
                line_description += ". \n"
            return "T" + str(self.tablenumber), procedure + line_description

        elif query["Node Type"] == 'Aggregate':
            self.tablenumber += 1
            line_description = "Execute AGGREGATE on table '{}'".format(joined_tables_list[0])
            if not first_run:
                line_description += " to get intermediate table T{}. \n".format(self.tablenumber)
            else:
                line_description += ". \n"
            return "T" + str(self.tablenumber), procedure + line_description

        elif query["Node Type"] == 'Gather':
            self.tablenumber += 1
            line_description = ("Execute GATHER on table '{}'".format(joined_tables_list[0]))
            if not first_run:
                line_description += " to get intermediate table T{}. \n".format(self.tablenumber)
            else:
                line_description += ". \n"
            return "T" + str(self.tablenumber), procedure + line_description

        elif query["Node Type"] == 'Append':
            self.tablenumber += 1
            line_description = "APPEND the results from table '{}' to table '{}'".format(joined_tables_list[0],
                                                                                         joined_tables_list[1])
            if not first_run:
                line_description += " to get intermediate table T{}. \n".format(self.tablenumber)
            else:
                line_description += ". \n"
            return "T" + str(self.tablenumber), procedure + line_description

        elif query["Node Type"] == 'Gather Merge':
            line_description = "Results of previous operation are GATHERED & MERGED. \n"
            return joined_tables_list[0], procedure + line_description

        elif query["Node Type"] == 'GroupAggregate':
            self.tablenumber += 1
            line_description = "Execute a GROUP AGGREGATE on table '{}'".format(joined_tables_list[0])
            if not first_run:
                line_description += " to get intermediate table T{}. \n".format(self.tablenumber)
            else:
                line_description += ". \n"
            return "T" + str(self.tablenumber), procedure + line_description

        elif query["Node Type"] == 'HashAggregate':
            self.tablenumber += 1
            line_description = "Execute a HASH AGGREGATE on table '{}'".format(joined_tables_list[0])
            if not first_run:
                line_description += " to get intermediate table T{}. \n".format(self.tablenumber)
            else:
                line_description += ". \n"
            return "T" + str(self.tablenumber), procedure + line_description

        elif query["Node Type"] == 'Hash':
            line_description = "Execute HASHING on table '{}'. \n".format(joined_tables_list[0])
            return joined_tables_list[0], procedure + line_description

        elif query["Node Type"] == 'Incremental Sort':
            line_description = "INCREMENTAL SORT is carried out on table '{}' with sort key {}. \n".format(
                joined_tables_list[0],
                query["Sort Key"])
            return joined_tables_list[0], procedure + line_description

        elif query["Node Type"] == 'Limit':
            line_description = "The indicated LIMIT on the number of rows is extracted from the table '{}'. \n".format(
                joined_tables_list[0])
            return joined_tables_list[0], procedure + line_description

        elif query["Node Type"] == 'Materialize':
            line_description = "MATERIALIZE table '{}'. \n".format(joined_tables_list[0])
            return joined_tables_list[0], procedure + line_description

        elif query["Node Type"] == 'ModifyTable':
            table = query["Relation Name"]
            line_description = "Table '{}' is MODIFIED. \n ".format(table)
            return table, procedure + line_description

        elif query["Node Type"] == 'MergeAppend':
            self.tablenumber += 1
            line_description = "Results from table '{}' are APPENDED to table '{}'".format(joined_tables_list[0],
                                                                                           joined_tables_list[1])
            if not first_run:
                line_description += " to get intermediate table T{}. \n".format(self.tablenumber)
            else:
                line_description += ". \n"
            return "T" + str(self.tablenumber), procedure + line_description

        elif query["Node Type"] == 'SetOp':
            self.tablenumber += 1
            line_description = "SET OPERATION carried out on table '{}'".format(joined_tables_list[0])
            if not first_run:
                line_description += " to get intermediate table T{}. \n".format(self.tablenumber)
            else:
                line_description += ". \n"
            return "T" + str(self.tablenumber), procedure + line_description

        elif query["Node Type"] == 'Sort':
            line_description = "Table '{}' is SORTED on sort key {}. \n".format(joined_tables_list[0],
                                                                                query["Sort Key"])
            return joined_tables_list[0], procedure + line_description

        elif query["Node Type"] == 'Unique':
            table = query["Subplan Name"] if "Subplan Name" in query else joined_tables_list[0]
            line_description = "DUPLICATE ELIMINATION is carried out on table '{}'. \n".format(table)
            return table, procedure + line_description

        else:
            line_description = "EXECUTE {}. \n".format(query["Node Type"])
            return joined_tables_list[0], procedure + line_description


def get_database_names(login_details: LoginDetails) -> List[str]:
    """
    Retrieve list of databases
    """
    try:
        with DatabaseConnector(login_details) as cursor:
            query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
            cursor.execute(query)
            database_list = cursor.fetchall()
            database_list = [i[0] for i in database_list]
            return database_list
    except psycopg2.OperationalError as e:
        from project import Main
        Main.show_error(str(e))


def get_tables_in_database(login_details: LoginDetails, db: str) -> List[str]:
    """
    Retrieve list of tables in specified database
    """
    try:
        with DatabaseConnector(login_details, db) as cursor:
            query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
            cursor.execute(query)
            table_list = cursor.fetchall()
            table_list = [i[0] for i in table_list]
            return table_list
    except psycopg2.OperationalError as e:
        from project import main
        main.show_error(str(e))


def get_columns_for_table(login_details: LoginDetails, db: str, schema: str) -> List[str]:
    """
    Retrieve list of columns in the chosen table.
    """
    try:
        with DatabaseConnector(login_details, db) as cursor:
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{schema}' AND table_catalog = '{db}';"
            cursor.execute(query)
            column_list = cursor.fetchall()
            column_list = [_[0] for _ in column_list]
            return column_list
    except psycopg2.OperationalError as e:
        from project import Main
        Main.show_error(str(e))


def retrieve_query_data(login_details: LoginDetails, querydetails: QueryDetails):
    """
    Process input/output data from EXPLAIN function in postgresql.
    """
    with DatabaseConnector(login_details, querydetails.database) as cursor:
        query = f'EXPLAIN (FORMAT JSON) {str(querydetails.query)}'
        try:
            cursor.execute(query)
            query_data = cursor.fetchall()
            return query_data
        except:
            return None


# Returns query list for parameter combinations
def generate_combinations(self):
    # Checks number of parameters chosen >0
    list_of_parameters_chosen = interface.MainUI.doCheck(self)
    if len(list_of_parameters_chosen) == 0:
        return

    scan_count, join_count, hash_agg_count, material_count, explicit_count = 0, 0, 0, 0, 0
    scan_selected, join_selected, hash_agg_selected, material_selected, explicit_selected = [], [], [], [], []

    # Extracts chosen parameters into respective count lists.
    for parameters in list_of_parameters_chosen:
        if 'Scan' in parameters:
            scan_selected.append(parameters)
            scan_count += 1
        if 'Join' in parameters:
            join_selected.append(parameters)
            join_count += 1
        if 'Hashed Aggregation' in parameters:
            hash_agg_selected.append(parameters)
            hash_agg_count += 1
        if 'Materialization' in parameters:
            material_selected.append(parameters)
            material_count += 1
        if 'Explicit Sort' in parameters:
            explicit_selected.append(parameters)
            explicit_count += 1

    # Combine scan & join parameters into 1 large list for permuting
    combined_list = [scan_selected, join_selected]

    # Append other classifications of parameters which would not be permuted - only 1 element will be used
    if hash_agg_selected or material_selected or explicit_selected:
        combined_list.append(hash_agg_selected)
        combined_list.append(material_selected)
        combined_list.append(explicit_selected)

    # Initialisation for the permuting
    breakdown = [q for q in combined_list if q != []]
    master_list = [z for z in itertools.product(*breakdown)]
    x = master_list[0]
    others_helper = np.array([0, 0, 0])
    other_categories = ['Hashed Aggregation', 'Materialization', 'Explicit Sort']
    if 'Hashed Aggregation' in x:
        others_helper[0] = 1
    if 'Materialization' in x:
        others_helper[1] = 1
    if 'Explicit Sort' in x:
        others_helper[2] = 1
    indexes = np.where(others_helper == 0)[0]
    indexes2 = np.where(others_helper == 1)[0]

    temp_list = []
    for parameters in master_list:
        combined_tuple = parameters
        for x in indexes:
            combined_tuple = (*combined_tuple, other_categories[x])

        temp_list.append(combined_tuple)

    temp_list_2 = []
    for parameters in temp_list:
        for x in indexes2:
            new_tuple = parameters
            x = new_tuple.index(other_categories[x])
            new_tuple = new_tuple[:x] + new_tuple[x + 1:]
            temp_list_2.append(new_tuple)

    final_tuple_list = temp_list + temp_list_2

    # Initialise query list
    query_list = []
    query_enable = {"enable_bitmapscan": False,
                    "enable_indexscan": False,
                    "enable_indexonlyscan": False,
                    "enable_seqscan": False,
                    "enable_tidscan": False,
                    "enable_hashjoin": False,
                    "enable_mergejoin": False,
                    "enable_nestloop": False,
                    "enable_hashagg": False,
                    "enable_material": False,
                    "enable_sort": False,
                    }
    # Helper to translate names into query
    conversion_helper = {
        "Bitmap Scan": "enable_bitmapscan",
        "Index Scan": "enable_indexscan",
        "Index-only Scan": "enable_indexonlyscan",
        "Sequential Scan": "enable_seqscan",
        "Tid Scan": "enable_tidscan",
        "Hash Join": "enable_hashjoin",
        "Merge Join": "enable_mergejoin",
        "Nested Loop Join": "enable_nestloop",
        "Hashed Aggregation": "enable_hashagg",
        "Materialization": "enable_material",
        "Explicit Sort": "enable_sort"
    }

    for parameters in final_tuple_list:
        temp = query_enable.copy()
        for x in parameters:
            if x in conversion_helper:
                key_value = conversion_helper[x]
                if key_value in temp:
                    temp[key_value] = True
        query_list.append(temp)
    return query_list


# Returns explain output of aqp
def retrieve_aqp_data(login_details: LoginDetails, querydetails: QueryDetails, combinations):
    """
    Executes the AQPs and retrieves their corresponding costs.
    """
    query = "BEGIN;"
    aqp_list = []
    for pairs in combinations:
        with DatabaseConnector(login_details, querydetails.database) as cursor:
            for key in pairs:
                # Set respective parameters for aqp
                if pairs[key]:
                    query += "SET " + key + " TO TRUE;"
                else:
                    query += "SET " + key + " TO FALSE;"

            # Below code gets AQP from running it with parameters set
            query += f'EXPLAIN (FORMAT JSON) {str(querydetails.query)};'
            try:
                cursor.execute(query)
                data = cursor.fetchall()
                aqp = data[0][0][0]["Plan"]
            except:
                aqp = None
            cursor.execute("ROLLBACK;")

        aqp_list.append(aqp)

    # Returns AQP Plan
    return aqp_list


# Returns dictionary of buffer shared hits data against each physical operator used in plan.
# {parameter : no. of buffered shared hits , parameter2: no. of buffered shared hits..}
def retrieve_buffer_access_data(login_details: LoginDetails, querydetails: QueryDetails):
    """
    Return EXPLAIN (analyze, buffers, costs off) output and retrieves buffers number of shared hits
    """
    with DatabaseConnector(login_details, querydetails.database) as cursor:
        query = f'EXPLAIN (analyze, buffers, costs off, format json) {str(querydetails.query)}'
        try:
            cursor.execute(query)
            query_data = cursor.fetchall()
            print(str(query_data) + "\n\nLOL\n\n")
            # Extract the 'Plan' node from the structure
            top_level_plan = query_data[0][0][0]['Plan']

            # Define a function to recursively traverse the plan and extract shared hit counts
            def extract_shared_hits(plan, shared_hits_per_operator):
                node_type = plan.get('Node Type')
                shared_hits = plan.get('Shared Hit Blocks', 0)

                # Check if the operator is already in the dictionary, if not, add it
                if node_type not in shared_hits_per_operator:
                    shared_hits_per_operator[node_type] = 0

                shared_hits_per_operator[node_type] += shared_hits

                # Check for the presence of 'Plans' key before processing child nodes
                if 'Plans' in plan:
                    for child_plan in plan['Plans']:
                        extract_shared_hits(child_plan, shared_hits_per_operator)

            # Extract shared hit counts for each operator in the plan
            shared_hits_per_operator = {}
            extract_shared_hits(top_level_plan, shared_hits_per_operator)

            # Print or use the collected information
            for operator_name, shared_hits in shared_hits_per_operator.items():
                print(f"{operator_name}: Shared Hit Blocks = {shared_hits}")
            return shared_hits_per_operator
        except Exception as e:
            print(f"An error occurred: {e}")

def get_table_names_from_query (query):
    table_names = []

    # Extract table name after the FROM clause
    from_match = re.search(r'FROM\s+(\w+)', query, re.IGNORECASE)
    if from_match:
        table_names.append(from_match.group(1))

    # Extract table names after each JOIN clause
    join_tables = re.findall(r'JOIN\s+(\w+)', query, re.IGNORECASE)
    table_names.extend(join_tables)

    return table_names

# Returns an array of
def retrieve_block_access_count(login_details: LoginDetails, querydetails: QueryDetails):
    with (DatabaseConnector(login_details, querydetails.database) as cursor):
        try:
            query = str(querydetails.query).lower()
            table_names = get_table_names_from_query(query)
            block_count = {}
            for table_name in table_names:
                modified_query = query.replace("select", "select {}.ctid, ".format(table_name))
                cursor.execute(modified_query)
                query_data = cursor.fetchall()
                # print(str(query_data))
                # Parse and count accessed blocks
                for row in query_data:
                    # The ctid is a tuple (block_number, index_within_block)
                    block_number = int(row[0].strip('()').split(',')[0])
                    # Count the accessed blocks
                    if block_number in block_count:
                        block_count[block_number] += 1
                    else:
                        block_count[block_number] = 1

            # Print the block count
            for block_number, count in block_count.items():
                print(f"Block {block_number}: Accessed {count} times")

            return block_count

        except Exception as e:
            print(f"An error occurred: {e}")
