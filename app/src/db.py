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
        cursor.execute("SELECT id_base_set FROM tb_base_set where url = %s", (url,))

        # return row using List datatype
        row = cursor.fetchone()
        if row is None:
            id_base_set = None
        else:
            id_base_set = row[0]

        # close the objects
        cursor.close()
        conn.close()
        return id_base_set
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
        cursor.execute("""Insert into tb_base_set (url) values (%s)""", (url,))
        conn.commit()

        cursor.execute("SELECT id_base_set FROM tb_base_set where url = %s", (url,))
        # return row using List datatype
        id_base_set = cursor.fetchone()[0]

        # close the objects
        cursor.close()
        conn.close()
        return id_base_set

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

        sql = """Insert into tb_link_references_raw(id_base_set, level, top_url, url)
        values(%(id_base_set)s, %(level)s, %(parent_url)s, %(url)s)"""

        for data in lst_data:
            cursor.execute(sql, data)

        conn.commit()
        # close the objects
        cursor.close()
        conn.close()
    except Error as e:
        print(e)


def read_link_references_summary(id_base_set, flg_new):
    """ Read the tb_base_set file and return a list data type with URL column
    :param id_base_set: URL which should be filter
    :param flg_new:
    :return: a list of URL´s
    """
    # try:
    # read the info from config file
    conf_file = read_db_config()
    # open the connection
    conn = MySQLConnection(**conf_file)

    # create and execute the query
    cursor = conn.cursor()

    if flg_new == 1:
        cursor.execute("SELECT url, feature_01, feature_02, feature_03, feature_04, feature_05, "
                       "feature_06, feature_07, feature_08, feature_09, feature_10 "
                       "FROM tb_link_references_summary where id_base_set = %s", (id_base_set,))
    else:
        cursor.execute("SELECT url, feature_01, feature_02, feature_03, feature_04, feature_05, "
                       "feature_06, feature_07, feature_08, feature_09, feature_10, qty_references "
                       "FROM tb_link_references_summary where id_base_set = %s", (id_base_set,))

    # return row using List datatype
    lst_data = cursor.fetchall()

    # close the objects
    cursor.close()
    conn.close()
    return lst_data

#except Error as e:
#        print(e)


def write_link_references_summary(id_base_set):
    """ write the summary info the database
    :param id_base_set: id info to be returned
    :return: None
    """
    # try:
    # read the info from config file
    conf_file = read_db_config()
    # open the connection
    conn = MySQLConnection(**conf_file)

    # create and execute the query
    cursor = conn.cursor()

    sql = "Insert into tb_link_references_summary (id_base_set, url, feature_01, feature_02, " \
          "feature_03, feature_04 , feature_05, feature_06, feature_07, feature_08, feature_09, " \
          "feature_10,qty_references) " \
          "select b.id_base_set, b.url, " \
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
          "count(b.url) as qty_references " \
          "from tb_link_references_raw b " \
          "where b.id_base_set = %s group by b.url " \
          "union " \
          "select distinct b.id_base_set, b.top_url, " \
          "length(b.top_url) length_url, " \
          "case when locate('?', b.top_url) > 0 then " \
          "length(substring(b.top_url, locate('?', b.top_url) + 1, length(b.top_url))) " \
          "else 0 end length_querystring, " \
          "length(b.top_url) - length(REPLACE(b.top_url,'.','')) nbr_dot, " \
          "length(b.top_url) - length(REPLACE(b.top_url,'/','')) nbr_slash, " \
          "length(b.top_url) - length(REPLACE(b.top_url,'&','')) nbr_ampersand, " \
          "length(b.top_url) - length(REPLACE(b.top_url,'-','')) nbr_hyphen, " \
          "length(b.top_url) - length(REPLACE(b.top_url,'_','')) nbr_underscore, " \
          "case when locate('www', b.top_url) > 0 then 1 else 0 end exist_www, " \
          "length(b.top_url) - length(REPLACE(b.top_url,'@','')) nbr_at, " \
          "case when length(substring(b.top_url, locate('.com', b.top_url), length(b.top_url))) > 0 " \
          "then 1 else 0 end if_com " \
          ",0 as qty_references " \
          "from tb_link_references_raw b " \
          "where b.id_base_set = %s and not exists (select 1 from tb_link_references_raw a " \
          "where a.url=b.top_url and a.id_base_set = %s)"

    cursor.execute(sql, (id_base_set, id_base_set, id_base_set))
    conn.commit()

    # close the objects
    cursor.close()
    conn.close()

    # except Error as e:
    #    print(e)


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
        cursor.execute("truncate table tb_base_set")
        conn.commit()
        cursor.execute("truncate table tb_link_references_raw")
        conn.commit()
        cursor.execute("truncate table tb_link_references_summary")
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

        sql = """Insert into tb_log(id_log, msg_log)
        values(%i, %s)"""

        cursor.execute(sql, (1, message))

        conn.commit()

        # close the objects
        cursor.close()
        conn.close()

    except Error as e:
        print(e)
