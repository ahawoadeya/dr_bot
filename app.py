from flask import Flask, render_template, request, send_file, flash
import pickle
import DiseasePred

# import warnings

app = Flask(__name__)
app.config['SECRET_KEY'] = '73a4b6ca8cb647a20b71423e31492452'

# For Coronavirus
with open("Coronavirus_logistic", "rb") as f:
    logisticRegression = pickle.load(f)


@app.route("/")
@app.route("/home")
def Homepage():
    # cases, cured, death = CurrentStats.currentStatus()
    return render_template("index.html", feedback="False")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.route("/infected")
def Infected():
    return render_template("infected.html", disease="Nothing")

@app.route("/noninfected")
def NonInfected():
    return render_template("not-infected.html")

@app.route("/diseaseprediction", methods=["POST", "GET"])
def Disease():
    symptoms = []
    if request.method == "POST":
        rf = request.form
        # print(rf)
        for key, value in rf.items():
            # print(key)
            symptoms.append(value)
        print(symptoms)

        if len(symptoms) < 5 or len(symptoms) > 8:
            flash("Please Select symptoms only between 5 and 8 Inclusive")
        else:
            prediction = DiseasePred.predicts(symptoms)
            if prediction:
                return render_template("infected.htm", disease=prediction)
            else:
                return render_template("not-infected.html")
    return render_template("dp.html")

@app.route("/CoronavirusPrediction", methods=["POST", "GET"])
def Coronavirus():
    if request.method == "POST":
        # print(request.form)
        submitted_values = request.form
        temperature = float(submitted_values["temperature"].strip())
        age = int(submitted_values["age"])
        cough = int(submitted_values["cough"])
        cold = int(submitted_values["cold"])
        sore_throat = int(submitted_values["sore_throat"])
        body_pain = int(submitted_values["body_pain"])
        fatigue = int(submitted_values["fatigue"])
        headache = int(submitted_values["headache"])
        diarrhea = int(submitted_values["diarrhea"])
        difficult_breathing = int(submitted_values["difficult_breathing"])
        travelled14 = int(submitted_values["travelled14"])
        travel_covid = int(submitted_values["travel_covid"])
        covid_contact = int(submitted_values["covid_contact"])

        age = 2 if (age > 50 or age < 10) else 0
        temperature = 1 if temperature > 98 else 0
        difficult_breathing = 2 if difficult_breathing else 0
        travelled14 = 3 if travelled14 else 0
        travel_covid = 3 if travel_covid else 0
        covid_contact = 3 if covid_contact else 0

        model_inputs = [cough, cold, diarrhea,
                        sore_throat, body_pain, headache, temperature, difficult_breathing, fatigue, travelled14, travel_covid, covid_contact, age]
        prediction = logisticRegression.predict([model_inputs])[0]
        # print("**************             ", prediction)
        if prediction:
            return render_template("infected.html", disease="Coronavirus")
        else:
            return render_template("not-infected.html")

    return render_template("Coronavirus.html", title="Coronavirus Prediction", navTitle="COVID-19 Detector", headText="Coronavirus Probability Detector", ImagePath="")


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
