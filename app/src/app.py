from flask import Flask, request, jsonify
import crawler

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/api/v1/resources/teste", methods=['GET'])
def teste():
	return "Hello World!"


@app.route("/api/v1/resources/search", methods=['GET'])
def search():

	# Check if an url was provided as part of the URL.
	# If url is provided, assign it to a variable.
	# If no url is provided, display an error in the browser.
	if 'url' in request.args:
		site_name = request.args['url']
	else:
		return "Error: No url field provided. Please specify an url."

	# Create an empty list for our results
	lst_url = []
	results = crawler.search_links(site_name, 1, lst_url)

	return jsonify(results)


if __name__ == "__main__":
	app.run(host='0.0.0.0')