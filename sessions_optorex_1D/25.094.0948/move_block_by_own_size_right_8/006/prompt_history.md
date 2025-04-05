
## train_1

**input:**
```
0 0 0 0 0 0 1 1 1 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 1 1 1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 9 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 0
```


## train_3

**input:**
```
0 0 0 9 9 9 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 9 9 9 0 0 0
```


## train_4

**input:**
```
0 0 0 0 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 4 4 4 4
```


## train_5

**input:**
```
0 0 0 7 7 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 7 7 7 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 3 3 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 3 3
```


## train_7

**input:**
```
0 0 9 9 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 9 9 0 0 0 0 0 0
```

## Perception of Task Elements

The task involves transforming a sequence of 12 digits. Each input sequence contains a single contiguous block of identical non-zero digits, surrounded by zeros. The output sequence consists of the same block of non-zero digits, shifted to the right within the sequence, with the remaining positions filled with zeros. The amount of the rightward shift is equal to the length of the non-zero block.

## Task Facts


```yaml
task_elements:
  - type: sequence
    description: Input is a sequence of 12 digits.
    properties:
      length: 12
      composition: Contains zeros and a single contiguous block of identical non-zero digits.
  - type: block
    description: A contiguous sub-sequence of identical non-zero digits within the input sequence.
    properties:
      - digit_value: The non-zero digit repeated in the block (e.g., 1, 9, 4, 7, 3).
      - length: The number of digits in the block.
      - start_index: The position (0-based index) where the block begins in the input sequence.
  - type: transformation
    description: The process applied to the input sequence to produce the output sequence.
    action:
      - identify: Locate the non-zero block in the input sequence.
      - measure: Determine the length of the identified block.
      - shift: Move the block to the right within the sequence.
      - fill: Place zeros in all positions not occupied by the shifted block.
    relationship:
      - The shift distance is equal to the length of the non-zero block.
  - type: sequence
    description: Output is a sequence of 12 digits.
    properties:
      length: 12
      composition: Contains zeros and the same non-zero block from the input, shifted rightward.
      - shifted_start_index: The new starting position of the block (original start_index + block length).
```


## Natural Language Program

