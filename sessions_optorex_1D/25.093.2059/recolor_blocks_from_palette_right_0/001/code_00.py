"""
Transforms a sequence of integers based on specific rules:
1. Parses the input string into a list of integers.
2. Identifies all non-zero integers except for 5, preserving their order. These form the 'replacement pool'.
3. Initializes an output list as a copy of the input list.
4. Iterates through the input list:
    - If the current number is 5:
        - Determine if this is the start of a consecutive sequence of 5s.
        - If it's the start, advance to the next replacement value from the pool.
        - Replace the 5 in the output list with the current replacement value.
    - If the current number is not 5 (i.e., 0 or another non-5 number), it remains unchanged in the output list (already handled by the initial copy).
5. Converts the transformed list of integers back into a space-separated string.
"""

import re

def get_replacement_pool(numbers):
  """
  Extracts non-zero, non-5 numbers from a list, preserving order.
  """
  pool = []
  for num in numbers:
    if num != 0 and num != 5:
      pool.append(num)
  return pool

def transform(input_str):
    """
    Applies the transformation rule to the input string sequence.
    """
    # Parse the input string into a list of integers
    try:
        input_list = [int(x) for x in input_str.split()]
    except ValueError:
        # Handle cases where input might not be space-separated integers
        print(f"Error: Input string '{input_str}' contains non-integer values or incorrect formatting.")
        return "" # Or raise an error

    # Initialize the output list as a copy of the input
    output_list = list(input_list)

    # Identify the pool of numbers to use for replacing 5s
    replacement_pool = get_replacement_pool(input_list)

    # Keep track of which replacement number to use
    five_sequence_index = -1 # Will be incremented to 0 for the first sequence

    # Iterate through the input list and modify the output list
    for i in range(len(input_list)):
        current_num = input_list[i]

        # Process sequences of 5s
        if current_num == 5:
            # Check if this is the start of a new sequence of 5s
            is_start_of_sequence = (i == 0 or input_list[i-1] != 5)

            if is_start_of_sequence:
                # Move to the next replacement value
                five_sequence_index += 1

            # Get the replacement value for the current sequence
            # Handle potential index errors if there aren't enough replacement numbers
            if five_sequence_index < len(replacement_pool):
                replacement_value = replacement_pool[five_sequence_index]
                output_list[i] = replacement_value
            else:
                # Decide how to handle insufficient replacement numbers
                # Option 1: Error out
                # raise IndexError(f"Not enough non-zero/non-5 numbers in input to replace all sequences of 5. Input: {input_str}")
                # Option 2: Use a default value (e.g., 0 or keep 5) - let's keep 5 for now
                # output_list[i] = 5 # Or 0, or handle differently
                print(f"Warning: Not enough replacement values for sequence starting at index {i}. Keeping original 5.")
                pass # Keep original 5 if pool exhausted

        # Non-5 numbers (0s and others) are already correctly placed in output_list
        # because it was initialized as a copy of input_list.

    # Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    return output_str
