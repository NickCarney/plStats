import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder

from plStats import *

#list of the urls for multiple leagues so we can predict ranks for them all
leagues = ['https://fbref.com/en/comps/9/Premier-League-Stats','https://fbref.com/en/comps/12/La-Liga-Stats','https://fbref.com/en/comps/20/Bundesliga-Stats']

for league in leagues:
    league_table = get_league_table(league)

    features = ['rank', 'name', 'MP','W','D','L','GF','GA','Pts','xG','xGA','Last 5','top scorer']
    target = 'Pts'

    data = pd.DataFrame(league_table[1:], columns=features)

    label_encoder = LabelEncoder()
    data['Last 5'] = label_encoder.fit_transform(data['Last 5'])
    data['top scorer'] = label_encoder.fit_transform(data['top scorer'])
    data['name'] = label_encoder.fit_transform(data['name'])

    X = data[features]
    y = data[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train,y_train)

    pred = model.predict(X_test)

    error = mean_absolute_error(y_test,pred)

    data['predicted_points'] = model.predict(X)

    data['name'] = label_encoder.inverse_transform(data['name'])

    data['predicted_rank'] = data['predicted_points'].rank(ascending=False)

    final_rankings = data.sort_values('predicted_points', ascending=False)

    print(final_rankings[['name', 'predicted_rank']])

