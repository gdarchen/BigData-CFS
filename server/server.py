from cassandra.cluster import Cluster

class Server(object):

    def __init__(self):
        cluster = Cluster()
        session = cluster.connect('tmp')
    
    def print_table_rows(self):
        rows = session.execute('SELECT * FROM tmp_table')
        for row in rows:
            print(row)

    def print_table_row_with_id(self, row_id):
        rows = session.execute('SELECT * FROM tmp_table where id=%d' % row_id)
        for row in rows:
            print(row)

    

    
    