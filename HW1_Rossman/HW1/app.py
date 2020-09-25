from flask import Flask, render_template
import joblib
from flask import request
import pandas as pd

app = Flask(__name__)

# Load ML model
model = joblib.load('rm.pkl')
# Load stores
stores_dummy = pd.read_csv("static/data/stores_dummy.csv", index_col=0)


@app.route('/')
def index():
    # Return Template
    return render_template("index.html")


@app.route('/predict', methods=["POST"])
def predict():

    month = int(request.form['month_select'])
    day, day_name = request.form['day_select'].split(':')
    promo, promo_name = request.form['promo_select'].split(':')
    state_holiday, state_holiday_name = request.form['state_holiday_select'].split(':')
    school_holiday, school_holiday_name = request.form['school_holiday_select'].split(':')
    store = int(request.form['store_select'])

    store_open, store_open_name = request.form['open_select'].split(':')

    if store in (291, 622, 879) or store < 1 or store > 1115:
        prediction = "Store not found"
    elif store_open == "0":
        prediction = "Store is closed"
    else:
        row = stores_dummy.iloc[[store - 1]].copy()
        row['Month'] = int(month)
        row['DayOfWeek'] = int(day)
        row['Promo'] = int(promo)
        row['StateHoliday_0'] = (1 if state_holiday == "0" else 0)
        row['StateHoliday_1'] = (1 if state_holiday == "1" else 0)
        row['StateHoliday_2'] = (1 if state_holiday == "2" else 0)
        row['StateHoliday_3'] = (1 if state_holiday == "3" else 0)
        row['SchoolHoliday'] = int(school_holiday)
        row = row.reindex(sorted(row.columns), axis=1)
        row = row.drop(['PromoInterval'], axis=1)
        prediction = str(round(model.predict(row)[0]))

    print("prediction: " + prediction)

    # Return Template
    return render_template("predict.html", prediction="Prediction: " + prediction, month=month, day=day_name,
                           promo=promo_name, state_holiday=state_holiday_name, school_holiday=school_holiday_name,
                           store=store, open=store_open_name)
