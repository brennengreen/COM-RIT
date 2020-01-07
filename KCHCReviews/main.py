import mysql.connector as mariadb
import json as js
import csv

CONFIG_FILE = "config.json" # Holds all of our connection info from the sneak github hackers

# NOTE: Value 0, 1, 2 : Paper, Poster, Either
def get_config():
    with open(CONFIG_FILE) as open_config:
        config = js.load(open_config)
    open_config.close()
    return config

if __name__ == "__main__":
    try:    
        # Attempting to connect to database
        cnx = mariadb.connect(**get_config());
    except mariadb.Error as err:
        # Checking for a couple common errors if there are any
        if err.errno == mariadb.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Wrong username or password")
        elif err.errno == mariadb.errorcode.ER_BAD_DB_ERROR:
            print("Invalid database")
        else:
            print(err)
    else:
        cursor = cnx.cursor(buffered=True)
        query_template = "SELECT * FROM ranks WHERE rev_id={}"
        last_name_query_template = "SELECT last_name FROM reviewers WHERE id={}"
        headers = ["Paper ID", "Rev ID", "Rating", "Theme", "Accept"]
        
        for rev_id in range(103, 166):            
            ### Fetching last name ###
            last_name_query = last_name_query_template.format(rev_id)
            cursor.execute(last_name_query)
            for s in cursor:
                last_name = s[0]
            ##########################
            
            print("CURRENT REVIEWER ID: {} LAST NAME: {}".format(rev_id, last_name))
            
            query = query_template.format(rev_id)
            cursor.execute(query)
            
            csv_name = "{}.csv".format(last_name)
            
            with open(csv_name, mode='w') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                csv_writer.writerow(headers)
                for s in cursor:
                    csv_writer.writerow([s[1], s[2], s[3], s[4], s[5]])
                
            csv_file.close()    
            

            
        cnx.close() # Close connection when finished