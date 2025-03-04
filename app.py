from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import os
from models import db, DataModel

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "data"
app.config["DATABASE"] = "database.db"


# Funkcija, kas ielādē datus no CSV faila datubāzē
def load_data_from_csv(filepath):
    if DataModel.select().count() == 0:  # Pārbauda, vai datubāze jau nav aizpildīta
        df = pd.read_csv(filepath)
        for _, row in df.iterrows():
            DataModel.create(
                column1=row["column1"], column2=row["column2"], value=row["value"]
            )


# Inicializē datubāzi
db.init("database.db")
db.connect()
db.create_tables([DataModel], safe=True)

# Ielādē datus no CSV faila
load_data_from_csv("data/pre_selected_data.csv")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/visualizations")
def visualizations():
    data = DataModel.select()
    df = pd.DataFrame(list(data.dicts()))

    # Izveido histogrammu
    plt.figure()
    df["value"].hist()
    plot_path = os.path.join("static", "histogram.png")
    plt.savefig(plot_path)
    plt.close()

    return render_template("visualizations.html", plot_url=plot_path)


@app.route("/download")
def download():
    data = DataModel.select()
    df = pd.DataFrame(list(data.dicts()))

    # Saglabā datus CSV failā
    download_path = os.path.join("data", "exported_data.csv")
    df.to_csv(download_path, index=False)

    return send_file(download_path, as_attachment=True)


# Aizver datubāzes savienojumu, kad lietotne beidz darbu
@app.teardown_appcontext
def close_db_connection(exception):
    if not db.is_closed():
        db.close()


if __name__ == "__main__":
    app.run(debug=True)
