from flask import Flask
import subprocess

app = Flask(__name__)
# flask --app app --debug run


@app.route('/', methods=['GET'])
def scrape_linkedin_endpoint():
    resultado = subprocess.run(
        "scrapy crawl linkedin", shell=True, capture_output=True)

    print(resultado)
    if resultado.returncode == 0:
        return "dsdxad"
    else:
        return f"Error: {resultado}"


if __name__ == '__main__':
    app.run(debug=True)
