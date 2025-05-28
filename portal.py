#innehåller funktioner för att porta datan från skraparen till domaren
import pandas as pd

def get_df_from_csv(file_name):
    print("Extracting data from local csv file...")
    data = pd.read_csv(file_name)

    #in the column there are semicolon separated values
    #split the values and store them in a list
    #make a new column in the df with the lists
    data["Inputs"] = data["Inputs"].apply(lambda x: x.split(";"))
    #strip whitespace from the values in the list
    data["Inputs"] = data["Inputs"].apply(lambda x: [y.strip() for y in x])
    #change all colons, ":", to "-" in the list values
    data["Inputs"] = data["Inputs"].apply(lambda x: [y.replace(":", "-") for y in x])
    #change all "/" to "-" in the list values
    data["Inputs"] = data["Inputs"].apply(lambda x: [y.replace("/", "-") for y in x])
    print("Data extracted successfully!")
    return data

df = get_df_from_csv("output_input_links_with_eu.csv")
print(df)


i = 0
for row_index in range(len(df)):
    row = df.iloc[row_index]
    print("Output: ", row["Output"])
    print("Inputs: ")
    for name in row["Inputs"]:
        print(name)
        i += 1
print("antal input-dokument:",i)