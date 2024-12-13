import os
import csv
import argparse
from datetime import datetime

# Environment variable for the root directory
ROOT_DIR = os.environ['QUEEN_BEE_DATA_ROOT_DIR']

def get_latest_csv_file(root_dir):
    # List all files in the root directory
    files = os.listdir(root_dir)
    
    # Filter files that match the pattern "Spelling Bee Solutions Database-YYYY-MM-DD-HHMMSS.csv"
    csv_files = [f for f in files if f.startswith("Spelling Bee Solutions Database-") and f.endswith(".csv")]
    
    # Extract the date and time from the filenames and find the most recent one
    latest_file = None
    latest_datetime = None
    
    for file in csv_files:
        # Extract the datetime part from the filename
        datetime_str = file[len("Spelling Bee Solutions Database-"):-len(".csv")]
        try:
            file_datetime = datetime.strptime(datetime_str, "%Y-%m-%d-%H%M%S")
            if latest_datetime is None or file_datetime > latest_datetime:
                latest_datetime = file_datetime
                latest_file = file
        except ValueError:
            # Skip files that don't match the expected datetime format
            continue
    
    return os.path.join(root_dir, latest_file) if latest_file else None

def read_csv_file_backwards(file_path):
    with open(file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)
        rows = list(csvreader)[::-1]  # Read all rows and reverse the list
        return header, rows

def extract_components(row):
    date = row[0]
    string = row[1]
    words = row[2].split()
    return date, string, words

def main(word):
    alphagram = ''.join(sorted(set(word)))
    print(f"Alphagram of the word: {alphagram}")
    latest_csv_file = get_latest_csv_file(ROOT_DIR)
    if latest_csv_file:
        print(f"Latest CSV file: {latest_csv_file}")
        header, rows = read_csv_file_backwards(latest_csv_file)
        for row in rows:  # Print the first three rows from the reversed list
            date, puzz_alpha, words = extract_components(row)
            if puzz_alpha[0] in alphagram and set(alphagram).issubset(set(puzz_alpha)):
                valid_words = []
                for word in words: 
                    if set(word)==set(alphagram):
                        valid_words.append(word)
        
                print(f"Date: {date} {puzz_alpha} {valid_words}")

    else:
        print("No CSV files found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find words in the Spelling Bee Solutions Database.')
    parser.add_argument('word', type=str, help='The word to find')
    args = parser.parse_args()
    main(args.word.upper())
