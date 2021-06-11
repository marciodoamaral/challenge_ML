""" Module used to access information"""
from flask import Flask, request, jsonify
import utils
import db

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/api/v1/resources/reset", methods=['GET'])
def reset():
    """ load the initial information from base set table
    :return: None
    """
    # clear the database
    db.clear()
    # get the URL from base set
    lst_base_set = db.read_base_set()
    # get the depth level to crawler
    depth = int(db.read_db_config(section='parameter').get("depth"))
    for url in lst_base_set:
        # crawler the page
        lst_url = []
        lst_results = utils.search_links(url, depth, lst_url)
        # write the results in the raw table
        db.write_link_reference_raw(lst_results)

    # write in the summary table
    db.write_link_reference_summary()
    # write summary feature table
    db.write_link_reference_feature_summary()
    # training the model
    utils.train_model()

    return jsonify(db.read_link_reference_feature_summary())


@app.route("/api/v1/resources/search", methods=['GET'])
def search():
    """ Search a url in the database
    :return: List with url, features and predict qty
    """

    # Check if an url was provided as part of the URL.
    # If url is provided, assign it to a variable.
    # If no url is provided, display an error in the browser.
    if 'url' in request.args:
        url = request.args['url']
    else:
        return "Error: No url field provided. Please specify an url."

    # if the url is new
    if db.search_url(url) == 0:
        # write in the summary table
        db.write_link_reference_summary(url)
        # write summary feature table
        db.write_link_reference_feature_summary()
        # list the information
        lst_data = db.read_link_reference_feature_summary(url, 1)
        # remove the url column = 10 columns features
        lst_feature = [sublist[1:] for sublist in lst_data]
        # get the predict data
        prediction_qty = int(utils.predict(lst_feature).tolist()[0])
        # update the prediction qty value
        db.update_link_reference(url, prediction_qty)

    return jsonify(db.read_link_reference_feature_summary(url, 0)[0])


@app.errorhandler(404)
def page_not_found():
    """ Unknown pages
    :return: None
    """
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
    app.run(host='0.0.0.0')
