import logging
import sqlite3
import time

# ==================================================================
# EXPERIMENT SETUP - ESTABLISH DATABASE CONNECTION AND LOGGER
# ==================================================================
db = sqlite3.connect("voter_turnout.db")
curr = db.cursor()

log = logging.getLogger("query_indexing_log")
logging.basicConfig(
                    filename="query_indexing.log", 
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s'
                )

# ==================================================================
# TEST QUERIES
# ==================================================================
select_all = """
                SELECT * FROM voter_turnout
            """
select_election_turnout = """
                        SELECT turnout, election 
                        FROM voter_turnout 
                        WHERE year BETWEEN 2020 AND 2024
                    """
select_one_election = """
                    SELECT turnout 
                    FROM voter_turnout 
                    WHERE geo_unit=20 AND election="2024 Presidential Primary"
                """
delete_one_record = """
                DELETE FROM voter_turnout WHERE geo_unit=20 AND election="2024 Presidential Primary"
            """
delete_range_records = """
                    DELETE FROM voter_turnout WHERE year BETWEEN 2020 AND 2024
                """

# ==================================================================
# APPLY INDEXES TO DATABASE
# ==================================================================

# ==================================================================
# TEST QUERIES 
# ==================================================================
def execute_query(query_name, applied_index, query):
    """ 
        query_name (string) -> name of the query being executed, used to identify the query that will be executed
        applied_index (string) -> name of indexing strategy being applied to the query. Acceptable values include:
                                    "hash", "b-tree", or "none" which indicates that no indexing strategy was applied
        query (SQL query) -> query that will be executed for testing purposes

        Given a query "query", execute it 5 times for data testing.
        Log query start time, end time, and execution time.
        Also log the query being executed and the applied indexing strategy
    """
    # Log query being used along with the indexing strategy that's applied 
    log.info("=== BEGINNING %s EXECUTION TEST WITH %s INDEX STRATEGY ===== ", query_name, applied_index)

    # Execute given query 5 times, log output for each test
    try:
        for test_id in range(1,6):
            log.info("=== BEGINNING TEST: %s ===== ", test_id)

            start = time.perf_counter() # Start timer
            res = curr.execute(query) # Execute query
            end = time.perf_counter() # End timer

            # TO-DO - COUNT NUMBER OF ROWS FETCHED

            # Calculate time difference and log execution time MAKE SURE YOU CAN DO MATH OR IF YOU NEED TO SAVE CALCULATION
            log.info("TEST %s EXECUTION TIME: %s", test_id, end - start)
            log.info("=== END TEST %s ===== ", test_id)

    except:
        log.error("=== ERROR: FAILED TO EXECUTE TEST %s FOR QUERY %s ===== ", test_id, query_name)

# ==================================================================
# QUERY EXECUTION SPACE - RUN AND TIME QUERY EXECUTIONS
# ==================================================================
execute_query("select_all_records", "none", select_all)
execute_query("select_all_records", "hash", select_all)
execute_query("select_all_records", "b-tree", select_all)

execute_query("select_election_turnout", "none", select_election_turnout)
execute_query("select_election_turnout", "hash", select_election_turnout)
execute_query("select_election_turnout", "b-tree", select_election_turnout)

execute_query("select_one_election", "none", select_one_election)
execute_query("select_one_election", "hash", select_one_election)
execute_query("select_one_election", "b-tree", select_one_election)

execute_query("delete_one_record", "none", delete_one_record)
execute_query("delete_one_record", "hash", delete_one_record)
execute_query("delete_one_record", "b-tree", delete_one_record)

execute_query("delete_range_records", "none", delete_range_records)
execute_query("delete_range_records", "hash", delete_range_records)
execute_query("delete_range_records", "b-tree", delete_range_records)

# ==================================================================
# CONVERT EXPERIMENT RESULTS - ADD RESULTS TO A GRAPH
# ==================================================================