
## train_1

**input:**
```
0 0 9 9 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 5 5 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 7 7 7 0 0 7 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 0 7 7 7 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the perception, facts, and the natural language program for this task.

**Perception of the Elements:**

1.  **Input/Output Format:** The input and output are presented as 1D sequences of numbers (colors), likely representing a single row of a larger grid or just a 1D problem.
2.  **Colors:** The primary colors involved are white (0) and one other non-white color per example (Maroon=9, Gray=5, Orange=7).
3.  **Objects:** The key objects are contiguous horizontal blocks (runs) of the non-white color within the sequence.
4.  **Key Feature:** The length (or width) of these non-white blocks is crucial.
5.  **Transformation:** The transformation involves modifying the lengths of these non-white blocks. Specifically, all blocks of the *same* non-white color are resized to match the length of the *longest* block of that color found in the input.
6.  **Resizing Mechanism:** The resizing appears to happen symmetrically around the center of the original block. Shorter blocks expand outwards, overwriting adjacent white pixels. The longest block remains unchanged.

**YAML Facts:**


```yaml
task_description: Resizes all contiguous horizontal blocks of a specific non-white color to match the length of the longest block of that same color found in the input sequence.
data_format:
  type: 1D sequence (or single row grid)
  cell_values: Integers 0-9 representing colors.
objects:
  - object: color_block
    description: A contiguous horizontal sequence of one or more identical non-white pixels.
    properties:
      - color: The color of the pixels in the block (e.g., Maroon, Gray, Orange).
      - start_index: The starting position (index) of the block in the sequence.
      - end_index: The ending position (index) of the block in the sequence.
      - length: The number of pixels in the block (end_index - start_index + 1).
relationships:
  - relationship: intra_color_comparison
    description: All blocks of the same non-white color are compared based on their length.
    operands:
      - color_block (same non-white color)
    purpose: To find the maximum length among them.
actions:
  - action: find_dominant_color
    description: Identify the single non-white color present in the input sequence.
    output: target_color
  - action: find_blocks
    description: Locate all contiguous blocks of the target_color in the input sequence.
    input: input_sequence, target_color
    output: list_of_blocks (each with start_index, end_index, length)
  - action: find_max_length
    description: Determine the maximum length among the identified blocks.
    input: list_of_blocks
    output: max_len
  - action: resize_blocks
    description: >
      Generate the output sequence by creating new blocks corresponding to each original block,
      but with the calculated max_len, centered at the original block's center position.
    input: input_sequence_length, list_of_blocks, target_color, max_len
    output: output_sequence
    details: >
      Initialize an output sequence (same length as input) with white (0).
      For each original block:
      1. Calculate its center index: center = floor((start + end) / 2).
      2. Calculate the new start/end indices based on max_len and center:
         new_start = center - floor((max_len - 1) / 2)
         new_end = center + ceil((max_len - 1) / 2)
      3. Fill the output sequence from new_start to new_end with target_color.
```


**Natural Language Program:**

1.  Identify the non-white color (`target_color`) present in the input sequence.
2.  Find all distinct contiguous blocks of the `target_color` in the input sequence, noting their start and end positions.
3.  Calculate the length of each block and determine the maximum length (`max_len`) found among them.
4.  Create a new output sequence of the same length as the input, initially filled entirely with the white color (0).
5.  For each identified block from the input sequence:
    a.  Calculate the central position (index) of the original block.
    b.  Determine the start and end indices for a new block of length `max_len`, centered at the calculated central position.
    c.  Fill the corresponding range of indices in the output sequence with the `target_color`.
6.  Return the completed output sequence.
```python
"""
Identifies the single non-white color present in the 1D input sequence.
Finds all contiguous horizontal blocks (runs) of this color.
Determines the maximum length among these blocks.
Creates an output sequence of the same length, initially all white.
For each original block, calculates its center position.
Places a new block of the determined maximum length, centered at the original block's center, into the output sequence, overwriting the white background with the identified non-white color.
Ensures the new blocks stay within the bounds of the sequence.
"""

import numpy as np
from typing import List, Tuple

def find_blocks(sequence: np.ndarray, target_color: int) -> List[Tuple[int, int]]:
    """
    Finds contiguous blocks of a target color in a 1D sequence.

    Args:
        sequence: The 1D numpy array representing the sequence.
        target_color: The integer color value to find blocks of.

    Returns:
        A list of tuples, where each tuple is (start_index, end_index)
        of a block.
    """
    blocks = []
    start_index = -1
    n = len(sequence)
    for i, color in enumerate(sequence):
        if color == target_color and start_index == -1:
            # Start of a new block
            start_index = i
        elif color != target_color and start_index != -1:
            # End of the current block (previous index was the end)
            blocks.append((start_index, i - 1))
            start_index = -1
            
    # Check if the sequence ends with a block
    if start_index != -1:
        blocks.append((start_index, n - 1))
        
    return blocks

def transform(input_sequence: List[int]) -> List[int]:
    """
    Resizes all contiguous horizontal blocks of a specific non-white color
    to match the length of the longest block of that same color found in
    the input sequence, centering the resized block around the original's center.

    Args:
        input_sequence: A list of integers (0-9) representing the input colors.

    Returns:
        A list of integers representing the transformed sequence.
    """
    
    input_array = np.array(input_sequence, dtype=int)
    n = len(input_array)
    
    # 1. Identify the non-white color (`target_color`)
    target_color = -1
    for color in input_array:
        if color != 0:
            target_color = color
            break
            
    # If no non-white color found, return the input as is
    if target_color == -1:
        return input_sequence

    # 2. Find all distinct contiguous blocks of the `target_color`
    blocks = find_blocks(input_array, target_color)
    
    # If no blocks found, return the input as is
    if not blocks:
        return input_sequence
        
    # 3. Calculate the length of each block and determine the maximum length (`max_len`)
    max_len = 0
    for start, end in blocks:
        length = end - start + 1
        if length > max_len:
            max_len = length
            
    # 4. Create a new output sequence, initially filled with white (0)
    output_array = np.zeros_like(input_array)

    # 5. For each identified block from the input sequence:
    for start, end in blocks:
        # a. Calculate the central position (index) of the original block
        # Use floor division for potentially even length blocks
        center = (start + end) // 2 
        
        # b. Determine the start and end indices for a new block of length `max_len`,
        #    centered at the calculated central position.
        # Calculate start index based on center and max_len
        new_start = center - (max_len - 1) // 2
        # Calculate end index based on new_start and max_len
        new_end = new_start + max_len - 1
        
        # Clamp indices to ensure they are within the bounds of the array
        new_start_clamped = max(0, new_start)
        new_end_clamped = min(n - 1, new_end)
        
        # c. Fill the corresponding range of indices in the output sequence
        #    with the `target_color`. Only fill if the range is valid.
        if new_start_clamped <= new_end_clamped:
             output_array[new_start_clamped : new_end_clamped + 1] = target_color

    # 6. Return the completed output sequence as a list
    return output_array.tolist()

```
