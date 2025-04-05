import math # Although '//' handles floor, importing might be convention

"""
Transforms a sequence of space-separated integers (or an iterable of numbers) 
based on contiguous blocks of the value '2'. For each contiguous block of '2's 
with length L, the first floor(L/2) elements of that block are changed to '8' 
in the output sequence. Elements with value 0 remain unchanged and act as 
delimiters for the blocks of '2's. Sequence start and end also act as 
delimiters. The final output is formatted as a space-separated string.
"""

def find_contiguous_block_end(sequence, start_index, value):
  """
  Finds the end index (inclusive) of a contiguous block of a specific value 
  starting from a given index.

  Args:
    sequence: The input sequence (list of standard Python integers).
    start_index: The index where the block starts.
    value: The integer value that defines the block (e.g., 2).

  Returns:
    The index of the last element in the contiguous block.
  """
  current_index = start_index
  # Iterate as long as we are within bounds and the value matches
  while current_index < len(sequence) and sequence[current_index] == value:
    current_index += 1
  # The loop stops *after* the last matching element or at the end of the sequence.
  # So, the end index of the block is the previous index.
  return current_index - 1

def parse_input(input_data):
    """
    Parses the input data (string or iterable) into a list of standard Python integers.
    This is crucial to avoid type issues (e.g., with NumPy scalars).
    
    Args:
        input_data: Can be a space-separated string or an iterable (list, tuple, np.array).

    Returns:
        A list of Python integers.
        
    Raises:
        ValueError: If input contains non-convertible values.
        TypeError: If input type is not supported.
    """
    if isinstance(input_data, str):
        # Split the string by spaces and explicitly convert each part to int
        try:
            # Using int() ensures we get standard Python integers
            return [int(x) for x in input_data.split()]
        except ValueError:
            raise ValueError("Input string contains non-integer values.")
    # Check if it's iterable but not a string/bytes (covers lists, tuples, np.arrays)
    elif hasattr(input_data, '__iter__') and not isinstance(input_data, (str, bytes)):
        try:
            # Explicitly cast each element to int
            return [int(x) for x in input_data]
        except ValueError:
             raise ValueError("Input sequence contains non-integer values.")
    else:
        raise TypeError("Input must be a space-separated string or an iterable of numbers.")


def format_output(output_sequence):
    """Formats the list of integers back into a space-separated string."""
    # Convert each integer back to string before joining
    return " ".join(map(str, output_sequence))

def transform(input_grid):
    """
    Applies the transformation rule to the input sequence.

    Args:
      input_grid: A string of space-separated integers (e.g., "2 2 0 2") 
                  or an iterable sequence of numbers.

    Returns:
      A string of space-separated integers representing the transformed sequence.
    """
    # 1. Parse Input: Convert input into a list of standard Python integers
    # This step is vital to ensure elements are comparable as integers.
    input_sequence = parse_input(input_grid)
    
    # 2. Initialize Output: Create a modifiable copy of the parsed sequence
    output_sequence = list(input_sequence)
    n = len(input_sequence)
    i = 0 # Initialize pointer/index for scanning the sequence

    # 3. Iterate and Identify Blocks: Scan the input sequence
    while i < n:
        # Get the current value (guaranteed to be a Python int after parsing)
        current_value = input_sequence[i] 
        
        # 4. Handle Delimiters (0): If the value is 0, do nothing and move on
        if current_value == 0:
            i += 1
        # 5. Process Blocks of '2's: If the value is 2, find the block
        elif current_value == 2:
            # a. Mark start index of the block
            start_idx = i
            
            # b. Find the end index (inclusive) of this block of 2s
            end_idx = find_contiguous_block_end(input_sequence, start_idx, 2)

            # c. Calculate the length of the block
            block_length = end_idx - start_idx + 1

            # d. Calculate the number of elements to modify (floor(L/2))
            # Integer division '//' performs floor operation correctly
            num_to_modify = block_length // 2 

            # e. Modify the output list: Change the first 'num_to_modify' 
            #    elements of this block in the *output* sequence to 8
            for k in range(start_idx, start_idx + num_to_modify):
                output_sequence[k] = 8

            # f. Advance the main scanner index 'i' to the position immediately 
            #    *after* the block we just processed to avoid re-processing
            i = end_idx + 1
        # 6. Handle Unexpected Values (Optional): Although the problem implies
        #    only 0s and 2s, robust code might skip other values.
        else:
            # For this problem, this case likely won't occur based on examples.
            # If it did, we'd just move to the next element.
            i += 1
            
    # 7. Format Output: Convert the result list back to a space-separated string
    formatted_output = format_output(output_sequence)

    # 8. Return: Return the final formatted string
    return formatted_output