import pandas as pd
pd.read_excel(".xls").to_csv("Participant_Data.csv", index=False)
pd.read_excel("WC_data.xls").to_csv("WC_data.csv", index=False)
