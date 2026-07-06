import pandas as pd


def clean_csv(input_file, output_file):
    """
    Reads a CSV file, cleans the data, and saves the cleaned data
    to a new CSV file.

    Parameters:
        input_file (str): The path to the CSV file you want to clean.
        output_file (str): The path where the cleaned CSV file will be saved.
    """

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # ---------------------------------------------------------
    # 1. Remove duplicate rows
    # ---------------------------------------------------------
    # This removes rows that are exactly the same as another row.
    df = df.drop_duplicates()

    # ---------------------------------------------------------
    # 2. Trim extra spaces from text data
    # ---------------------------------------------------------
    # This removes spaces before and after text in every string cell.
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # ---------------------------------------------------------
    # 3. Standardize column names
    # ---------------------------------------------------------
    # This makes column names lowercase, removes extra spaces,
    # and replaces spaces with underscores.
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # ---------------------------------------------------------
    # 4. Remove empty rows
    # ---------------------------------------------------------
    # This removes rows where every value is missing.
    df = df.dropna(how="all")

    # ---------------------------------------------------------
    # 5. Remove empty columns
    # ---------------------------------------------------------
    # This removes columns where every value is missing.
    df = df.dropna(axis=1, how="all")

    # ---------------------------------------------------------
    # 6. Handle missing values
    # ---------------------------------------------------------
    # For numeric columns, fill missing values with the column average.
    # For text columns, fill missing values with "Unknown".
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].mean())
        else:
            df[column] = df[column].fillna("Unknown")

    # ---------------------------------------------------------
    # 7. Save the cleaned data to a new CSV file
    # ---------------------------------------------------------
    # index=False prevents pandas from adding an extra index column.
    df.to_csv(output_file, index=False)

    print(f"Cleaned CSV file saved as: {output_file}")


# ---------------------------------------------------------
# Example usage
# ---------------------------------------------------------
# Change these file names to match your own files.
input_csv = "input.csv"
output_csv = "cleaned_output.csv"

clean_csv(input_csv, output_csv)