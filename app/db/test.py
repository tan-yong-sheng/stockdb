from datetime import datetime
from dateutil import relativedelta

from app.db.macro.macro_model import (
    get_countries_code,
    get_economic_calendar,
    get_macro_countries,
    get_macro_parameters,
    get_macro_indicators_data
)


get_macro_indicators_data(parameters=get_macro_parameters(),
                          countries=get_macro_countries()["Country"],
                          start_date="2000-01-01",
                          end_date=datetime.now(),
                          symbol=get_countries_code()["Code"]
                          )
