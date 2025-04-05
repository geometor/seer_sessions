"""
Transforms an input string representing a sequence of 12 space-separated digits.
The transformation rule is as follows:
1. Parse the input string into a list of 12 integers.
2. Keep the first four digits unchanged (expected to be [0, 0, 0, 0]).
3. Identify the unique non-zero digit (X) within the digits from index 4 to 11.
4. Replace the digits from index 4 to 11 with a fixed pattern using the identified digit X: [X, X, X, 0, X, X, 0, X].
5. Format the resulting 12-digit list back into a space-separated string.
"""

from typing import List

# === Helper Functions ===

def parse_input_string(input_str: str) -> List[int]:
    """Parses a space-separated string of digits into a list of integers."""
    try:
        # Split the string by spaces and convert each part to an integer
        parsed_list = [int(digit) for digit in input_str.split()]
        # Validate that exactly 12 digits were parsed
        if len(parsed_list) != 12:
            raise ValueError(f"Input string '{input_str}' did not parse into exactly 12 digits.")
        return parsed_list
    except ValueError as e:
        # Re-raise exceptions related to non-integer parts or incorrect count
        raise ValueError(f"Error parsing input string: {e}")

def find_unique_non_zero(sub_list: List[int]) -> int:
    """Finds the unique non-zero digit in a list segment."""
    non_zero_digit = None
    # Iterate through the sub-list to find the non-zero digit
    for digit in sub_list:
        if digit != 0:
            # Check if we already found a different non-zero digit (optional, based on problem constraints)
            # if non_zero_digit is not None and non_zero_digit != digit:
            #     raise ValueError("Multiple distinct non-zero digits found in segment.")
            non_zero_digit = digit
            # Assuming only one unique non-zero digit exists based on examples,
            # we could break here, but iterating fully confirms uniqueness implicitly if no error is raised later.
            # We actually just need the *first* non-zero found based on the pattern.
            break 
            
    # Check if a non-zero digit was actually found
    if non_zero_digit is None:
        raise ValueError("No non-zero digit found in the relevant segment (indices 4-11).")
    return non_zero_digit

def format_output_list(output_list: List[int]) -> str:
    """Formats a list of integers into a space-separated string."""
    # Convert each integer back to a string and join with spaces
    return " ".join(map(str, output_list))

# === Main Transformation Function ===

def transform(input_grid: str) -> str:
    """
    Applies the sequence transformation rule to the input string.

    Args:
        input_grid: A string containing 12 space-separated digits.

    Returns:
        A string containing the transformed 12 space-separated digits.
    """
    # Step 1: Parse the input string into a list of integers
    input_list = parse_input_string(input_grid)
    
    # Step 2: The first four digits remain [0, 0, 0, 0] (implicitly handled by slice later)
    # output_list = [0] * 12 # Initialize output (optional, can build directly)

    # Step 3: Identify the unique non-zero digit (X) in the segment from index 4 to 11
    variable_segment = input_list[4:12]
    non_zero_x = find_unique_non_zero(variable_segment)

    # Step 4: Construct the target pattern segment using X: [X, X, X, 0, X, X, 0, X]
    target_pattern_segment = [
        non_zero_x, non_zero_x, non_zero_x, 0,
        non_zero_x, non_zero_x, 0, non_zero_x
    ]

    # Step 5: Combine the initial segment with the new pattern segment
    # The first 4 elements are taken directly from the input (assumed [0,0,0,0])
    final_output_list = input_list[0:4] + target_pattern_segment

    # Step 6: Format the final list back into a space-separated string
    output_string = format_output_list(final_output_list)

    # Return the result
    return output_string
