import sqlite3


def data_base(environ, insert=None, ):
    conn = sqlite3.connect('sqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    all_tables = cur.fetchall()

    def del_table(table):
        cur.execute("DROP TABLE {};".format(table))

    def create_insert_table(table_name):
        for table in all_tables:
            if table != ('sqlite_sequence',) and table_name in table[0]:
                del_table(*table)
        cur.execute(f"CREATE TABLE IF NOT EXISTS '{table_name}' ("
                    "'name' VARCHAR(50),"
                    "'value' INTEGER) ")
        for key, value in insert.items():
            if isinstance(value, str):
                cur.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (key, value,))
                conn.commit()
            elif isinstance(value, dict):
                cur.execute(f"CREATE TABLE IF NOT EXISTS '{key}_{table_name}' ("
                            "'name' VARCHAR(50),"
                            "'value' INTEGER) ")
                cur.execute(f'DELETE FROM "{key}_{table_name}"')
                for k, obj in value.items():
                    cur.execute(f"INSERT INTO '{key}_{table_name}' VALUES (?, ?)", (k, obj))
                    conn.commit()

    def get_data(check_table):
        all_result = dict()
        all_result[check_table] = []
        for table in all_tables:
            if table != ('sqlite_sequence',):
                if check_table in table[0]:
                    cur.execute("SELECT  * FROM {};".format(*table))
                    one_result = cur.fetchall()
                    if table[0] == check_table:
                        all_result[check_table].append(one_result)
                    else:
                        all_result[check_table].append(
                            {'{}'.format(table[0].split('_')[0]): one_result})
        return all_result

    if insert is not None and environ['REQUEST_METHOD'] == 'POST':
        if environ['PATH_INFO'] == '/webhooks/marketing':
            create_insert_table('MARKETING')
        elif environ['PATH_INFO'] == '/webhooks/recruiting':
            create_insert_table('RECRUITING')
    else:
        if environ['PATH_INFO'] == '/marketing':
            return get_data('MARKETING')['MARKETING']
        elif environ['PATH_INFO'] == '/recruiting':
            return get_data('RECRUITING')['RECRUITING']
    conn.close()
