from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from waitress import serve

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def web_scraper():
    url = request.args.get('url')
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # find all text within the p tag
        texts = [p.text for p in soup.find_all('p')]

        # find all image src within the img tag
        images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]

        # print the request info
        print(f"Scraping URL: {url}")

        return jsonify({'texts': texts, 'images': images})

    except requests.exceptions.RequestException as err:
        # print the error
        print(f"Error occurred: {err}")
        return {"error": "An Exception occured"}, 400

if __name__ == '__main__':
    print("The app is running")
    serve(app, host="0.0.0.0", port=8080)