import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import argparse


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
    df = df.drop_duplicates()

    # ---------------------------------------------------------
    # 2. Trim extra spaces from text data
    # ---------------------------------------------------------
    # This removes spaces before and after text in every string cell.
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # ---------------------------------------------------------
    # 3. Standardize column names
    # ---------------------------------------------------------
    # Example: " First Name " becomes "first_name"
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # ---------------------------------------------------------
    # 4. Remove empty rows
    # ---------------------------------------------------------
    # Removes rows where every value is missing.
    df = df.dropna(how="all")

    # ---------------------------------------------------------
    # 5. Remove empty columns
    # ---------------------------------------------------------
    # Removes columns where every value is missing.
    df = df.dropna(axis=1, how="all")

    # ---------------------------------------------------------
    # 6. Handle missing values
    # ---------------------------------------------------------
    # Numeric columns: fill missing values with the column mean.
    # Text columns: fill missing values with "Unknown".
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].mean())
        else:
            df[column] = df[column].fillna("Unknown")

    # ---------------------------------------------------------
    # 7. Save the cleaned data to a new CSV file
    # ---------------------------------------------------------
    df.to_csv(output_file, index=False)

    print(f"Cleaned CSV file saved as: {output_file}")


def run_terminal_mode():
    """
    Runs the program in terminal-only mode.

    This asks the user to type the input CSV file path
    and the output CSV file path directly into the terminal.
    """

    print("\nCSV Data Cleaner - Terminal Mode")
    print("--------------------------------")

    input_file = input("Enter the input CSV file path: ")
    output_file = input("Enter the output cleaned CSV file path: ")

    if not input_file:
        print("Error: No input file was entered.")
        return

    if not output_file:
        print("Error: No output file was entered.")
        return

    try:
        clean_csv(input_file, output_file)
        print("CSV file cleaned successfully!")

    except Exception as e:
        print(f"Error: Something went wrong:\n{e}")


def browse_input_file():
    """
    Opens a file picker so the user can select the CSV file to clean.
    """

    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )

    if file_path:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)


def browse_output_file():
    """
    Opens a file picker so the user can choose where to save
    the cleaned CSV file.
    """

    file_path = filedialog.asksaveasfilename(
        title="Save Cleaned CSV File As",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if file_path:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, file_path)


def run_cleaner_from_gui():
    """
    Gets the input and output file paths from the GUI,
    runs the cleaner, and shows a success or error message.
    """

    input_file = input_file_entry.get()
    output_file = output_file_entry.get()

    if not input_file:
        messagebox.showerror("Missing Input File", "Please select an input CSV file.")
        return

    if not output_file:
        messagebox.showerror(
            "Missing Output File",
            "Please choose where to save the cleaned CSV file."
        )
        return

    try:
        clean_csv(input_file, output_file)
        messagebox.showinfo("Success", "CSV file cleaned successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n\n{e}")


def switch_to_terminal_mode():
    """
    Closes the GUI and switches the program back to terminal-only mode.
    """

    # Close the GUI window
    root.destroy()

    # After the GUI closes, run the terminal version
    run_terminal_mode()


def start_gui():
    """
    Creates and starts the GUI window.
    """

    global root
    global input_file_entry
    global output_file_entry

    # Create the main window
    root = tk.Tk()
    root.title("CSV Data Cleaner")
    root.geometry("650x320")

    # Title label
    title_label = tk.Label(
        root,
        text="CSV Data Cleaner",
        font=("Arial", 18, "bold")
    )
    title_label.pack(pady=10)

    # ---------------------------------------------------------
    # Input file section
    # ---------------------------------------------------------

    input_frame = tk.Frame(root)
    input_frame.pack(pady=5, padx=10, fill="x")

    input_label = tk.Label(input_frame, text="Input CSV File:")
    input_label.pack(anchor="w")

    input_file_entry = tk.Entry(input_frame, width=60)
    input_file_entry.pack(side="left", padx=(0, 5), fill="x", expand=True)

    input_browse_button = tk.Button(
        input_frame,
        text="Browse",
        command=browse_input_file
    )
    input_browse_button.pack(side="right")

    # ---------------------------------------------------------
    # Output file section
    # ---------------------------------------------------------

    output_frame = tk.Frame(root)
    output_frame.pack(pady=5, padx=10, fill="x")

    output_label = tk.Label(output_frame, text="Save Cleaned CSV As:")
    output_label.pack(anchor="w")

    output_file_entry = tk.Entry(output_frame, width=60)
    output_file_entry.pack(side="left", padx=(0, 5), fill="x", expand=True)

    output_browse_button = tk.Button(
        output_frame,
        text="Browse",
        command=browse_output_file
    )
    output_browse_button.pack(side="right")

    # ---------------------------------------------------------
    # Buttons section
    # ---------------------------------------------------------

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    clean_button = tk.Button(
        button_frame,
        text="Clean CSV",
        font=("Arial", 12, "bold"),
        command=run_cleaner_from_gui
    )
    clean_button.pack(side="left", padx=10)

    terminal_button = tk.Button(
        button_frame,
        text="Switch to Terminal Mode",
        font=("Arial", 12),
        command=switch_to_terminal_mode
    )
    terminal_button.pack(side="left", padx=10)

    # Help text
    help_label = tk.Label(
        root,
        text="Terminal Mode lets you type the file paths instead of using the GUI.",
        font=("Arial", 10)
    )
    help_label.pack(pady=5)

    # Start the GUI event loop
    root.mainloop()


def main():
    """
    Decides whether to run the program with the GUI,
    terminal input mode, or command-line file arguments.
    """

    parser = argparse.ArgumentParser(description="Clean a CSV file.")

    parser.add_argument(
        "input_file",
        nargs="?",
        help="The CSV file to clean."
    )

    parser.add_argument(
        "output_file",
        nargs="?",
        help="The file name for the cleaned CSV."
    )

    parser.add_argument(
        "--gui",
        action="store_true",
        help="Open the GUI version of the program."
    )

    parser.add_argument(
        "--terminal",
        action="store_true",
        help="Run in terminal mode and type file paths manually."
    )

    args = parser.parse_args()

    # If the user types --gui, always open the GUI.
    if args.gui:
        start_gui()

    # If the user types --terminal, run the terminal-only version.
    elif args.terminal:
        run_terminal_mode()

    # If the user gives both file names, run without the GUI.
    elif args.input_file and args.output_file:
        try:
            clean_csv(args.input_file, args.output_file)
        except Exception as e:
            print(f"Error: {e}")

    # If the user gives only one file name, show an error.
    elif args.input_file or args.output_file:
        print("Error: Please provide both an input file and an output file.")
        print("Example:")
        print("python csv_data_cleaner.py input.csv cleaned_output.csv")

    # If the user gives no file names, open the GUI by default.
    else:
        start_gui()


# This makes sure main() only runs when this file is run directly.
# It will not automatically run if this file is imported into another file.
if __name__ == "__main__":
    main()