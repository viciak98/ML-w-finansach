import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
from yahoofinancials import YahooFinancials
from datetime import datetime
from datetime import timedelta, date
import csv

df = pd.read_csv('C:\\Users\\kpetu\\PycharmProjects\\umwf\\CONVICTIONLISTTOPN_BSLD-408.csv',header=None)
df.rename(columns={1: "time", 2: "number", 3: "code", 4: "type", 5: "mer", 6: "value"}, inplace=True)


df.describe()

df = df[df['mer'].notnull()]
df = df.dropna()
df.isnull().sum()

plt.hist(df["value"],bins = 15)
plt.show()
plt.clf()

def tydzien(x):
    rok = x[0:2]
    x = x[2:]
    date = datetime.strptime(x, "%y-%m-%d")
    EndDate = date - timedelta(days=6)
    data_koncowa = EndDate.strftime("%y-%m-%d")
    return(rok + data_koncowa)

def dzien(x):
    rok = x[0:2]
    x = x[2:]
    date = datetime.strptime(x, "%y-%m-%d")
    EndDate = date + timedelta(days=1)
    data_koncowa = EndDate.strftime("%y-%m-%d")
    return(rok + data_koncowa)

def ob_zwrot(x, y):
  lista = []
  dane = yf.download(x,
                      start=tydzien(y),
                      end=dzien(y),
                      progress=False)
  for index, row in dane.iterrows():
    lista.append(row["Close"])
  if len(lista) > 0:
    zwrot = (lista[-1]/lista[0])-1
  else:
    zwrot ="nic"
  return(zwrot)

sl_score = {}

for lab, row in df.iterrows():
    sl_score[row["time"]] = {}
    if "." in row["code"]:
      znak_z_x = row["code"]
      indeks_znaku = znak_z_x.index(".")
      row["code"] = znak_z_x[0:indeks_znaku]

    sl_score[row["time"]][row["code"]] = row["value"]

braki = []
with open('C:\\Users\\kpetu\\PycharmProjects\\umwf\\zwroty.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    for lab, row in df.iterrows():
        wiersz = []
        if "." in row["code"]:
            znak_z_x = row["code"]
            indeks_znaku = znak_z_x.index(".")
            row["code"] = znak_z_x[0:indeks_znaku]

        if row["code"] not in braki:
            zw = ob_zwrot(row["code"], row["time"])
            if zw == "nic":
                braki.append(row["code"])
            else:
                wiersz.append(row["time"])
                wiersz.append(row["code"])
                wiersz.append(zw)
            print(wiersz)
            writer.writerow(wiersz)

