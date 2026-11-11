import sqlite3
import csv

# ==================================================================
# CONVERT CSV TO SQL
# ==================================================================

# Create new database connection voter_turnout
db = sqlite3.connect("voter_turnout.db")
curr = db.cursor()

# Create voter turnout table
curr.execute(
    """
        CREATE TABLE IF NOT EXISTS voter_turnout(
            geo_level,
            geo_unit,
            voted,
            did_not_vote,
            not_eligible_to_vote,
            turnout,
            election,
            election_date,
            year
        )
    """
)

# open file and save as voter_turnout
with open("Historical_Voter_Turnout.csv") as voter_turnout:
    voter_data = csv.reader(voter_turnout, delimiter=",")

    for row in voter_data:
        # Add data in row to tuple to add to sql dataset piece of data 
        data = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],)

        curr.execute(
            """
                INSERT INTO voter_turnout(geo_level,
                            geo_unit,
                            voted,
                            did_not_vote,
                            not_eligible_to_vote,
                            turnout,
                            election,
                            election_date,
                            year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            data
        )
        db.commit()

# ==================================================================
# APPLY INDEXES TO DATABASE
# ==================================================================

# ==================================================================
# TEST QUERIES 
# ==================================================================

# ==================================================================
# QUERY EXECUTION SPACE - RUN AND TIME QUERY EXECUTIONS
# ==================================================================

# ==================================================================
# CONVERT EXPERIMENT RESULTS - ADD RESULTS TO A GRAPH
# ==================================================================