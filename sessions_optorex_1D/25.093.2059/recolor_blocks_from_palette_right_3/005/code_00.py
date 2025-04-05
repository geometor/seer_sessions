import re
from typing import List

# Constants for magic numbers
PLACEHOLDER_VALUE = 5
IGNORE_VALUE = 0

def find_source_values(numbers: List[int]) -> List[int]:
    """
    Extracts non-zero, non-placeholder numbers from the input list,
    preserving their order.
    """
    return [num for num in numbers if num != IGNORE_VALUE and num != PLACEHOLDER_VALUE]

def transform_sequence(input_nums: List[int], source_values: List[int]) -> List[int]:
    """
    Applies the transformation rule to the sequence of numbers.
    """
    output_sequence = []
    source_index = -1  # Index for the current source value being used
    processing_fives_group = False # Flag to track if we are inside a consecutive group of 5s

    # Iterate through the input sequence
    for current_number in input_nums:
        # Check if the current number is the placeholder value (5)
        if current_number == PLACEHOLDER_VALUE:
            # Check if this is the start of a new group of 5s
            if not processing_fives_group:
                processing_fives_group = True
                # Move to the next source value for this new group
                source_index += 1
            
            # Retrieve the appropriate source value for the current group
            # Add error handling in case source_values is shorter than expected groups
            if source_index < len(source_values):
                replacement_value = source_values[source_index]
            else:
                # Fallback or error: Use placeholder if not enough source values
                # Based on examples, this shouldn't happen, but good practice.
                replacement_value = PLACEHOLDER_VALUE 
                
            # Append the replacement value to the output
            output_sequence.append(replacement_value)
        else:
            # If the current number is not 5, the group of 5s (if any) ends
            processing_fives_group = False
            # Append the original number (0 or a source value) to the output
            output_sequence.append(current_number)
            
    return output_sequence

def transform(input_str: str) -> str:
    """
    Transforms an input string of space-separated integers based on the rule:
    1. Identifies non-zero, non-5 integers as ordered 'source values'.
    2. Identifies consecutive sequences of '5's as 'target groups'.
    3. Replaces all integers within the Nth target group with the Nth source value.
    4. Keeps all other numbers (0s and original source values) unchanged.
    """
    
    # 1. Parse the input string into a sequence of integers.
    try:
        input_nums = [int(x) for x in input_str.split()]
    except ValueError:
        # Handle cases where input might not be valid integers
        print(f"Error: Input string '{input_str}' contains non-integer values.")
        return "" # Or raise an exception

    # 2. Create an ordered list of source values.
    source_values = find_source_values(input_nums)

    # 3-7. Apply the transformation logic using a helper function.
    output_sequence = transform_sequence(input_nums, source_values)

    # 8. Convert the output sequence back into a space-separated string.
    output_str = " ".join(map(str, output_sequence))

    return output_str
