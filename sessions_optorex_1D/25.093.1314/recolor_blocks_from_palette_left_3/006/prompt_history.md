
## train_1

**input:**
```
0 5 5 5 0 5 5 5 0 0 8 5
```


**output:**
```
0 8 8 8 0 5 5 5 0 0 8 5
```


## train_2

**input:**
```
0 0 5 5 0 0 5 5 0 0 3 5
```


**output:**
```
0 0 3 3 0 0 5 5 0 0 3 5
```


## train_3

**input:**
```
5 5 0 0 0 0 0 5 5 0 7 9
```


**output:**
```
7 7 0 0 0 0 0 9 9 0 7 9
```


## train_4

**input:**
```
0 0 5 5 0 0 5 5 0 0 8 5
```


**output:**
```
0 0 8 8 0 0 5 5 0 0 8 5
```


## train_5

**input:**
```
0 5 5 5 0 5 5 5 0 0 5 7
```


**output:**
```
0 5 5 5 0 7 7 7 0 0 5 7
```


## train_6

**input:**
```
5 5 0 0 0 0 5 5 0 0 9 8
```


**output:**
```
9 9 0 0 0 0 8 8 0 0 9 8
```


## train_7

**input:**
```
5 5 5 0 0 5 5 5 0 0 3 8
```


**output:**
```
3 3 3 0 0 8 8 8 0 0 3 8
```

*   **Perception of Elements:**
    *   The input and output are sequences of 12 integers.
    *   The core operation involves identifying and replacing specific values within the sequence.
    *   The value `5` appears to be the target value for replacement within the initial part of the sequence (first 10 elements).
    *   The last two elements of the input sequence (at index 10 and 11) act as replacement values. Let's call them `val1` and `val2`, respectively.
    *   The transformation identifies contiguous blocks of the target value (`5`) within the first 10 elements.
    *   The *first* such block found is replaced using `val1`.
    *   The *second* such block found is replaced using `val2`.
    *   If only one block of `5`s exists, it is treated as the first block and replaced with `val1`.
    *   If no blocks of `5`s exist, or if only one block exists and a second replacement is attempted, no further changes occur for that specific replacement step.
    *   The last two elements of the sequence remain unchanged in the output.

*   **YAML Facts:**
    
```yaml
    task_description: Replace blocks of a specific target value within a sequence using values derived from the end of the sequence.
    input_elements:
      - name: input_sequence
        type: list of integers
        length: 12
        properties: Contains numbers, potentially including blocks of the target value and the replacement values.
    output_elements:
      - name: output_sequence
        type: list of integers
        length: 12
        properties: Derived from input_sequence by replacing target blocks.
    constants:
      - name: target_value
        value: 5
        description: The integer value to be replaced in blocks.
      - name: sequence_prefix_length
        value: 10
        description: The length of the initial part of the sequence where replacements occur.
    derived_values:
      - name: replacement_value_1
        source: input_sequence[10]
        description: The value used to replace the first block of target_value.
      - name: replacement_value_2
        source: input_sequence[11]
        description: The value used to replace the second block of target_value.
    actions:
      - name: identify_blocks
        input: input_sequence (first 10 elements), target_value
        output: List of start and end indices for contiguous blocks of target_value.
        description: Finds consecutive occurrences of the target_value.
      - name: replace_block
        input: sequence, block_indices, replacement_value
        output: modified_sequence
        description: Replaces the elements within the specified block indices with the replacement_value.
    relationships:
      - The last two elements of the input_sequence determine the replacement values.
      - Replacements only happen within the first 10 elements of the input_sequence.
      - The first identified block of target_value is replaced by replacement_value_1.
      - The second identified block of target_value is replaced by replacement_value_2.
      - Elements not part of the identified blocks or outside the first 10 positions remain unchanged relative to the input (unless they were part of a block that got replaced).
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of 12 integers.
    2.  Identify the two replacement values: `val1` is the element at index 10, and `val2` is the element at index 11.
    3.  Initialize the output sequence as a copy of the input sequence.
    4.  Scan the first 10 elements (indices 0 through 9) of the sequence to find contiguous blocks where all elements are equal to `5`. Keep track of the start and end indices of these blocks.
    5.  If at least one block of `5`s is found:
        a.  Take the first block identified (the one with the smallest starting index).
        b.  Replace every element within this first block in the output sequence with `val1`.
    6.  If at least two blocks of `5`s are found:
        a.  Take the second block identified (the one with the second smallest starting index).
        b.  Replace every element within this second block in the output sequence with `val2`.
    7.  Return the modified output sequence.
```python
import math
import re

