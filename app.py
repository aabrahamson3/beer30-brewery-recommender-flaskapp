from flask import Flask, send_from_directory, render_template, request, abort
from waitress import serve
from src.models.brewery_recommender import beer2beer, get_recs_from_wordvec
from src.utils import validate_input

app = Flask(__name__, static_url_path="/static")

@app.route("/")
def index():
    """Return the main page."""
    return send_from_directory("static", "index.html")

@app.route("/get_results", methods=["POST"])
def get_results():
    """ Recommends breweries to visit """
    data = request.form
    # switch = request.form.getlist
    print(data)

    test_value, errors = validate_input(data)
    switch = test_value[2]
    
    if not errors:
        if switch == 'specific beer':
            predicted_class = beer2beer(test_value[1], test_value[0], test_value[3])
        elif switch == 'keyword':
            predicted_class = get_recs_from_wordvec(test_value[1], test_value[0], test_value[3])
        
        if not predicted_class:
            return 'Nothing was found - please go back and try again. Double check the search option you have selected. <br><br> <a href="/">Go back home</a>'

        return render_template("results.html", predicted_class=predicted_class, test=[(predicted_class[i][0],predicted_class[i][2]) for i in predicted_class], switch=test_value[2], search_term = test_value[3])
        
    else:
        return abort(400, errors)


@app.route("/detailed_review", methods=["POST"])
def detailed_review():
    """ Let user recommend many beers for a SVD collaborative filter """
    return render_template("detailed.html")

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
