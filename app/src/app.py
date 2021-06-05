from flask import Flask, request, jsonify
import crawler
import db

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/api/v1/resources/initialize", methods=['GET'])
def initialize():
	# clear the table to avoid duplication
	db.unload()
	# read the data from base set table
	lst_base_set = db.read_base_set(None)

	# crawler the web sites in the table
	for url in lst_base_set:
		lst_url = []
		lst_results = crawler.search_links(url, 1, lst_url)

	db.write_link_references(lst_results)

	return "ok"


@app.route("/api/v1/resources/clear", methods=['GET'])
def clear():
	db.unload()
	return "ok"


@app.route("/api/v1/resources/search", methods=['GET'])
def search():

	# Check if database already initialized
	if db.check_register() == 0:
		initialize()

	# Check if an url was provided as part of the URL.
	# If url is provided, assign it to a variable.
	# If no url is provided, display an error in the browser.
	if 'url' in request.args:
		url = request.args['url']
	else:
		return "Error: No url field provided. Please specify an url."

	# read the data from base set table
	lst_base_set = db.read_base_set(url)
	# meaning new url
	if lst_base_set is None:
		db.write_base_set(url)
		lst_url = []
		lst_results = crawler.search_links(url, 1, lst_url)
		db.write_link_references(lst_results)

	return jsonify(db.return_links(url))


@app.errorhandler(404)
def page_not_found(e):
	return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
	app.run(host='0.0.0.0')