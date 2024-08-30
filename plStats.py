import requests
import bs4
from prettytable import PrettyTable

#this function will get the league table and return a list of lists that contain each row of data in the table
def get_league_table():
    #get html from the amazing fbref webiste
    table_url = 'https://fbref.com/en/comps/9/Premier-League-Stats'
    r = requests.get(table_url)
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

#this function will get the fixtures from the premier league and will return two lists one with the previous results and one with the upcoming fixtures
def get_league_fixtures():
    fixtures_url = 'https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures'
    req = requests.get(fixtures_url)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    
    #get premier league fixtures table
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    
    #list for all previously played results
    results = []
    #list for upcoming fixtures
    fixtures = []
    
    for row in rows[1:]:
        #list to represent one game whethere already played or not
        game = []
        cells = row.find_all('td')

        #if there is an empty row, we will skip that iteration
        if(cells[2].text == ''):
            continue

        #the day of the week the game is played
        game.append(cells[0].text)
        #the date the game is played
        game.append(cells[1].text)
        #the time of day the game is played (in BST so we will subtract 7 hours to get eastern time
        game.append(cells[2].text)
        #team 1 (home team)
        game.append(cells[3].text)
        #team 1 expected goals
        game.append(cells[4].text)
        #score of the game, which we will find the winner from
        score = cells[5].text
        game.append(score)
        #team 2 XG
        game.append(cells[6].text)
        #team 2
        game.append(cells[7].text)
        #stadium
        game.append(cells[9].text)

        #now we look at the 'match report' section to see if the game has already been played('Match Report') or not('Head-to-Head')
        if(cells[11].text == 'Match Report'):#the match has already been played and is a result
            results.append(game)
        else:#the game has not been played and is a fixture
            fixtures.append(game)

    return results, fixtures

#this function will print the league table in a nice format
def print_league_table():
    league_data = get_league_table()
    t = PrettyTable(league_data[0])
    for team in league_data[1:]:
        t.add_row(team)
    print(t)
    return t

#this function will print the previous league results in a nice format
def print_league_results():
    results, fixtures = get_league_fixtures()
    t = PrettyTable(['day','date','time','team1','team1 XG','score','team2 XG','team2','stadium'])
    for game in results:
        t.add_row(game)
    print(t)
    return t

#this function will print the upcoming league fixtures in a nice format
def print_league_fixtures():
    results, fixtures = get_league_fixtures()
    t = PrettyTable(['day','date','time','team1','team1 XG','score','team2 XG','team2','stadium'])
    for game in fixtures:
        t.add_row(game)
    print(t)
    return t

def main():
    #get and print league table data
    print_league_table()
    #get and print the results
    print_league_results()
    #get and print the fixtures
    print_league_fixtures()

if __name__ == '__main__':
    main()