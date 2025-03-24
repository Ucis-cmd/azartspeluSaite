from flask import Flask, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from peewee import *

db = SqliteDatabase(None)

class GadaModelis(Model):
    gads = IntegerField()
    pavisam = FloatField()
    automāti = FloatField()
    kazino_galdi = FloatField()
    bingo_spēles = FloatField()
    totalizatori = FloatField()
    interaktīvās_spēles = FloatField()
    tālrunis = FloatField()

    class Meta:
        database = db


app = Flask(__name__)
matplotlib.use("agg")


db.init("database.db")
db.connect()
db.create_tables([GadaModelis], safe=True)
if GadaModelis.select().count() == 0:
    df = pd.read_csv("data/azartspeluDati.csv", delimiter=";")
    
    for _, row in df.iterrows():
        GadaModelis.create(
            gads=row["Laika periods"],
            pavisam=row["Pavisam"],
            automāti=row["Azartspēļu automāti"],
            kazino_galdi=row["Azartspēļu kazino galdi"],
            bingo_spēles=row["Bingo spēles"],
            totalizatori=row["Totalizatori"],
            interaktīvās_spēles=row["Interaktīvās azartspēles"],
            tālrunis=row["Veiksmes spēles pa tālruni"])


@app.route("/")
def index():
    return render_template("sākumaLapa.html")

@app.route("/grafiki")
def grafiki():
    dati = GadaModelis.select()
    df = pd.DataFrame(list(dati.dicts()))
    df = df.drop(columns=['id'])
    df.set_index('gads', inplace=True)

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('#303030')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    plot = df.plot(ax=ax)

    nosaukumi = []
    for nosaukums in df.columns:
        nosaukums = nosaukums.capitalize().replace("_", " ")
        nosaukumi.append(nosaukums)
    ax.legend(
        nosaukumi,
        facecolor='black',
        labelcolor='white'
    )
    ax.set_xlabel("Gads")
    ax.set_ylabel("Neto ieņēmumi no azartspēlēm (milj. eiro)")
    fig.savefig("static/linijuGrafiks.jpg")

    
    fig, ax = plt.subplots()

    fig.patch.set_facecolor('black')
    ax.set_facecolor('#303030')

    
    ax.tick_params(axis='y', colors='white')
    ax.xaxis.label.set_color('white')

    dati2024 = GadaModelis.select().where(GadaModelis.gads == 2024)
    df2024 = pd.DataFrame(list(dati2024.dicts()))
    df2024 = df2024.drop(columns=['id'])
    df2024.set_index('gads', inplace=True)
    df2024.plot.bar(ax=ax)
    plt.xticks(rotation=0)  

    nosaukumi = []
    for nosaukums in df2024.columns:
        nosaukums = nosaukums.capitalize().replace("_", " ")
        nosaukumi.append(nosaukums)
    ax.legend(
        nosaukumi,
        facecolor='black',
        labelcolor='white'
    )
    ax.set_xlabel("2024. gads")
    ax.set_ylabel("Neto ieņēmumi no azartspēlēm (milj. eiro)")
    ax.yaxis.label.set_color('white')
    fig.savefig("static/stabinuGrafiks.jpg")


    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('#303030')   
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
   

    stabiņa_kolonnas = []
    for kolonna in df.columns:
        if kolonna == 'pavisam':
            continue
        else:
            stabiņa_kolonnas.append(kolonna)

    stabiņu_dati = df[stabiņa_kolonnas]
    
    stabiņu_dati.plot.bar(stacked=True, ax=ax)
    ax.set_xlabel("Gads")
    ax.set_ylabel("Neto ieņēmumi no azartspēlēm (milj. eiro)")
    
    ax.tick_params(axis='x', labelsize=8)
    
    nosaukumi = []
    for nosaukums in stabiņu_dati.columns:
        nosaukums = nosaukums.capitalize().replace("_", " ")
        nosaukumi.append(nosaukums)
    ax.legend(
        nosaukumi,
        facecolor='black',
        labelcolor='white'
    )
    
    fig.savefig("static/gredotsStabins.jpg")

    saites = ["static/linijuGrafiks.jpg", "static/stabinuGrafiks.jpg", "static/gredotsStabins.jpg"]
    return render_template("diagrammas.html", saites=saites)


@app.route("/lejupielādēt")
def lejupielāde():
    data = GadaModelis.select()
    df = pd.DataFrame(list(data.dicts()))
    df.to_csv("data/dati.csv", index=False)
    return send_file("data/dati.csv", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
