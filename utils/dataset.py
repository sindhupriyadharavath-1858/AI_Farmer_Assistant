import csv
import os


def load_dataset(file_path):
    """
    Load a CSV file and return a list of dictionaries.
    """

    if not os.path.exists(file_path):
        return []

    data = []

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                data.append(row)

        return data

    except Exception:
        return []


def search_dataset(data, keyword):
    """
    Search for a keyword anywhere in the dataset.
    """

    if not keyword:
        return []

    results = []

    keyword = keyword.lower().strip()

    for row in data:

        row_text = " ".join(
            str(value).lower()
            for value in row.values()
        )

        if keyword in row_text:
            results.append(row)

    return results