"""
Replace blocks of a specific target value (5) within the first 10 elements of a sequence using values derived from the end of the sequence. The value at index 10 replaces the first block of 5s, and the value at index 11 replaces the second block of 5s.
"""

def find_target_blocks(sequence, target, length):
    """
    Finds contiguous blocks of the target value within the specified length of the sequence.

    Args:
        sequence: The list of integers to search within.
        target: The integer value to find blocks of.
        length: The number of elements from the start of the sequence to search.

    Returns:
        A list of tuples, where each tuple represents a block and contains
        the (start_index, end_index_exclusive) of the block.
    """
    blocks = []
    in_block = False
    start_index = -1
    for i in range(length):
        is_target = sequence[i] == target
        # Start of a new block
        if is_target and not in_block:
            in_block = True
            start_index = i
        # End of the current block (found a non-target value)
        elif not is_target and in_block:
            in_block = False
            blocks.append((start_index, i))
            start_index = -1

    # Check if a block was ongoing until the very end of the specified length
    if in_block:
        blocks.append((start_index, length))

    return blocks

def transform(input_list):
    """
    Transforms the input list by replacing blocks of 5s in the first 10 elements.
    The first block is replaced by the element at index 10.
    The second block is replaced by the element at index 11.

    Args:
        input_list: A list of 12 integers.

    Returns:
        A new list of 12 integers with the replacements performed.
    """
    # Constants and derived values
    target_value = 5
    sequence_prefix_length = 10

    # Ensure input has the expected length, otherwise return it unchanged or raise error
    if len(input_list) != 12:
        # Or raise ValueError("Input list must have exactly 12 elements")
        return input_list 

    replacement_value_1 = input_list[10]
    replacement_value_2 = input_list[11]

    # Initialize output_list as a copy of the input
    output_list = list(input_list)

    # Find blocks of the target value within the defined prefix length
    blocks_of_5 = find_target_blocks(output_list, target_value, sequence_prefix_length)

    # Replace the first block if it exists
    if len(blocks_of_5) >= 1:
        start1, end1 = blocks_of_5[0]
        for i in range(start1, end1):
            output_list[i] = replacement_value_1

    # Replace the second block if it exists
    if len(blocks_of_5) >= 2:
        start2, end2 = blocks_of_5[1]
        for i in range(start2, end2):
            output_list[i] = replacement_value_2

    return output_list

# Example Usage (using train_1 input format for parsing)
# input_str = "0 5 5 5 0 5 5 5 0 0 8 5"
# input_list_int = [int(x) for x in input_str.split()]
# output_list_int = transform(input_list_int)
# print(output_list_int) # Expected: [0, 8, 8, 8, 0, 5, 5, 5, 0, 0, 8, 5] - Wait, example 1 output is different. Let's re-read.

# Re-reading the examples and description...
# Example 1: input: 0 5 5 5 0 5 5 5 0 0 8 5 -> output: 0 8 8 8 0 5 5 5 0 0 8 5.  My code would replace the second block (5 5 5 at index 5) with 5. This doesn't match.
# Example 5: input: 0 5 5 5 0 5 5 5 0 0 5 7 -> output: 0 5 5 5 0 7 7 7 0 0 5 7. My code would replace the first block (5 5 5 at index 1) with 5. This doesn't match.
# Example 7: input: 5 5 5 0 0 5 5 5 0 0 3 8 -> output: 3 3 3 0 0 8 8 8 0 0 3 8. My code replaces correctly here.

