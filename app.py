from flask import Flask, render_template_string
from plStats import *


app = Flask(__name__)

@app.route("/")
def prem_tables():
    league_data = get_league_table()
    t = PrettyTable(league_data[0])
    for team in league_data[1:]:
        t.add_row(team)
    
    prem_table_html = t.get_html_string()

    results, fixtures = get_league_fixtures()
    t2 = PrettyTable(['day','date','time','team1','team1 XG','score','team2 XG','team2','stadium'])
    for game in results:
        t2.add_row(game)

    for game in fixtures:
        t2.add_row(game)

    prem_fixtures_html = t2.get_html_string()

    html_template = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Premier League tables</title>
        <style>
          table {
            width: 100%;
            border-collapse: collapse;
          }
          th, td {
            border: 1px solid #fff;
            padding: 8px;
          }
          body {
            background-color: rgb(27,224,177);
          }
        </style>
      </head>
      <body>
        <h1>PL Table</h1>
        {{ prem_table_html|safe }}
        <h1>PL Fixtures</h1>
        {{ prem_fixtures_html|safe }}
        <p>data sourced from the wonderful https://fbref.com/en/</p>
      </body>
    </html>
    """

    return render_template_string(html_template, prem_table_html=prem_table_html, prem_fixtures_html=prem_fixtures_html)
