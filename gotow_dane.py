
import pandas as pd

df = pd.read_csv('C:\\Users\\kpetu\\PycharmProjects\\umwf\\CONVICTIONLISTTOPN_BSLD-408.csv',header=None)
df.rename(columns={1: "time", 2: "number", 3: "code", 4: "type", 5: "mer", 6: "value"}, inplace=True)

data = pd.read_csv('C:\\Users\\kpetu\\PycharmProjects\\umwf\\zwroty.csv')
data.columns = ["time", "code", "return"]
sl_score = {}

for lab, row in df.iterrows():
    sl_score[row["time"]] = {}
    if "." in row["code"]:
      znak_z_x = row["code"]
      indeks_znaku = znak_z_x.index(".")
      row["code"] = znak_z_x[0:indeks_znaku]

    sl_score[row["time"]][row["code"]] = row["value"]

df2 = pd.merge(data, df, on=['time','code'])
print(df2)




