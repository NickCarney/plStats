import requests
import bs4
from prettytable import PrettyTable

def get_league_table():
    table_url = 'https://fbref.com/en/comps/9/Premier-League-Stats'
    #r = requests.get(table_url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    #get premier league table
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    #to count the team's rankings
    rank = 1
    
    headers = ['rank', 'name', 'MP','W','D','L','GF','GA','Pts','xG','xGA','Last 5','top scorer']
    #list to store team data for each team in the league
    league_data = []
    league_data.append(headers)
    for row in rows[1:]:
        #data to represent each team including rank, name, MP,W,D,L,GF,GA,Pts,xG,xGA,Last 5, and top scorer
        team_data = []
        #gets all details per row
        cells = row.find_all('td')
        #rank
        team_data.append(str(rank))
        #team name
        team_data.append(cells[0].text)
        #matches played
        team_data.append(cells[1].text)
        #wins
        team_data.append(cells[2].text)
        #draws
        team_data.append(cells[3].text)
        #losses
        team_data.append(cells[4].text)
        #goals for
        team_data.append(cells[5].text)
        #goals against
        team_data.append(cells[6].text)
        #points
        team_data.append(cells[8].text)
        #expected goals for
        team_data.append(cells[10].text)
        #expexted goals against
        team_data.append(cells[11].text)
        #last 5 form
        team_data.append(cells[14].text)
        #top scorer
        team_data.append(cells[16].text)
        rank+=1
        league_data.append(team_data)
    return league_data


def print_league_data():
    league_data = get_league_table()
    t = PrettyTable(league_data[0])
    for team in league_data[1:]:
        t.add_row(team)
    print(t)

        
print_league_data()