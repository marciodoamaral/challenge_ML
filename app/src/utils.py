""" Module used to access information"""
import re
import os
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from joblib import dump, load
import db


# function to return the links inside URL
def search_links(url, depth, list_url):
    """ Read database configuration file and return a dictionary object
    :param url: the URL to be crawled
    :param depth: the level to depth
    :param list_url: the list of url
    :return: a list of url which exists in the URL
    """

    parent_url = url
    # if reach the last level
    if depth < 0:
        return None

    try:
        # make a request to specific site
        request_page = requests.get(url)

        if request_page.status_code == 200:

            # convert the request to text and parse it
            soup = BeautifulSoup(request_page.text, "html.parser")

            # make a loop to get all links in the URL
            for obj in soup.find_all("a", attrs={'href': re.compile("^(http|https)")}):
                tuple_href = ()
                href_address = str(obj.attrs['href']).replace("<", "")

                if href_address not in list_url:
                    # level, parent_url, url
                    tuple_href = (depth, parent_url, href_address)
                    # list_url.append(dict_href)
                    list_url.append(tuple_href)
                    # calling it self
                    search_links(href_address, depth - 1, list_url)

    except HTTPError as error_msg:
        print(error_msg)

    return list_url


def train_model():
    """ train the model and store it in the filesystem
    :return: None
    """

    # Load directory paths for persisting model
    model_dir = os.environ["MODEL_DIR"]
    model_file = os.environ["MODEL_FILE"]
    model_path = os.path.join(model_dir, model_file)

    # load the data to be trained ans separated them
    lst_data = db.read_link_reference_feature_summary()
    # load the last value which is qty_reference
    lst_label = [sublist[-1] for sublist in lst_data]
    # load all features
    lst_feature = [sublist[1:-1] for sublist in lst_data]

    # convert the list to numpy array
    np_label = np.array(lst_label)
    np_feature = np.array(lst_feature)

    # split the data into training and testing sets
    train_features, test_features, train_labels, test_labels = train_test_split(
        np_feature, np_label, test_size=0.3)

    # instantiate model with 1000 decision trees
    clf_rf = RandomForestRegressor(n_estimators=1000)

    # train the model on training data
    clf_rf.fit(train_features, train_labels)

    # Serialize model
    dump(clf_rf, model_path)


def predict(lst_data):
    """ Read database configuration file and return a dictionary object
    :param lst_data: the list of features used to predict
    :return: the predict value
    """

    # Load directory paths for persisting model
    model_dir = os.environ["MODEL_DIR"]
    model_file = os.environ["MODEL_FILE"]
    model_path = os.path.join(model_dir, model_file)

    # verify if trained file exists
    if not os.path.exists(model_path):
        train_model()

    # load the trained model
    clf_rf = load(model_path)
    # predict the qty data
    prediction_lda = clf_rf.predict(lst_data)

    return prediction_lda
