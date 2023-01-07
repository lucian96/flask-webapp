"""
with j2 we can process and render expressions, data structures(lists, dicts, custom objects),
conditionals({% if expression %}; {% endif %}),
loops({% for item in list; for key, value in dict.items() %}; {% endfor %})
"""
import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)
    client = MongoClient("mongodb+srv://lucian:mongodbpa55@cluster0.ai1jgol.mongodb.net/test")
    app.db = client.webapp

    # entries = []

    @app.route("/", methods=["GET", "POST"])
    def home():
        print([e for e in app.db.entries.find({})])
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            # entries.append((entry_content, formatted_date))
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (entry["content"],
             entry["date"],
             datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"))
            for entry in app.db.entries.find({})
        ]

        return render_template("home.html", entries=entries_with_date)

    return app

