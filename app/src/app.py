from flask import Flask, request, jsonify
import crawler
import db

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/api/v1/resources/clear", methods=['GET'])
def clear():
	db.clear()
	return "ok"


@app.route("/api/v1/resources/search", methods=['GET'])
def search():

	# Check if an url was provided as part of the URL.
	# If url is provided, assign it to a variable.
	# If no url is provided, display an error in the browser.
	if 'url' in request.args:
		url = request.args['url']
	else:
		return "Error: No url field provided. Please specify an url."

	flg_new = 0
	# read the data from base set table
	id_base_set = db.read_base_set(url)
	# meaning new url
	if id_base_set is None:
		flg_new = 1
		# write the url in the base set table
		id_base_set = db.write_base_set(url)
		# get the depth level to crawler
		depth = int(db.read_db_config(section='parameter').get("depth"))
		# crawler the page
		lst_url = []
		lst_results = crawler.search_links(id_base_set, url, depth, lst_url)
		# write the results in the raw table
		db.write_link_references(lst_results)
		# write the results in the summary table
		db.write_link_references_summary(id_base_set)

	# return the array with all information
	lst_return = db.read_link_references_summary(id_base_set, flg_new)
	return jsonify(lst_return)


@app.errorhandler(404)
def page_not_found():
	return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == "__main__":
	app.run(host='0.0.0.0')
