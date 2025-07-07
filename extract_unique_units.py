import csv
import re

def extract_unique_units():
    """
    Extract unique words from column 3 (Units) of Geerts_parameter_values.csv,
    filter out mathematical characters, and append to converted_parameters.txt
    """
    
    input_file = 'Geerts_parameter_values.csv'
    output_file = 'converted_parameters.txt'
    
    # Set to store unique words
    unique_words = set()
    
    try:
        # Read the CSV file and extract unique words from column 3
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header
            
            for row in csv_reader:
                if len(row) >= 3:
                    units = row[2].strip()
                    
                    # Split by mathematical characters and spaces, then filter
                    # Remove mathematical characters: *, /, (, ), [, ], {, }, +, -, =, <, >, etc.
                    words = re.split(r'[\s\*\/\(\)\[\]\{\}\+\-\=\<\>\^]', units)
                    
                    for word in words:
                        word = word.strip()
                        # Only add non-empty words that are not mathematical characters
                        if word and not re.match(r'^[\*\/\(\)\[\]\{\}\+\-\=\<\>\^]+$', word):
                            unique_words.add(word)
        
        # Sort the unique words alphabetically
        sorted_words = sorted(unique_words)
        
        # Append to the existing text file
        with open(output_file, 'a', encoding='utf-8') as textfile:
            textfile.write('\n')  # Add a blank line for separation
            for word in sorted_words:
                formatted_line = f"unit {word} = \n"
                textfile.write(formatted_line)
        
        print(f"Unique units extraction completed successfully!")
        print(f"Found {len(sorted_words)} unique words in the Units column")
        print(f"Appended to: {output_file}")
        print(f"Unique words: {', '.join(sorted_words)}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    extract_unique_units() 