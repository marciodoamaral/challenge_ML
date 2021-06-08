from flask import Flask, request, jsonify
import crawler
import db

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/api/v1/resources/clear", methods=['GET'])
def clear():
	db.clear()
	return "ok"


@app.route("/api/v1/resources/load", methods=['GET'])
def load():

	# clear the database
	db.clear()
	# get the URL from base set
	lst_base_set = db.read_base_set()
	# get the depth level to crawler
	depth = int(db.read_db_config(section='parameter').get("depth"))
	for url in lst_base_set:
		# crawler the page
		lst_url = []
		lst_results = crawler.search_links(url, depth, lst_url)
		# write the results in the raw table
		db.write_link_reference_raw(lst_results)

	# write in the summary table
	db.write_link_reference_summary()
	# write summary feature table
	db.write_link_reference_feature_summary()

	return jsonify(db.read_link_reference_feature_summary())


@app.route("/api/v1/resources/search", methods=['GET'])
def search():

	# Check if an url was provided as part of the URL.
	# If url is provided, assign it to a variable.
	# If no url is provided, display an error in the browser.
	if 'url' in request.args:
		url = request.args['url']
	else:
		return "Error: No url field provided. Please specify an url."

	is_new = 0
	if db.search_url(url) == 0:
		is_new = 1
		# write in the summary table
		db.write_link_reference_summary(url)
		# write summary feature table
		db.write_link_reference_feature_summary()

	return jsonify(db.read_link_reference_feature_summary(url, is_new))


@app.errorhandler(404)
def page_not_found():
	return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
	app.run(host='0.0.0.0')
