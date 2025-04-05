
## train_1

**input:**
```
0 0 0 0 1 1 1 1 0 0 0 0
```


**output:**
```
0 0 0 0 1 0 0 1 0 0 0 0
```


## train_2

**input:**
```
0 7 7 7 7 7 7 7 7 0 0 0
```


**output:**
```
0 7 0 0 0 0 0 0 7 0 0 0
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 0 0 0
```


**output:**
```
7 0 0 0 0 0 0 0 7 0 0 0
```


## train_4

**input:**
```
0 0 7 7 7 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 0 7 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 5 5 5 5 5 5 5 0 0 0 0
```


**output:**
```
0 5 0 0 0 0 0 5 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 1 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 1 0 0 0 0
```


## train_7

**input:**
```
0 6 6 6 6 6 6 6 6 0 0 0
```


**output:**
```
0 6 0 0 0 0 0 0 6 0 0 0
```

## Perception of Task Elements

The task involves transforming a 1D sequence of numbers. The input sequences consist of blocks of identical numbers, often separated or surrounded by zeros. The transformation primarily affects contiguous blocks of identical *non-zero* numbers. Zeros seem to act as delimiters or background elements that remain unchanged unless they are part of the modification applied to the non-zero blocks. The core operation targets the *interior* elements of these non-zero blocks, specifically when the block's length exceeds two.

## Facts


```yaml
objects:
  - name: sequence
    type: list_of_integers
    description: Represents both the input and output data structure.
  - name: element
    type: integer
    description: Individual number within the sequence. Can be 0 or non-zero.
  - name: block
    type: contiguous_subsequence
    description: A run of identical, consecutive non-zero elements within the sequence.
properties:
  - object: block
    name: value
    type: integer
    description: The non-zero integer value repeated within the block.
  - object: block
    name: length
    type: integer
    description: The number of elements in the block.
  - object: block
    name: start_index
    type: integer
    description: The index of the first element of the block in the main sequence.
  - object: block
    name: end_index
    type: integer
    description: The index of the last element of the block in the main sequence.
actions:
  - name: identify_blocks
    description: Scan the input sequence to find all contiguous blocks of identical non-zero numbers.
  - name: modify_block
    description: Change elements within an identified block based on its length.
  - name: preserve_element
    description: Keep an element unchanged if it is 0 or part of a block not meeting modification criteria.
relationships:
  - type: condition
    description: The modification applied to a block depends on its length.
    condition: block.length > 2
    action: Replace elements between the first and last element of the block with 0.
  - type: condition
    description: If a block's length is 2 or less, it remains unchanged.
    condition: block.length <= 2
    action: Preserve all elements of the block.
  - type: context
    description: Elements equal to 0 that are not part of a modified block remain unchanged.
```


## Natural Language Program

1.  Initialize an output sequence identical to the input sequence.
2.  Iterate through the input sequence to identify contiguous blocks of identical non-zero numbers. For each block, record its value, start index, and end index.
3.  For each identified block:
    a.  Calculate the length of the block (end index - start index + 1).
    b.  If the length of the block is greater than 2:
        i.  Iterate from the element *after* the first element (index: start index + 1) up to the element *before* the last element (index: end index - 1).
        ii. Set the value of each element within this range in the *output* sequence to 0.
4.  Return the modified output sequence. Elements not part of a block longer than 2 (i.e., zeros or elements in blocks of length 1 or 2) remain unchanged from the input.
```python
import math
import numpy as np # Although numpy isn't strictly needed for list manipulation, it's a common import.

"""
Identifies contiguous blocks of identical non-zero numbers in a 1D sequence. 
If a block's length is greater than 2, it replaces all elements within the block, except for the first and the last, with 0. 
Elements that are 0 or part of blocks with length 2 or less remain unchanged.
"""

def find_block_end(sequence, start_index):
    """
    Finds the end index of a contiguous block of identical non-zero values.
    
    Args:
        sequence (list): The input sequence of numbers.
        start_index (int): The starting index of the potential block.

    Returns:
        int: The index of the last element in the block.
    """
    value_to_match = sequence[start_index]
    if value_to_match == 0: # Should not happen if called correctly, but good for safety
        return start_index 
        
    end_index = start_index
    while end_index + 1 < len(sequence) and sequence[end_index + 1] == value_to_match:
        end_index += 1
    return end_index

def transform(input_grid: list[int]) -> list[int]:
    """
    Transforms the input sequence based on contiguous non-zero blocks.

    Args:
        input_grid (list[int]): The input 1D sequence of integers.

    Returns:
        list[int]: The transformed 1D sequence.
    """
    # Initialize output_grid as a copy of the input to modify
    output_grid = list(input_grid)
    n = len(output_grid)
    i = 0 # Current index for scanning the sequence

    # Iterate through the sequence to find and process blocks
    while i < n:
        current_value = output_grid[i]

        # Check if the current element is non-zero and could start a block
        if current_value != 0:
            # Find the end of the contiguous block starting at index i
            start_index = i
            end_index = find_block_end(output_grid, start_index)
            
            # Calculate the length of the identified block
            block_length = end_index - start_index + 1

            # Modify the block in the output_grid if its length is greater than 2
            if block_length > 2:
                # Iterate through the interior elements of the block
                for j in range(start_index + 1, end_index):
                    # Set the interior elements to 0
                    output_grid[j] = 0
            
            # Move the main index past the processed block
            i = end_index + 1 
        else:
            # If the current element is 0, just move to the next element
            i += 1

    # Return the modified sequence
    return output_grid
```
