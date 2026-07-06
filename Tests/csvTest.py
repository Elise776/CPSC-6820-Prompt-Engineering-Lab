from pathlib import Path
import shutil
import subprocess
import pandas as pd

testFolder = Path(__file__).parent
projectFolder = testFolder.parent

cleanerFiles = ["csvDataCleanerGPT1.py", "csvDataCleanerGPT2.py", "csvDataCleanerGPT3.py"]
testCSVFiles = ["csvBasicTest.csv", "csvDuplicatesTest.csv", "csvEmptyRowsColsTest.csv", "csvInconsistantTest.csv", "csvMissingInfoTest.csv"]
inputFile = projectFolder / "input.csv"
outputFile = projectFolder / "cleaned_output.csv"


test_cases = {
    "csvBasicTest.csv": {
        "expected_columns": ["name", "age", "city"],
        "expected_rows": 3,
    },

    "csvDuplicatesTest.csv": {
        "expected_columns": ["name", "age", "city"],
        "expected_rows": 3,
    },

    "csvMissingInfoTest.csv": {
        "expected_columns": ["name", "age", "city", "major"],
        "expected_rows": 4,
    },

    "csvEmptyRowsColsTest.csv": {
        "expected_columns": ["name", "age", "city"],
        "expected_rows": 3,
    },

    "csvInconsistantTest.csv": {
        "expected_columns": ["first_name", "last_name", "student_id", "major"],
        "expected_rows": 3,
    },
}


def run_test(cleanerFile, csvFile, expectedColumns, expectedRows):
    sourceCSV = testFolder / csvFile

    shutil.copy(sourceCSV, inputFile)

    if outputFile.exists():
        outputFile.unlink()

    result = subprocess.run(["python", cleanerFile], cwd=projectFolder, capture_output=True, text=True)

    if result.returncode != 0:
        return False, f"Script crashed:\n{result.stderr}"

    if not outputFile.exists():
        return False, f"Output file was not created: {outputFile.name}"

    cleaned = pd.read_csv(outputFile)

    actualCols = list(cleaned.columns)

    if actualCols != expectedColumns:
        return False, (
            f"Column mismatch.\n"
            f"Expected: {expectedColumns}\n"
            f"Actual:   {actualCols}"
        )

    actualRows = len(cleaned)

    if actualRows != expectedRows:
        return False, (
            f"Row count mismatch.\n"
            f"Expected rows: {expectedRows}\n"
            f"Actual rows:   {actualRows}"
        )

    return True, "Passed"


total_tests = 0
passed_tests = 0

for cleanerFile in cleanerFiles:
    print("\n~~~")
    print(f"Testing cleaner: {cleanerFile}")
    print("~~~")

    for csvFile, expected in test_cases.items():
        total_tests += 1

        passed, message = run_test(
            cleanerFile,
            csvFile,
            expected["expected_columns"],
            expected["expected_rows"]
        )

        if passed:
            passed_tests += 1
            print(f"PASS: {csvFile}")
        else:
            print(f"FAIL: {csvFile}")
            print(message)


print("\n~~~")
print("TEST SUMMARY")
print("~~~")
print(f"Passed: {passed_tests}/{total_tests}")
print(f"Failed: {total_tests - passed_tests}/{total_tests}")