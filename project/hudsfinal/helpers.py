import os
import requests
import urllib.parse
import json
from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(id):
    """Look up quote for symbol."""
    print("in lookup function")
    # Contact API
    try:
        response = requests.get(f"https://api.cs50.io/dining/recipes/{id}")

        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "food": quote["name"],
            "protein": quote["protein"]["amount"],
            "sodium": quote["sodium"]["amount"],
            "sugars": quote["sugars"]["amount"],
            "total fat": quote["total_fat"]["amount"],
            "calories": quote["calories"],
            "carbs": quote["total_carb"]["amount"],
            "cholesterol": quote["cholesterol"]["amount"],
            "fiber": quote["dietary_fiber"]["amount"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def printing():
    """Look up quote for symbol."""
    print("in lookup function")
    # Contact API
    try:
        response = requests.get(f"https://api.cs50.io/dining/recipes")

        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
         quote = response.json()
         dictionary = {}
         onlyid = {}
         for q in quote:
             dictionary[q["name"]] = q["id"]
             onlyid[q["id"]] = q["name"]
             print(q["name"],q["id"])
        #  print(quote)
         return (dictionary, onlyid)


    except (KeyError, TypeError, ValueError):
        return None

def breakfast():
    """Look up quote for symbol."""
    print("in lookup function")
    # Contact API
    try:
        response = requests.get(f"https://api.cs50.io/dining/menus?meal=0")

        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        dictionary = []
        for q in quote:
            dictionary.append(q["recipe"])
        return dictionary

    except (KeyError, TypeError, ValueError):
        return None


def lunch():
    """Look up quote for symbol."""
    print("in lookup function")
    # Contact API
    try:
        response = requests.get(f"https://api.cs50.io/dining/menus?meal=1")

        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        dictionary = []
        for q in quote:
            dictionary.append(q["recipe"])
        return dictionary

    except (KeyError, TypeError, ValueError):
        return None


def dinner():
    """Look up quote for symbol."""
    print("in lookup function")
    # Contact API
    try:
        response = requests.get(f"https://api.cs50.io/dining/menus?meal=2")

        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        dictionary = []
        for q in quote:
            dictionary.append(q["recipe"])
        return dictionary

    except (KeyError, TypeError, ValueError):
        return None

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"