# Ah, I see the discrepancy. My initial interpretation was slightly off.
# The NL program:
# 5a. Take the first block identified (the one with the smallest starting index). Replace every element within this first block in the output sequence with val1.
# 6a. Take the second block identified (the one with the second smallest starting index). Replace every element within this second block in the output sequence with val2.
# This is what the code does. Let's re-check the examples against this logic.

# train_1: input: 0 5 5 5 0 5 5 5 0 0 8 5
#   val1=8, val2=5
#   Blocks of 5: (1, 4), (5, 8)
#   Replace block (1, 4) with 8 -> 0 8 8 8 0 5 5 5 0 0 8 5
#   Replace block (5, 8) with 5 -> 0 8 8 8 0 5 5 5 0 0 8 5
#   Output: 0 8 8 8 0 5 5 5 0 0 8 5.  This *matches* the desired output `0 8 8 8 0 5 5 5 0 0 8 5`. Okay, my previous re-read was confused.

# train_2: input: 0 0 5 5 0 0 5 5 0 0 3 5
#   val1=3, val2=5
#   Blocks of 5: (2, 4), (6, 8)
#   Replace block (2, 4) with 3 -> 0 0 3 3 0 0 5 5 0 0 3 5
#   Replace block (6, 8) with 5 -> 0 0 3 3 0 0 5 5 0 0 3 5
#   Output: 0 0 3 3 0 0 5 5 0 0 3 5. This *matches* the desired output `0 0 3 3 0 0 5 5 0 0 3 5`.

# train_3: input: 5 5 0 0 0 0 0 5 5 0 7 9
#   val1=7, val2=9
#   Blocks of 5: (0, 2), (7, 9)
#   Replace block (0, 2) with 7 -> 7 7 0 0 0 0 0 5 5 0 7 9
#   Replace block (7, 9) with 9 -> 7 7 0 0 0 0 0 9 9 0 7 9
#   Output: 7 7 0 0 0 0 0 9 9 0 7 9. This *matches* the desired output `7 7 0 0 0 0 0 9 9 0 7 9`.

# train_4: input: 0 0 5 5 0 0 5 5 0 0 8 5
#   val1=8, val2=5
#   Blocks of 5: (2, 4), (6, 8)
#   Replace block (2, 4) with 8 -> 0 0 8 8 0 0 5 5 0 0 8 5
#   Replace block (6, 8) with 5 -> 0 0 8 8 0 0 5 5 0 0 8 5
#   Output: 0 0 8 8 0 0 5 5 0 0 8 5. This *matches* the desired output `0 0 8 8 0 0 5 5 0 0 8 5`.

# train_5: input: 0 5 5 5 0 5 5 5 0 0 5 7
#   val1=5, val2=7
#   Blocks of 5: (1, 4), (5, 8)
#   Replace block (1, 4) with 5 -> 0 5 5 5 0 5 5 5 0 0 5 7
#   Replace block (5, 8) with 7 -> 0 5 5 5 0 7 7 7 0 0 5 7
#   Output: 0 5 5 5 0 7 7 7 0 0 5 7. This *matches* the desired output `0 5 5 5 0 7 7 7 0 0 5 7`. Okay, my previous re-read was *definitely* confused.

# train_6: input: 5 5 0 0 0 0 5 5 0 0 9 8
#   val1=9, val2=8
#   Blocks of 5: (0, 2), (6, 8)
#   Replace block (0, 2) with 9 -> 9 9 0 0 0 0 5 5 0 0 9 8
#   Replace block (6, 8) with 8 -> 9 9 0 0 0 0 8 8 0 0 9 8
#   Output: 9 9 0 0 0 0 8 8 0 0 9 8. This *matches* the desired output `9 9 0 0 0 0 8 8 0 0 9 8`.

