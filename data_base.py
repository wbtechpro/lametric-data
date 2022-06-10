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
        check_zero = lambda check: not check.isalnum() or '-' in check or 'Value in column' in check
        for key, value in insert.items():
            if isinstance(value, str):
                if check_zero(check=value):
                    value = '0'
                cur.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (key, value,))
                conn.commit()
            elif isinstance(value, dict):
                cur.execute(f"CREATE TABLE IF NOT EXISTS '{key}_{table_name}' ("
                            "'name' VARCHAR(50),"
                            "'value' INTEGER) ")
                cur.execute(f'DELETE FROM "{key}_{table_name}"')
                for k, obj in value.items():
                    if check_zero(check=obj):
                        obj = '0'
                    cur.execute(f"INSERT INTO '{key}_{table_name}' VALUES (?, ?)", (k, obj))
                    conn.commit()

    def get_data(check_table, icon):
        all_result = dict()
        all_result[(items := (check_table, icon))] = []
        for table in all_tables:
            if table != ('sqlite_sequence',) and check_table in table[0]:
                cur.execute("SELECT  * FROM {};".format(*table))
                one_result = cur.fetchall()
                if table[0] == check_table:
                    all_result[items] += one_result
                else:
                    all_result[items].append(
                        {'{}'.format(table[0].split('_')[0]): one_result})
        return all_result

    if insert is not None and environ['REQUEST_METHOD'] == 'POST':
        if environ['PATH_INFO'] == '/webhooks/marketing':
            create_insert_table('MARKETING')
        elif environ['PATH_INFO'] == '/webhooks/recruiting':
            create_insert_table('RECRUITING')
    else:
        if environ['PATH_INFO'] == '/marketing':
            return get_data('MARKETING', 7734), {'Drfts': (1, 'Drfts'),
                                                 'Pstd': (1, 'Pstd'),
                                                 'Psts': (4, 'Psts'),
                                                 'K-Psts': (1, 'K-Psts'),
                                                 'New': (3, 'New'),
                                                 'InRttn': (6, 'Rtn'),
                                                 'KPSnd': (1, 'Prsl'),
                                                 'Clsd': (0, 'Clsd'),
                                                 'NwUsf': (1, 'N-PPL'),
                                                 'Trfc': (614, 'TRFK')}
        elif environ['PATH_INFO'] == '/recruiting':
            return get_data('RECRUITING', 294), {'New': (25, 'New'),
                                                 'Rtn': (10, 'Rtn'),
                                                 'Hired': (1, 'Clsd'),
                                                 'NwAds': (1, 'Ads'),
                                                 'VacPrgrs': (1, 'Vcns'),
                                                 'Back': (10, 'Bck'),
                                                 'Front': (10, 'Frnt'),
                                                 'NoCd': (10, 'Low')}
    conn.close()