1.  Receive the input sequence of 12 digits.
2.  Initialize an output sequence of 12 zeros.
3.  Iterate through the input sequence to find the first non-zero digit. Record its value (`digit_value`) and its index (`start_index`).
4.  Continue iterating from `start_index` to find the end of the contiguous block of `digit_value`. Calculate the length of this block (`block_length`).
5.  Calculate the new starting index for the block in the output sequence: `new_start_index = start_index + block_length`.
6.  Place the block of `digit_value` with length `block_length` into the output sequence, starting at `new_start_index`.
7.  Return the modified output sequence.
```python
import re

"""
Transforms a sequence of 12 digits by identifying a single contiguous block of 
identical non-zero digits and shifting this block to the right by a distance 
equal to its own length. The remaining positions are filled with zeros.
"""

def find_block(input_sequence):
    """
    Finds the start index, digit value, and length of the non-zero block.

    Args:
        input_sequence: The input string sequence.

    Returns:
        A tuple (start_index, digit_value, block_length) if a block is found,
        otherwise None.
    """
    start_index = -1
    digit_value = '0'
    block_length = 0

    # Iterate through the sequence to find the start of the block
    for i, char in enumerate(input_sequence):
        if char != '0':
            start_index = i
            digit_value = char
            break

    # If no non-zero digit was found, return None
    if start_index == -1:
        return None

    # Count the length of the block starting from start_index
    for i in range(start_index, len(input_sequence)):
        if input_sequence[i] == digit_value:
            block_length += 1
        else:
            # Stop counting when a different digit or zero is encountered
            break
            
    return start_index, digit_value, block_length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid string.

    Args:
        input_grid: A string representing the sequence of 12 digits.

    Returns:
        A string representing the transformed sequence.
    """
    # Ensure input is treated as a string sequence
    input_sequence = str(input_grid)
    sequence_length = len(input_sequence)

    # Initialize the output sequence with zeros
    output_sequence = ['0'] * sequence_length

    # Find the non-zero block details
    block_info = find_block(input_sequence)

    # If no block is found (e.g., all zeros), return the initialized output
    if block_info is None:
        return "".join(output_sequence)

    start_index, digit_value, block_length = block_info

    # Calculate the new starting index for the block
    # Ensure the shift calculation is correct based on the start and length
    new_start_index = start_index + block_length

    # Place the block into the output sequence at the new position
    # Ensure the block fits within the sequence bounds
    end_index = new_start_index + block_length
    if new_start_index < sequence_length:
        for i in range(new_start_index, min(end_index, sequence_length)):
             output_sequence[i] = digit_value

    # Convert the list back to a string and return
    return "".join(output_sequence)

```
```python
import re

"""
Transforms a sequence of 12 digits by identifying a single contiguous block of 
identical non-zero digits and shifting this block to the right by a distance 
equal to its own length. The input may contain spaces, which are removed 
before processing. The output is formatted as a space-separated string.
"""

def find_block(digit_sequence):
    """
    Finds the start index, digit value, and length of the first contiguous 
    block of identical non-zero digits in a sequence.

    Args:
        digit_sequence: A string containing only digits.

    Returns:
        A tuple (start_index, digit_value, block_length) if a block is found,
        otherwise None. Returns None if the sequence contains only zeros.
    """
    start_index = -1
    digit_value = '0'
    block_length = 0

    # Find the start of the first non-zero block
    for i, char in enumerate(digit_sequence):
        if char != '0':
            start_index = i
            digit_value = char
            break

    # If no non-zero digit was found (all zeros), return None
    if start_index == -1:
        return None

    # Count the length of the block starting from start_index
    # Ensure we only count contiguous identical digits
    for i in range(start_index, len(digit_sequence)):
        if digit_sequence[i] == digit_value:
            block_length += 1
        else:
            # Stop counting when a different digit or zero is encountered
            break
            
    return start_index, digit_value, block_length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid string.

    Args:
        input_grid: A string or other representation of the sequence of 12 digits, 
                    potentially containing spaces or other characters.

    Returns:
        A string representing the transformed sequence, with digits separated by spaces.
    """
    # 1. Convert input to string and preprocess
    input_string = str(input_grid)
    # Remove spaces and any other non-digit characters
    cleaned_sequence = "".join(filter(str.isdigit, input_string))

    # Ensure the cleaned sequence has the expected length (12)
    # If not, this might indicate an unexpected input format. 
    # For robustness, we'll proceed but it might lead to errors if length is wrong.
    # A more robust solution might raise an error or return a default state.
    sequence_length = 12 # Assuming fixed length based on examples

    # 2. Initialize output grid (as a list of characters)
    output_list = ['0'] * sequence_length

    # 3. Find the non-zero block in the cleaned sequence
    block_info = find_block(cleaned_sequence)

    # 4. If a block is found, calculate the shift and modify the output list
    if block_info:
        start_index, digit_value, block_length = block_info

        # Calculate the new starting index for the block
        new_start_index = start_index + block_length

        # Place the block into the output list at the new position
        # Ensure the block fits within the sequence bounds
        # Calculate the actual end index in the output list
        output_end_index = new_start_index + block_length 
        
        for i in range(new_start_index, min(output_end_index, sequence_length)):
             # Check index is within bounds before assignment
             if i < sequence_length:
                 output_list[i] = digit_value

    # 5. Format the output list into a space-separated string
    output_grid = " ".join(output_list)

    return output_grid
```
```python
import re

"""
Transforms a sequence of 12 digits, provided as a space-separated string,
by identifying a single contiguous block of identical non-zero digits
and shifting this block to the right by a distance equal to its own length.
The remaining positions are filled with zeros, and the output is returned
as a space-separated string.
"""

def find_non_zero_block(digit_sequence):
    """
    Finds the start index, digit value, and length of the first contiguous
    block of identical non-zero digits in a sequence.

    Args:
        digit_sequence: A string containing only digits (e.g., "000111000").

    Returns:
        A tuple (start_index, digit_value, block_length) if a block is found.
        Returns None if the sequence contains only zeros or no valid block.
    """
    start_index = -1
    digit_value = '0'
    block_length = 0

    # Find the start of the first non-zero block
    for i, char in enumerate(digit_sequence):
        # Check if the character is a non-zero digit
        if char != '0' and '1' <= char <= '9':
            start_index = i
            digit_value = char
            break

    # If no non-zero digit was found (e.g., all zeros), return None
    if start_index == -1:
        return None

    # Count the length of the contiguous block starting from start_index
    # Ensure we only count contiguous identical non-zero digits
    for i in range(start_index, len(digit_sequence)):
        if digit_sequence[i] == digit_value:
            block_length += 1
        else:
            # Stop counting when a different digit (or zero) is encountered
            break

    # Basic validation: if block_length is 0 after finding a start, something is wrong
    # but the logic above should prevent this unless the sequence is empty or malformed.
    if block_length == 0:
         return None # Should not happen with valid non-zero start found

    return start_index, digit_value, block_length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid string.

    Args:
        input_grid: A string representing the sequence of 12 digits,
                    separated by spaces (e.g., "0 0 0 1 1 1 0 0 0 0 0 0").

    Returns:
        A string representing the transformed sequence, with digits
        separated by spaces (e.g., "0 0 0 0 0 0 1 1 1 0 0 0").
        Returns a default zero string if input is invalid or has no block.
    """
    # Define the expected length of the digit sequence
    sequence_length = 12
    default_output = " ".join(['0'] * sequence_length)

    # --- Step 1 & 2: Preprocess Input ---
    # Ensure input is treated as a string
    input_string = str(input_grid)
    # Remove spaces to get the pure digit sequence
    cleaned_sequence = "".join(input_string.split())

    # Validate the length of the cleaned sequence
    if len(cleaned_sequence) != sequence_length:
        # Handle invalid input length - return default or raise error
        # For this task, returning default zero sequence seems reasonable
        # print(f"Warning: Input sequence length is not {sequence_length} after cleaning: '{cleaned_sequence}'")
        return default_output
    # Validate if sequence contains only digits 0-9
    if not cleaned_sequence.isdigit():
        # print(f"Warning: Input sequence contains non-digit characters after cleaning: '{cleaned_sequence}'")
        return default_output


    # --- Step 3: Initialize Output ---
    # Create an output list initialized with zeros
    output_list = ['0'] * sequence_length

    # --- Step 4 & 5: Find the Non-Zero Block ---
    # Use the helper function to find the block details
    block_info = find_non_zero_block(cleaned_sequence)

    # --- Step 6 & 7: Calculate Shift and Place Block (if found) ---
    # Proceed only if a valid block was found
    if block_info:
        start_index, digit_value, block_length = block_info

        # Calculate the new starting index for the block in the output
        new_start_index = start_index + block_length

        # Place the block into the output list at the calculated new position
        # Iterate for the length of the block
        for i in range(block_length):
            # Calculate the target index in the output list
            target_index = new_start_index + i
            # IMPORTANT: Check if the target index is within the bounds of the output list
            if target_index < sequence_length:
                output_list[target_index] = digit_value
            # else: block goes partially or fully out of bounds, ignore the out-of-bounds part

    # --- Step 8: Format Output ---
    # Join the characters in the output list using a single space separator
    output_grid_str = " ".join(output_list)

    # --- Step 9: Return Result ---
    return output_grid_str
```
