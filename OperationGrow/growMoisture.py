import sqlite3

TABLE_PREFIX = 'moisture'
DATABASE_NAME = 'grow.db'
MAX_POINTS = 10

# Class for storing and reading moisture data from the database
class Moisture():
    table = None
    conn = None
    c = None

    # Connect to the table for the specified plant
    def __init__(self, index):
        self.table = TABLE_PREFIX + repr(index)
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.c = self.conn.cursor()
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS %s (time INTEGER PRIMARY KEY ASC, value INTEGER)' %
            self.table
            )

    # Add a measurement to the moisture dataset, and remove spill-over
    def push(self, time, value):
        self.c.execute('SELECT COUNT(*) FROM %s' % self.table)
        result = self.c.fetchall()
        count = result[0][0]
        
        if count > MAX_POINTS:
            self.c.execute(
                'DELETE FROM %s WHERE time IN (SELECT time FROM %s ORDER BY time ASC LIMIT 1)' %
                (self.table, self.table)
                )
        
        self.c.execute('INSERT INTO %s VALUES (%d, %d)' % (self.table, time, value))
        self.conn.commit()

    # Read all data as an array of 2D arrays
    def read(self):
        self.c.execute('SELECT * FROM %s' % self.table)
        sql = self.c.fetchall()
        
        a = []
        for (i, row) in enumerate(sql):
            a.append([row[0], row[1]]);
        return a

    def __del__(self):
        self.conn.close()
