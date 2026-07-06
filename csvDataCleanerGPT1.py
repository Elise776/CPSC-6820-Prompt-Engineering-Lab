import pandas as pd
from pathlib import Path


def clean_csv(input_file, output_file=None, fill_missing=""):
    """
    Cleans a CSV file and saves the cleaned version.

    Parameters:
        input_file (str): Path to the CSV file to clean.
        output_file (str): Path where the cleaned CSV should be saved.
        fill_missing (str): Value used to replace missing cells.

    Returns:
        pandas.DataFrame: The cleaned DataFrame.
    """

    input_path = Path(input_file)

    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_file}")

    if output_file is None:
        output_file = input_path.with_name(input_path.stem + "_cleaned.csv")

    # Read CSV
    df = pd.read_csv(input_file)

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Remove completely empty rows and columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # Strip extra spaces from text cells
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].astype(str).str.strip()

    # Replace string versions of missing values
    missing_values = ["nan", "None", "NONE", "null", "NULL", "N/A", "n/a", ""]
    df = df.replace(missing_values, pd.NA)

    # Fill missing values
    df = df.fillna(fill_missing)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Save cleaned CSV
    df.to_csv(output_file, index=False)

    print(f"Cleaned CSV saved as: {output_file}")

    return df


# Example usage
if __name__ == "__main__":
    clean_csv("input.csv")