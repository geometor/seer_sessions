```python
import math # not strictly needed for this task, but included as per template example

# Helper functions

def parse_input_string(input_str: str) -> list[int]:
    """Parses a space-separated string of digits into a list of integers."""
    return [int(digit) for digit in input_str.split()]

def format_output_list(output_list: list[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    return " ".join(map(str, output_list))

# Main transformation function

def transform(input_str: str) -> str:
    """
    Takes a sequence of 12 space-separated digits, splits it into two parts
    (the first 8 digits and the last 4 digits), and returns a new sequence
    formed by concatenating the last 4 digits followed by the first 8 digits.
    """

    # Parse the input string into a list of numbers
    numbers = parse_input_string(input_str)

    # Define the split point
    split_index = 8

    # Check if the input list has the expected length (optional, for robustness)
    if len(numbers) != 12:
        # Handle error or unexpected input length if necessary
        # For this task, we assume valid input based on examples
        pass 

    # Split the list into two parts based on the split index
    part1 = numbers[:split_index] # First 8 elements
    part2 = numbers[split_index:] # Last 4 elements

    # Concatenate the parts in the reverse order: part2 then part1
    rearranged_list = part2 + part1

    # Format the rearranged list back into a space-separated string
    output_str = format_output_list(rearranged_list)

    return output_str

```