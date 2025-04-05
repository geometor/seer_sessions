```python
import re

def parse_input(input_str):
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.strip().split()]

def format_output(output_list):
    """Formats the list of integers into a space-separated string."""
    return ' '.join(map(str, output_list))

def rotate_left_once(int_list):
    """Rotates the list one position to the left."""
    if not int_list:
        return []
    # Store the first element
    first_element = int_list[0]
    # Get the remaining elements
    remaining_elements = int_list[1:]
    # Append the first element to the end of the remaining elements
    rotated_list = remaining_elements + [first_element]
    return rotated_list

def transform(input_str):
    """
    Transforms the input sequence by moving the first integer to the end.

    1. Read the input sequence of integers.
    2. Identify and store the first integer in the sequence.
    3. Create a new sequence containing all integers from the input sequence
       starting from the second integer up to the last one, maintaining
       their original relative order.
    4. Append the stored first integer to the end of this new sequence.
    5. The resulting sequence is the output.
    """
    # Parse the input string into a list of integers
    input_list = parse_input(input_str)

    # Perform the left rotation
    output_list = rotate_left_once(input_list)

    # Format the output list back into a space-separated string
    output_str = format_output(output_list)

    return output_str

```