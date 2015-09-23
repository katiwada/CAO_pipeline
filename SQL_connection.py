from pymysql import connect

db_connection = connect(host='PHY-MP202-8.boisestate.edu',
                        user='root',
                        password='',
                        database='research_phot',
                        port=3307)

