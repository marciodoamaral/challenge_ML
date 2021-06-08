from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser


def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """

    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    dict_db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            dict_db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return dict_db


def search_url(url):
    """ Read the tb_link_reference_summary table and check if the url exists
    :param url: url to be search
    :return: an integer number of row.
    """
    try:

        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()
        cursor.execute('SELECT coalesce(count(1), 0) cnt FROM tb_link_reference_summary where url = %s', (url,))

        # return row using List datatype
        cnt_row = cursor.fetchone()[0]

        # close the objects
        cursor.close()
        conn.close()
        return cnt_row

    except Error as e:
        print(e)


def clear():
    """ Remove all information from the tables
    :return: None
    """
    try:
        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()
        cursor.execute("truncate table tb_link_reference_raw")
        conn.commit()
        cursor.execute("truncate table tb_link_reference_summary")
        conn.commit()
        cursor.execute("truncate table tb_link_reference_feature_summary")
        conn.commit()

        # close the objects
        cursor.close()
        conn.close()

    except Error as e:
        print(e)


def read_base_set(*args):
    """ Read the tb_base_set file and return a list data type with URL column
    :return: a list of URL´s
    """
    try:
        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()
        if len(args) > 0:
            cursor.execute("SELECT url FROM tb_base_set where url = %s", (args[0],))
        else:
            cursor.execute('SELECT url FROM tb_base_set')

        # return row using List datatype
        lst_data = [item[0] for item in cursor.fetchall()]

        # close the objects
        cursor.close()
        conn.close()
        return lst_data
    except Error as e:
        print(e)


def read_link_reference_feature_summary(*args):
    """ Read the tb_base_set file and return a list data type with URL column
    :return: a list of URL´s
    """
    try:
        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()
        if len(args) > 0:
            if args[1] == 1:
                sql = "SELECT url, feature_01, feature_02, feature_03, feature_04, feature_05, "\
                      "feature_06, feature_07, feature_08, feature_09, feature_10 " \
                      "FROM tb_link_reference_feature_summary where url = %s"
            else:
                sql = "SELECT url, feature_01, feature_02, feature_03, feature_04, feature_05, " \
                      "feature_06, feature_07, feature_08, feature_09, feature_10, qty_reference " \
                      "FROM tb_link_reference_feature_summary where url = %s"
            cursor.execute(sql, (args[0],))
        else:
            cursor.execute('SELECT url, feature_01, feature_02, feature_03, feature_04, feature_05, '
                           'feature_06, feature_07, feature_08, feature_09, feature_10, qty_reference '
                           'FROM tb_link_reference_feature_summary')

        # return row using List datatype
        lst_data = cursor.fetchall()

        # close the objects
        cursor.close()
        conn.close()
        return lst_data
    except Error as e:
        print(e)


def write_link_reference_raw(lst_data):
    """ Write the link references in the database
    :param lst_data: list of data to be inserted in the link reference table
    :return: None
    """
    # try:
    # read the info from config file
    conf_file = read_db_config()
    # open the connection
    conn = MySQLConnection(**conf_file)

    # create and execute the query
    cursor = conn.cursor()
    sql = "Insert into tb_link_reference_raw(level, top_url, url) values(%s, %s, %s)"
    cursor.executemany(sql, lst_data)

    # for data in lst_data:
    #    cursor.execute(sql, data)

    conn.commit()
    # close the objects
    cursor.close()
    conn.close()
    # except Error as e:
    #    print(e)


def write_link_reference_summary(*args):
    """ write the summary info the database
    :return: None
    """
    # try:
    # read the info from config file
    conf_file = read_db_config()
    # open the connection
    conn = MySQLConnection(**conf_file)

    # create and execute the query
    cursor = conn.cursor()
    if len(args) == 0:
        sql = "INSERT INTO tb_link_reference_summary(url,qty_reference) " \
              "select a.url, " \
              "coalesce(count(b.url),0) as qty_reference " \
              "from tb_base_set a " \
              "left join tb_link_reference_raw b " \
              "on a.url=b.url group by a.url "
        cursor.execute(sql)
    else:
        sql = "Insert into tb_link_reference_summary (url, qty_reference) values(%s, null)"
        cursor.execute(sql, (args[0],))

    conn.commit()

    # close the objects
    cursor.close()
    conn.close()

    # except Error as e:
    #    print(e)


def write_link_reference_feature_summary(*args):
    """ write the feature summary info in the database
    :return: None
    """
    # try:
    # read the info from config file
    conf_file = read_db_config()
    # open the connection
    conn = MySQLConnection(**conf_file)

    # create and execute the query
    cursor = conn.cursor()

    sql = "Insert into tb_link_reference_feature_summary (url,  feature_01, feature_02, " \
          "feature_03, feature_04 , feature_05, feature_06, feature_07, feature_08, feature_09, " \
          "feature_10, qty_reference) " \
          "select b.url, " \
          "length(b.url) length_url, " \
          "case when locate('?', b.url) > 0 then " \
          "length(substring(b.url, locate('?', b.url) + 1, length(b.url))) " \
          "else 0 end length_querystring, " \
          "length(b.url) - length(REPLACE(b.url,'.','')) nbr_dot, " \
          "length(b.url) - length(REPLACE(b.url,'/','')) nbr_slash, " \
          "length(b.url) - length(REPLACE(b.url,'&','')) nbr_ampersand, " \
          "length(b.url) - length(REPLACE(b.url,'-','')) nbr_hyphen, " \
          "length(b.url) - length(REPLACE(b.url,'_','')) nbr_underscore, " \
          "case when locate('www', b.url) > 0 then 1 else 0 end exist_www, " \
          "length(b.url) - length(REPLACE(b.url,'@','')) nbr_at, " \
          "case when length(substring(b.url, locate('.com', b.url), length(b.url))) > 0 then 1 else 0 end if_com, " \
          "b.qty_reference " \
          "from tb_link_reference_summary b "

    # if it is a new register not in base set
    if len(args) > 0:
        url = args[0]
        sql += "where b.url = %s "
        cursor.execute(sql, (url,))
    else:
        cursor.execute(sql)

    conn.commit()

    # close the objects
    cursor.close()
    conn.close()

    # except Error as e:
    #    print(e)


def log_msg(message):
    """ Write log information in the table
    :param message: message to log
    :return: None
    """
    try:
        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()

        sql = """Insert into tb_log(id_log, msg_log)
        values(%i, %s)"""

        cursor.execute(sql, (1, message))

        conn.commit()

        # close the objects
        cursor.close()
        conn.close()

    except Error as e:
        print(e)
