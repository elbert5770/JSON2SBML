import csv

def convert_csv_to_text():
    """
    Read Geerts_parameter_values.csv and convert each row to the format:
    'column1 = column2 ; column1 has column3'
    """
    
    input_file = 'Geerts_parameter_values.csv'
    output_file = 'converted_parameters.txt'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as csvfile:
            # Skip the header row
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header
            
            with open(output_file, 'w', encoding='utf-8') as textfile:
                for row in csv_reader:
                    if len(row) >= 3:
                        parameter = row[0].strip()
                        value = row[1].strip()
                        units = row[2].strip()
                        
                        # Create the formatted line
                        formatted_line = f"{parameter} = {value} ; {parameter} has {units}\n"
                        textfile.write(formatted_line)
        
        print(f"Conversion completed successfully!")
        print(f"Output written to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    convert_csv_to_text() 