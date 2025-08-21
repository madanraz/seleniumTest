from flask import Flask, request, jsonify

from cuveet import get_cuvette_internships


Cuvette_url = "https://cuvette.tech/jobs/internships"

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Flask app running on Nhost ✅"}

@app.route("/scrape_cuvette", methods=["GET"])
def scrape_api_cuvette():
    refresh = request.args.get("refresh") or request.headers.get("refresh")
    refresh = refresh.lower() == "true" if refresh else False
    result = get_cuvette_internships(url=Cuvette_url,refresh=refresh)
    return jsonify(result)


if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port=5000)
