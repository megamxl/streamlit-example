import datetime
from datetime import datetime as dt, time
from sqlalchemy import text

import streamlit as st

"""
# Welcome to How much time dose Simon der Nenning cost's us!

Just enter start and end time and your name and save it

"""
today = "0"

def insertTime(time, name):
    conn = st.connection("postgresql", type="sql")

    # Using a parameterized query for safety

    with conn.session as session:
        # Executing the statement with parameters
        statement = text('INSERT INTO simon (name, decimal_value) VALUES (:name, :time)')
        session.execute(statement, {"name": name, "time": time})
        session.commit()


def showTabel():
    conn = st.connection("postgresql", type="sql")
    sql_query = """

    SELECT *
    FROM simon
    WHERE timestamp BETWEEN DATE_TRUNC('day', CURRENT_TIMESTAMP) AND CURRENT_TIMESTAMP;
    """

    # Execute the query and fetch the results
    result = conn.query(sql_query)

    # Display the results

def showtime():
    conn = st.connection("postgresql", type="sql", ttl=None)
    print("doing")
    sql_query = """
    SELECT sum(decimal_value)
    FROM simon
    WHERE timestamp BETWEEN DATE_TRUNC('day', CURRENT_TIMESTAMP) AND CURRENT_TIMESTAMP;
    """
    # Execute the query and fetch the results
    today = conn.query(sql_query, ttl=1)

    sql_query = """
    SELECT SUM(decimal_value)
    FROM simon
    WHERE timestamp BETWEEN CURRENT_TIMESTAMP - INTERVAL '1 month' AND CURRENT_TIMESTAMP;
    """

    month= conn.query(sql_query,ttl=1)

    sql_query = """
    SELECT SUM(decimal_value)
    FROM simon
    """

    end = conn.query(sql_query, ttl=1)
    return (today.iloc[0,0], month.iloc[0,0], end.iloc[0,0])


title = st.text_input('Name', 'Xmaretti')
col1, col2 = st.columns(2)

with col1:
    start = st.time_input('Set an alarm for', datetime.time(18, 10))

with col2:
    end = st.time_input('Set an alarm for', value="now")

bt = st.button("Save", type="primary")

print("doing1")

if bt:
    datetime1 = dt.combine(datetime.date.today(), start)
    datetime2 = dt.combine(datetime.date.today(), end)

    if(datetime1 > datetime2):
        difference = datetime1 - datetime2
    else:
        difference = datetime2 - datetime1
    minutes_diff = difference.total_seconds() / 60

    insertTime(minutes_diff, title)

st.header(f"Time simon cost us today: {str(showtime()[0])} minutes")
st.header(f"Time simon cost us this Month: {str(showtime()[1])} minutes")
st.header(f"Time simon cost us overall: {str(showtime()[2])} minutes")











