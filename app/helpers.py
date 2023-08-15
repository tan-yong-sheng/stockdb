import pandas
import numpy
import polars


def standardize_dataframe_column(
    data_frame: pandas.DataFrame, replace_mapper: dict = {}, drop_columns: list = []
) -> pandas.DataFrame:
    """
    Standardizes the column names of a pandas DataFrame and allows for custom renaming.

    This function takes a pandas DataFrame and converts all its column names to lowercase,
    removes leading and trailing whitespaces, and replaces any spaces with underscores.

    Parameters:
        data_frame (pandas.DataFrame): The input DataFrame to be standardized.

        replace_mapper: Keyword arguments for custom renaming of specific columns.
                           The keyword is the current column name, and the value is the desired new name.
        drop_columns: column names where that columns should be removed

    Returns:
        pandas.DataFrame: A new DataFrame with standardized column names. If any custom column renames
                          are specified, they will be applied to the new DataFrame.
    """
    data_frame.reset_index(inplace=True)
    data_frame.rename(columns=replace_mapper, inplace=True)
    data_frame.rename(
        columns={
            col: col.lower().strip().replace(" ", "_") for col in data_frame.columns
        },
        inplace=True,
    )
    data_frame.drop(columns=drop_columns, inplace=True, errors="ignore")
    return data_frame


def remove_null_values_in_dict(data_frame: pandas.DataFrame) -> list:
    # remove null values in the dictionary
    result = [
        {k: v for k, v in row.items() if v is not None}
        for row in data_frame.replace(numpy.nan, None).reset_index().to_dict("records")
    ]
    return result
