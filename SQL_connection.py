from pymysql import connect, ProgrammingError


class Connection(object):
    """
    Provides connection to MySQL Server on computer PHY-MP202-8.boisestate.edu
    """
    db_connection = connect(host='PHY-MP202-8.boisestate.edu',
                            user='root',
                            password='',
                            database='research_phot',
                            port=3307)

    def __init__(self):
        pass


class WriteFileStatus(Connection):
    """
    Inherits from Connection class.  Uses cursor function to insert data into
    file_status table in the research_phot database.
    """
    def __init__(self):
        pass

    def write(self, file_name, file_target, filter, phot_stat):
        """
        Inserts row into file_status based on provided parameters:

        :param file_name: filename of image
        :param file_target: target associated with filename
        :param filter: filter associated with CCD image.
            possible values are B,V,R,I.
        :param phot_stat: Value 0 means file can be used in astrometry.net.
                          Value 1 means file will not be used in astrometry.net
        :return:
        """

        try:
            cursor = db_connection.cursor()
            sql_statement = 'INSERT INTO "file_status" values (%s, %s, %s, %s)'
            cursor.execute(sql_statement, (file_name, file_target, filter, phot_stat))
            cursor.commit()
            return True
        except ProgrammingError:
            raise
        finally:
            db_connection.close()



