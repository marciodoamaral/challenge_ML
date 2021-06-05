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


def read_base_set(url):
    """ Read the tb_base_set file and return a list data type with URL column
    :param url: URL which should be filter
    :return: a list of URL´s
    """
    try:
        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()
        if url is None:
            cursor.execute('SELECT url FROM tb_base_set')
        else:
            cursor.execute("SELECT url FROM tb_base_set where url = %s", (url,))

        # return row using List datatype
        lst_data = [item[0] for item in cursor.fetchall()]

        # close the objects
        cursor.close()
        conn.close()
        return lst_data
    except Error as e:
        print(e)


def check_register():
    """ Read the tb_link_references file and return number of rows
    :return: an integer number of rows
    """
    try:
        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()
        cursor.execute('SELECT coalesce(count(1), 0) cnt FROM tb_link_references')

        # return row using List datatype
        cnt_row = cursor.fetchone()

        # close the objects
        cursor.close()
        conn.close()
        return cnt_row
    except Error as e:
        print(e)


def write_base_set(url):
    """ Write a url in the base set table
    :param url: URL to be added
    :return: None
    """
    try:
        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()
        cursor.execute("Insert into tb_link_references(url) values(%(url)s)", (url,))
        conn.commit()

        # close the objects
        cursor.close()
        conn.close()
    except Error as e:
        print(e)


def write_link_references(lst_data):
    """ Write the link references in the database
    :param lst_data: list of data to be inserted in the link reference table
    :return: None
    """
    try:
        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()

        sql = """Insert into tb_link_references(level, top_url, url)
        values( %(level)s, %(parent_url)s, %(url)s)"""

        for data in lst_data:
            cursor.execute(sql, data)

        conn.commit()

        # close the objects
        cursor.close()
        conn.close()
    except Error as e:
        print(e)


def return_links(url):
    """ Return a list of URL´s from the database
    :return: list of URL´s
    """
    try:
        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()

        sql = "select a.url, " \
              "length(a.url) length_url, " \
              "length(substring(a.url, locate('?', a.url), length(a.url))) length_querystring," \
              "length(a.url) - length(REPLACE(a.url,'.','')) nbr_dot, " \
              "length(a.url) - length(REPLACE(a.url,'/','')) nbr_fslash, " \
              "length(a.url) - length(REPLACE(a.url,'&','')) nbr_ampersand, " \
              "length(a.url) - length(REPLACE(a.url,'-','')) nbr_hyphen, " \
              "length(a.url) - length(REPLACE(a.url,'_','')) nbr_underscore, " \
              "case when locate('www', a.url) > 0 then 1 else 0 end exist_www, " \
              "CAST(a.url as SIGNED) AS nbr_digit, " \
              "case when substring(a.url, locate('.com', a.url), length(a.url)) > 0 then 1 else 0 end if_com, " \
              "count(1) as qty_references " \
              "from tb_base_set a inner join tb_link_references b on a.url = b.top_url "
        if url is not None:
            sql += " where a.url = %s group by a.url"
            cursor.execute(sql, (url,))
        else:
            sql += "group by a.url"
            cursor.execute(sql)

        lst_data = cursor.fetchall()

        # close the objects
        cursor.close()
        conn.close()

        return lst_data

    except Error as e:
        print(e)


def unload():
    """ Remove all information from the tb_link_references table
    :return: None
    """
    try:
        # read the info from config file
        conf_file = read_db_config()
        # open the connection
        conn = MySQLConnection(**conf_file)

        # create and execute the query
        cursor = conn.cursor()

        # create and execute the query
        cursor = conn.cursor()

        sql = "truncate table tb_link_references"

        cursor.execute(sql)

        conn.commit()

        # close the objects
        cursor.close()
        conn.close()

    except Error as e:
        print(e)


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
