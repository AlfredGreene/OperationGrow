import sqlite3

TABLE_NAME = 'configuration'
DATABASE_NAME = 'grow.db'

class Configuration:
    conn = None
    c = None

    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_NAME)
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS configuration (plant INTEGER PRIMARY KEY, name TEXT, enabled INTEGER, dry INTEGER)')
    
    def push(self, plant, name, enabled, dry):
        self.c.execute(
            'INSERT OR REPLACE INTO configuration VALUES (%d, "%s", %d, %d)' %
            (plant, name, enabled, dry)
            )
        self.conn.commit()

    def setDry(self, plant, dry):
        self.c.execute(
            '''UPDATE configuration
               SET dry=%d
               WHERE plant=%d''' %
            (dry, plant)
            )
        self.conn.commit()

    def read(self):
        self.c.execute('SELECT * FROM %s' % TABLE_NAME)
        sql = self.c.fetchall()
        
        a = []
        for (i, row) in enumerate(sql):
            a.append({
                'plant':row[0],
                'name':row[1],
                'enabled':row[2],
                'dry':row[3],
                });
        return a

    def getNames(self):
        self.c.execute('SELECT name FROM %s' % TABLE_NAME)
        sql = self.c.fetchall()
        return sql

    def __del__(self):
        self.conn.close()
