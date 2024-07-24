from flask import Flask, render_template
from src.database import Database

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    db = Database('quotes.db')
    quotes = db.get_all_quotes()
    print(quotes)
    return render_template('index.html', quotes=quotes)



