import mysql.connector as mariadb

# NOTE: Value 0, 1, 2 : Paper, Poster, Either

#mariadb_connection = mariadb.connect(database='employees');
#cursor = mariadb_connection.cursor();

for i in range(103, 166):
    query = "SELECT * FROM TABLE WHERE REV_ID IS {}".format(i)
    print(query)
    
#cursor.execute("SELECT * FROM salaries;");

#for s in cursor:
#    print(s);
