import pandas as pd
from openbb_terminal.sdk import openbb
from datetime import datetime

# openbb.economy.macro_parameters() 
def get_macro_indicators_data(parameters = ["HOU","CORE","RETA"], 
              countries = ["United States", "China","Singapore","Malaysia"],
              symbol="USD"):
    macro_data, *metadata = openbb.economy.macro(parameters=parameters,
                                                 countries=countries,symbol=symbol)
    macro_df = pd.melt(macro_data.reset_index(),id_vars=["date"], 
                       var_name=["countries","variable"],value_name="value")
    macro_df["unit"] = metadata[1].replace("[","").replace("]","").replace("in ","")
    # add currency & measurement column 
    data_type_dict = {}
    for data_type in metadata[0].values():
        data_type_dict.update(**data_type)
    macro_df["currency_or_measurement"] = macro_df["variable"].replace(data_type_dict)
    return macro_df

def get_macro_events(countries=["united_states","china"],
                     start_date="2022-01-01",
                     end_date=datetime.now()):
    #openbb.economy.macro_countries().keys()
    #all_countries = openbb.economy.macro_countries().keys() #str.lower() + replace(" ","_")
    macro_events = openbb.economy.events(countries = countries,
                                           start_date=start_date, 
                                           end_date=end_date)
    return macro_events
    

if __name__ == "__main__":
    #df = get_macro_indicators_data()
    #df.to_csv("test.csv")
    #print(df)