# train_7: input: 5 5 5 0 0 5 5 5 0 0 3 8
#   val1=3, val2=8
#   Blocks of 5: (0, 3), (5, 8)
#   Replace block (0, 3) with 3 -> 3 3 3 0 0 5 5 5 0 0 3 8
#   Replace block (5, 8) with 8 -> 3 3 3 0 0 8 8 8 0 0 3 8
#   Output: 3 3 3 0 0 8 8 8 0 0 3 8. This *matches* the desired output `3 3 3 0 0 8 8 8 0 0 3 8`.

It seems the initial code implementation was correct according to the NL program and the examples provided. The confusion was during my manual re-checking. The code should work as intended.

```python
import math # Included as per template, though not strictly needed here
import re   # Included as per template, though not strictly needed here

"""
Replace blocks of a specific target value (5) within the first 10 elements of a sequence using values derived from the end of the sequence. 
The value at index 10 replaces the first identified contiguous block of 5s.
The value at index 11 replaces the second identified contiguous block of 5s.
Replacements only occur within the first 10 elements (indices 0-9).
The last two elements remain unchanged.
"""

def find_target_blocks(sequence, target, length):
    """
    Finds contiguous blocks of the target value within the specified length of the sequence.

    Args:
        sequence: The list of integers to search within.
        target: The integer value to find blocks of.
        length: The number of elements from the start of the sequence to search.

    Returns:
        A list of tuples, where each tuple represents a block and contains
        the (start_index, end_index_exclusive) of the block. Blocks are ordered
        by their start_index.
    """
    blocks = []
    in_block = False
    start_index = -1
    # Iterate through the prefix of the sequence
    for i in range(length):
        is_target = sequence[i] == target
        
        # Detect the start of a new block
        if is_target and not in_block:
            in_block = True
            start_index = i
        # Detect the end of the current block (when a non-target is found)
        elif not is_target and in_block:
            in_block = False
            blocks.append((start_index, i)) # end index is exclusive
            start_index = -1 # Reset start index

    # If a block was still ongoing when the loop finished (reached the end of prefix length)
    if in_block:
        blocks.append((start_index, length)) # end index is exclusive (length)

    return blocks

def transform(input_list):
    """
    Transforms the input list by replacing the first two blocks of 5s in the 
    first 10 elements using the values at indices 10 and 11 respectively.

    Args:
        input_list: A list of 12 integers.

    Returns:
        A new list of 12 integers with the specified replacements performed.
    """
    # Define constants based on the observed pattern
    target_value = 5
    sequence_prefix_length = 10
    list_length = 12
    
    # Basic input validation
    if not isinstance(input_list, list) or len(input_list) != list_length:
        # Handle invalid input, e.g., return as is or raise an error
        # print(f"Warning: Input is not a list of length {list_length}. Returning original input.")
        return input_list 

    # Extract the replacement values from the end of the input list
    replacement_value_1 = input_list[10]
    replacement_value_2 = input_list[11]

    # Initialize the output list as a copy of the input list to avoid modifying the original
    output_list = list(input_list)

    # Find all contiguous blocks of the target value within the specified prefix length
    blocks_of_target = find_target_blocks(output_list, target_value, sequence_prefix_length)

    # Replace the elements of the first identified block, if it exists
    if len(blocks_of_target) >= 1:
        start_index_1, end_index_1 = blocks_of_target[0]
        for i in range(start_index_1, end_index_1):
            output_list[i] = replacement_value_1

    # Replace the elements of the second identified block, if it exists
    if len(blocks_of_target) >= 2:
        start_index_2, end_index_2 = blocks_of_target[1]
        for i in range(start_index_2, end_index_2):
            output_list[i] = replacement_value_2

    # Return the modified list
    return output_list
```
```python
import math # common libraries available
import re # common libraries available

"""
Transforms an input sequence of 12 integers. It identifies the first two 
contiguous blocks of the integer '5' within the first 10 elements (indices 0-9). 
The first block found is replaced element-wise by the value at index 10 of the input sequence. 
The second block found (if any) is replaced element-wise by the value at index 11 of the input sequence. 
Elements outside these blocks or outside the first 10 indices remain unchanged, 
including the values at indices 10 and 11.
"""

def find_contiguous_blocks(sequence, target, length):
    """
    Finds contiguous blocks of the target value within the specified length of the sequence.

    Args:
        sequence: The list of integers to search within.
        target: The integer value to find blocks of.
        length: The number of elements from the start of the sequence to search (exclusive index).

    Returns:
        A list of tuples, where each tuple represents a block and contains
        the (start_index, end_index_exclusive) of the block. Blocks are ordered
        by their start_index. Returns an empty list if no blocks are found.
    """
    blocks = []
    in_block = False
    start_index = -1
    # Iterate through the specified prefix of the sequence
    for i in range(length):
        is_target = sequence[i] == target
        
        # Detect the start of a new block of the target value
        if is_target and not in_block:
            in_block = True
            start_index = i
        # Detect the end of the current block (when a non-target is found after being in a block)
        elif not is_target and in_block:
            in_block = False
            blocks.append((start_index, i)) # end index is exclusive
            start_index = -1 # Reset start index for the next potential block

    # If a block was still ongoing when the loop finished (i.e., ended at the 'length' boundary)
    if in_block:
        blocks.append((start_index, length)) # The end index is the exclusive boundary 'length'

    return blocks

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of 12 integers.

    Returns:
        A new list of 12 integers with block replacements applied, or the original 
        list if the input is not a list of length 12.
    """
    
    # --- Configuration ---
    list_length = 12
    target_value = 5
    modification_range_end_exclusive = 10
    replacement_value_1_index = 10
    replacement_value_2_index = 11

    # --- Input Validation ---
    if not isinstance(input_list, list) or len(input_list) != list_length:
        # Consider raising an error or returning None depending on requirements
        print(f"Warning: Input must be a list of {list_length} integers.")
        return input_list # Return original input if invalid

    # --- Initialization ---
    # Create a copy of the input sequence to serve as the working output sequence.
    output_list = list(input_list) 

    # --- Extract Replacement Values ---
    # Identify the first replacement value (val1) from the element at index 10.
    replacement_value_1 = input_list[replacement_value_1_index]
    # Identify the second replacement value (val2) from the element at index 11.
    replacement_value_2 = input_list[replacement_value_2_index]

    # --- Find Target Blocks ---
    # Scan the sequence within the modification range [0, modification_range_end_exclusive) 
    # to find all contiguous blocks of the target_value.
    blocks_found = find_contiguous_blocks(output_list, target_value, modification_range_end_exclusive)

    # --- Apply Replacements ---
    # If one or more blocks were found:
    if len(blocks_found) >= 1:
        # Select the first block found.
        start_index_1, end_index_1 = blocks_found[0]
        # Replace all elements within this first block's index range with replacement_value_1.
        for i in range(start_index_1, end_index_1):
            output_list[i] = replacement_value_1

    # If two or more blocks were found:
    if len(blocks_found) >= 2:
        # Select the second block found.
        start_index_2, end_index_2 = blocks_found[1]
        # Replace all elements within this second block's index range with replacement_value_2.
        for i in range(start_index_2, end_index_2):
            output_list[i] = replacement_value_2
            
    # --- Return Result ---
    # Return the modified output sequence.
    return output_list
```
```python
import math # common libraries available
import re # common libraries available

"""
Transforms an input sequence (list) of 12 integers. It identifies the first two 
contiguous blocks of the integer '5' within the first 10 elements (indices 0-9). 
The first block found is replaced element-wise by the value at index 10 of the 
input sequence. The second block found (if any) is replaced element-wise by the 
value at index 11 of the input sequence. Elements outside these blocks or outside 
the first 10 indices remain unchanged, including the values at indices 10 and 11.
"""

def find_contiguous_blocks(sequence, target, length):
    """
    Finds contiguous blocks of the target value within the specified length of the sequence.

    Args:
        sequence: The list of integers to search within.
        target: The integer value to find blocks of.
        length: The number of elements from the start of the sequence to search (exclusive index).

    Returns:
        A list of tuples, where each tuple represents a block and contains
        the (start_index, end_index_exclusive) of the block. Blocks are ordered
        by their start_index. Returns an empty list if no blocks are found.
    """
    blocks = []
    in_block = False
    start_index = -1
    # Iterate through the specified prefix of the sequence
    for i in range(length):
        is_target = sequence[i] == target
        
        # Detect the start of a new block of the target value
        if is_target and not in_block:
            in_block = True
            start_index = i
        # Detect the end of the current block (when a non-target is found after being in a block)
        elif not is_target and in_block:
            in_block = False
            blocks.append((start_index, i)) # end index is exclusive
            start_index = -1 # Reset start index for the next potential block

    # If a block was still ongoing when the loop finished (i.e., ended at the 'length' boundary)
    if in_block:
        blocks.append((start_index, length)) # The end index is the exclusive boundary 'length'

    return blocks

def transform(input_list):
    """
    Applies the transformation rule to the input list.

    Args:
        input_list: A list of 12 integers.

    Returns:
        A new list of 12 integers with block replacements applied, or the original 
        list if the input is not a list of length 12.
    """
    
    # --- Configuration ---
    # Define constants for the transformation based on observed patterns
    list_length = 12
    target_value = 5
    modification_range_end_exclusive = 10 # Process elements from index 0 up to (but not including) 10
    replacement_value_1_index = 10
    replacement_value_2_index = 11

    # --- Input Validation ---
    # Step 1: Receive the input sequence, expected to be a list of 12 integers. Validate the input length.
    if not isinstance(input_list, list) or len(input_list) != list_length:
        # Handle invalid input - returning the input as-is for robustness
        # Consider raising ValueError("Input must be a list of 12 integers") for stricter handling
        return input_list 

    # --- Initialization ---
    # Step 2: Create a mutable copy of the input sequence to serve as the working output sequence.
    output_list = list(input_list) 

    # --- Extract Replacement Values ---
    # Step 3: Identify the first replacement value (`val1`) from the element at index 10 of the *input* sequence.
    replacement_value_1 = input_list[replacement_value_1_index]
    # Step 4: Identify the second replacement value (`val2`) from the element at index 11 of the *input* sequence.
    replacement_value_2 = input_list[replacement_value_2_index]

    # --- Find Target Blocks ---
    # Step 5: Scan the first 10 elements (indices 0 through 9) of the working output sequence 
    #         to find all contiguous blocks where every element is equal to the target value `5`. 
    #         Record the start/end indices for each block. Store these blocks in a list, ordered by start index.
    blocks_found = find_contiguous_blocks(output_list, target_value, modification_range_end_exclusive)

    # --- Apply Replacements ---
    # Step 6: Check the number of blocks found and apply replacements.
    # Step 6a: If one or more blocks were found:
    if len(blocks_found) >= 1:
        # Step 6a.i: Select the first block from the ordered list.
        start_index_1, end_index_1 = blocks_found[0]
        # Step 6a.ii: Iterate through the indices defined by this block.
        # Step 6a.iii: For each index in this range, set the element in the working output sequence to `val1`.
        for i in range(start_index_1, end_index_1):
            output_list[i] = replacement_value_1

    # Step 6b: If two or more blocks were found:
    if len(blocks_found) >= 2:
        # Step 6b.i: Select the second block from the ordered list.
        start_index_2, end_index_2 = blocks_found[1]
        # Step 6b.ii: Iterate through the indices defined by this second block.
        # Step 6b.iii: For each index in this range, set the element in the working output sequence to `val2`.
        for i in range(start_index_2, end_index_2):
            output_list[i] = replacement_value_2
            
    # --- Return Result ---
    # Step 7: Return the modified working output sequence.
    return output_list
```
