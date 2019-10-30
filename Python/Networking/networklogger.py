import re
import time
import os.path
import sqlite3
from datetime import datetime
from subprocess import Popen, PIPE

# Executes ifconfig
# Output format: (rx ,tx)
# TODO: Improve way to gather information about network ports
def execute_ifconfig(interface):
    command = f'ifconfig {interface}'

    # Open subprocess and parse output
    pipe = Popen(command, shell=True, stdout=PIPE)
    command_output = pipe.communicate()[0].decode("ascii")

    # Find byte values
    parser_regex = r'bytes ([0-9]*)'
    values = re.findall(parser_regex, command_output)

    # Convert to int
    return int(values[0]), int(values[1])

# Setup database file
def init_sqlite3(file):

    # Just connect when there is a file found
    if os.path.isfile(file):
        return sqlite3.connect(file)

    # Connect to the database if there is no file found
    db = sqlite3.connect(file)

    # Create new table for storing records
    db.execute('''CREATE TABLE RECORDS ( \
        TIMESTAMP INTEGER NOT NULL PRIMARY KEY, \
        TOTAL_RECIEVED INTEGER NOT NULL, \
        TOTAL_SEND INTEGER NOT NULL,\
        RECIEVED INTEGER NOT NULL, \
        SEND INTEGER NOT NULL,\
        SPECIAL INTEGER NOT NULL)
        ''')
    db.commit()
    return db


# Recieve last row in the database and select the totals
def get_lastvalue(db):
    sql = f'SELECT TOTAL_RECIEVED, TOTAL_SEND FROM RECORDS WHERE TIMESTAMP = (SELECT MAX(TIMESTAMP)  FROM RECORDS);'
    output = db.execute(sql).fetchone()
    # Return 0, 0 when there is nothing in the database
    if output is None:
        return 0, 0
    return output[0], output[1]


def add_row(db, total_recieved, total_send, recieved, send, timestamp=None, special=0):
    # Set timestamp in miliseconds if it wasn't set
    if timestamp is None:
        timestamp = int(round(time.time()*1000))

    # Add values to database
    sql = 'INSERT INTO RECORDS (TIMESTAMP, TOTAL_RECIEVED , TOTAL_SEND, RECIEVED, SEND, SPECIAL) ' \
        f'VALUES({timestamp}, {total_recieved}, {total_send}, {recieved}, {send},{special});'
    db.execute(sql)
    db.commit()

# Make the large numbers more readable
def byte_formatter(value):
    # Could add more options here but only in the power of 3
    byte_units = ['B ', 'KB', 'MB', 'GB', 'TB']
    options = len(byte_units)
    size = len(str(value))

    for i in reversed(range(options)):
        if value >= 10 ** (3 * i):
            reduced = value / 1000 ** i
            # Add some pretty formatting
            return '{:6.2F}{}'.format(reduced, byte_units[i])


def print_usage(total_rx, total_tx):
    # Some disgusting code to format the strings pretty
    message = '{} | rx: {} | tx: {} | total: {}'.format(
        datetime.now().strftime('%H:%M:%S'), byte_formatter(total_rx),
        byte_formatter(total_tx), byte_formatter(total_rx+total_tx))
    print(message)


def recieve_loop(interface, delay=10, boot=False, database_file='data.sqlite'):
    db = init_sqlite3(database_file)

    # Get base values
    total_rx, total_tx = get_lastvalue(db)
    last_rx, last_tx = execute_ifconfig(interface)

    # This should only be enabled when you're logging networkstats full time
    if boot:
        total_rx, total_tx = total_rx + last_rx, total_tx + last_tx
        add_row(db, total_rx, total_tx, last_rx, last_tx, special=1)
        print_usage(total_rx, total_tx)

    while(1):
        time.sleep(delay)
        now = datetime.now().strftime('%H:%M:%S')

        # Calculate new values
        new_rx, new_tx = execute_ifconfig(interface)
        calc_rx, calc_tx = new_rx - last_rx, new_tx - last_tx
        total_rx, total_tx = total_rx + calc_rx, total_tx + calc_tx

        # Add new information to the database
        add_row(db, total_rx, total_tx, calc_rx, calc_tx)

        print_usage(total_rx, total_tx)


# For testing
if __name__ == "__main__":
    try:
        recieve_loop('lo', boot=False)
    except:
        pass
