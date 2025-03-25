import psycopg2
import json

db_url = 'postgresql://username:password@localhost:5432/database'

DATABASE_DUMP_JSON_FILE_NAME = "filename.json"

conn = None
cur = None
try:
    data = None

    with open(DATABASE_DUMP_JSON_FILE_NAME, 'r') as f:
        data = json.load(f)

    table_order = None
    with open('table_order', 'r') as trf:
        table_order  = trf.read()

    table_order = (table_order.split('\n'))

    # raise Exception('test error')
    queries = []
    
    for table in table_order: # generate queries in order
        for item in data: # loop through the generated json
            if type(item) is dict: # check if the item datatype is dict
                if item['type'] == 'table': # check if the item type is a table
                    if item['name'] == table: # check if the item name and table name match
                        for row in item['data']:
                            query = f"INSERT INTO \"{item['name']}\" (\"{'\", \"'.join(row.keys())}\") VALUES ({', '.join([f'NULL' if value is None else f'\'{value}\'' if isinstance(value, str) else f'{value}' for value in row.values()])})"
                            queries.append(query)
    
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    # print(queries)
    for query in queries:
        print("Executing", query)
        cur.execute(query)
        print("Ran query")

    conn.commit()

    cur.close()
    conn.close()


except psycopg2.Error as e:
    print("Fail", e)
    if conn:
        conn.rollback()
        cur.close()
        conn.close()
finally:
    print("Done")
    if conn:
        conn.close()