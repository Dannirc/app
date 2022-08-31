import csv
import json
import pandas as pd

with open("archivo.json", "w") as archivo:
    archivo.write("")
    archivo.close()


pasarlo= pd.DataFrame(pd.read_csv("ficha1.csv", sep=";", header=0, dtype={"pk": int}, index_col=False, encoding='latin-1', error_bad_lines=False))

lista = pd.DataFrame(pd.read_csv("ficha2.csv", sep=";", header=0, dtype={"pk": int}, index_col=False, encoding='latin-1', error_bad_lines=False))

new = []

for i in range(0, len(lista)):
    print(lista.iloc[i].to_dict())
    new.append(lista.iloc[i].to_dict())

pasarlo['fields'] = new

pasarlo.to_json("archivo.json", orient="records", date_format="epoch", double_precision=10, force_ascii=True, date_unit="ms", default_handler=None, indent=1)


print(pasarlo.values[0])