import sys
import argparse

parser = argparse.ArgumentParser(
    description= "Cut out selected portions from each line of a file.",
    epilog="Example: python %(prog)s -f 2 -d ',' data.csv" 
)

parser.add_argument('-f', '--field', 
    type=int, 
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
    if(args.field<=0):
        parser.error("argument -f/--field: must be a positive integer")

    field_number = args.field
    delimeter = args.delimiter
    filename = args.filename

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
            fields = processed_line.split(delimeter)

            try:
                if field_number -1 < len(fields):
                     print(fields[field_number - 1])
                else:
                     print() # Or print("", file=sys.stderr) to indicate missing field

            except IndexError:
                 print() # Print empty line for lines that don't have the field

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
