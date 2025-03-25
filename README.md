# MySQL to PostgreSQL Data Migration
1. Create a virtual environment
```bash
python3 -m venv .venv
```
2. Activate the virtual environment
```bash
. ./.venv/bin/activate
```
3. Install the required packages
```bash
pip install -r requirements.txt
```
4. Log into **phpmyadmin** and dump your database in JSON format
5. Copy the file inside the project directory root
6. Change the value in `main.py` to match the name of your database dump file
7. Connect to your local PostgreSQL instance
```bash
sudo -u postgre psql
```
8. Create a new database and user
```SQL
-- Create the database
CREATE DATABASE databasename;
-- Create the user
CREATE USER username WITH PASSWORD 'password';
-- Grant connect privilege to the user
GRANT CONNECT ON DATABASE databasename TO username;
-- Connect to the database
\c databasename
-- Grant all privileges to the user on public schema
GRANT USAGE, CREATE ON SCHEMA public TO username;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO username;
```
> This will be your connection string
```plaintext
postgresql://username:password@localhost:5432/databasename #Example
```
9. Change the `db_url` to the connection string from above
10. Migrate the database using your app's orm, you will have make updates on your code to do this. Make user to set the databse url to the one we created earlier
11. After migration is done come back to the app and update the table order in **table_order** file to match the order of insertion.
12. Finally run the main.py script to insert the data into postgresql databse

## Migrating the data to a cloud database.
In case you want to migrate to a cloud database service, for example Neon, it is not advised to run the script on the cloud database, although it is possible to do so. Since we might make a huge number of requests this can cause the db to crash or exhaust your usage quota instead use `pg_dump` and `pg_restore` to transfer data. Run the following code to do this.

```bash
pg_dump --no-owner --no-privileges --no-publications --no-subscriptions --no-tablespaces -Fc -v -d "postgresql://<local_database_username>:<local_database_password>@localhost:5432/<local_database_name>" -f database.bak

pg_restore -v -d "cloud_db_connection_string" database.bak
```

