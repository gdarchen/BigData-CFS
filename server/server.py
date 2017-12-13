from cassandra.cluster import Cluster

class Server(object):

    def __init__(self):
        self.cluster = Cluster()
        self.session = self.cluster.connect('tmp')
    
    def print_table_rows(self):
        rows = self.session.execute('SELECT * FROM tmp_table')
        print(rows)
        for row in rows:
            print(row)

    def print_table_row_with_id(self, row_id):
        rows = self.session.execute('SELECT * FROM tmp_table where id=%d' % row_id)
        for row in rows:
            print(row)

    

    
    