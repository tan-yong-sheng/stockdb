import pandas as pd
from openbb_terminal.sdk import openbb
from collections import ChainMap

# openbb.economy.macro_parameters() 
def get_macro(parameters = ["HOU","CORE","RETA"], 
              countries = ["United States", "China","Singapore","Malaysia"],
              symbol="USD"):
    macro_data, *metadata = openbb.economy.macro(parameters=parameters,
                                                 countries=countries,symbol=symbol)
    macro_df = pd.melt(macro_data.reset_index(),id_vars=["date"], 
                       var_name=["countries","variable"],value_name="value")
    macro_df["unit"] = metadata[1].replace("[","").replace("]","").replace("in ","")
    # transform the  
    data_type_dict = {}
    for data_type in metadata[0].values():
        data_type_dict.update(**data_type)
    macro_df["currency_or_measurement"] = macro_df["variable"].replace(data_type_dict)
    return macro_df

if __name__ == "__main__":
    df = get_macro()
    df.to_csv("test.csv")
    print(df)