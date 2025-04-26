import sys
import argparse

def parse_field_string(field_string):
    fields = set()
    try:
        if ',' in field_string:
            separator = ','
        else:
            separator = None
        
        parts = field_string.split(separator)
        
        if not parts or all(p.strip() == "" for p in parts):
            raise ValueError("Field specification cannot be empty.")
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            num = int(part)

            if num <= 0:
                raise ValueError("Field numbers must be positive.")
            
            fields.add(num)
        
        if not fields:
            raise ValueError("No valid field numbers found in specification.")

        sorted_fields = sorted(list(fields))
        return sorted_fields

    except ValueError as e:
            # Raise ArgumentTypeError for argparse to handle nicely
            raise argparse.ArgumentTypeError(f"Invalid field specification '{field_string}': {e}")



parser = argparse.ArgumentParser(
    description= "Cut out selected portions from each line of a file.",
    epilog="Example: python %(prog)s -f 2 -d ',' data.csv" 
)

parser.add_argument('-f', '--field', 
    type=parse_field_string, 
    required=True, 
    help='Select only this field (positive integer)'
)

parser.add_argument(
    '-d', '--delimiter',
    type=str,
    default='\t', # Default delimiter is TAB
    help='Use DELIMITER instead of TAB for field delimiter'
)

parser.add_argument(
    'filename',
    nargs='?', # Allows filename to be optional
    help='The file to process (reads from stdin if omitted)'
)

try:
    args = parser.parse_args()
    

    field_numbers = args.field
    delimeter = args.delimiter
    filename = args.filename
    output_delimiter = delimeter

    input_source = None
    if(filename):
        try:
            input_source = open(filename, 'r', encoding='utf-8')
        except FileNotFoundError:
            print(f"Error: File not found at {filename}", file=sys.stderr) # Print errors to stderr
            sys.exit(1) 
    
    else:
         # Read from standard input if no filename provided
         # (This makes it work with pipes like `cat file | python script.py -f 1`)
         print("No filename provided, reading from standard input...", file=sys.stderr) # Inform user
         input_source = sys.stdin

    
    with input_source:
        for line in input_source:
            processed_line = line.rstrip('\r\n')
            line_fields = processed_line.split(delimeter)
            output_parts = [] # Store the parts to print for this line

            for field_num in field_numbers:
                index = field_num - 1

                if 0 <= index < len(line_fields):
                    output_parts.append(line_fields[index])
            
            print(output_delimiter.join(output_parts))

# --- Handle Argument Parsing Errors ---
except argparse.ArgumentError as e:
    # argparse usually prints help on error, but you can catch specific things
    print(f"Argument Error: {e}", file=sys.stderr)
    sys.exit(1)
except SystemExit as e:
    # Catch SystemExit exceptions raised by parser.error() or --help
    # This prevents traceback messages for expected exits.
    sys.exit(e.code)
except Exception as e:
    # Generic catch for other unexpected errors during setup/processing
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(1)
