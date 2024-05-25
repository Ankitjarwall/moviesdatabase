import csv

# Read the TSV file
# Replace with the actual path to your file
file_path = r"C:\Users\Ankit\Downloads\Medlexo Full Version\MedLexo\bin\name.csv"

unique_titles = set()

with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        known_titles = row['knownForTitles']
        if known_titles != r'\N':  # Check if the value is not missing
            titles = known_titles.split(',')
            unique_titles.update(titles)

# Convert the set to a sorted list
sorted_unique_titles = sorted(unique_titles)

# Print the sorted unique titles
# Save the sorted unique titles to a file
# Replace with desired output file path
output_file_path = 'sorted_unique_titles.txt'

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for title in sorted_unique_titles:
        output_file.write(title + '\n')
