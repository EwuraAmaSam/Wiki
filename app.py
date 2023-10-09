from flask import Flask, render_template, url_for
from bs4 import BeautifulSoup
import requests
import wikipediaapi
import random
from transformers import MarianTokenizer, MarianMTModel
model_name = "Helsinki-NLP/opus-mt-en-fr"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

app = Flask(__name__)

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="Wiki/1.0 (ewuraamasam@example.com)"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wiki.html')
def wiki():
    return render_template('wiki.html', article_title="", article_content="")

@app.route('/wiki', methods=['POST'])
def generate_article():
    url = 'https://en.wikipedia.org/wiki/Special:Random'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article_title = soup.find('h1', {'class': 'firstHeading'}).text

    article_content_element = soup.find('div', {'id': 'mw-content-text'})

    
    if article_content_element:
        article_content = ""
        for paragraph in article_content_element.find_all('p'):
            article_content += paragraph.text + '\n'
    else:
        article_content = "Article content not found."
    inputs = tokenizer.encode(">>en<<" + article_content, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(inputs, max_length=500)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return render_template('wiki.html', article_title=article_title, article_content=article_content, translated_text = translated_text)


@app.route('/credits.html')
def credits():

    return render_template('credits.html')

if __name__ == "__main__":
    app.run(debug = True)

