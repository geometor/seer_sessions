
## train_1

**input:**
```
0 0 0 0 7 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0 0 7 0 0 0 0 7 0 0 0 7 0
```


**output:**
```
0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 5 5 5 5 5 5 5 5 5 5 0 0 0 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 8 0 0 0 8 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 8 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
```

**Perception:**

The task operates on a one-dimensional array of pixels (colors). Each input array contains white pixels (represented by 0) and pixels of one other color (e.g., orange=7, gray=5, azure=8). The goal is to isolate the single largest contiguous block of non-white pixels within the input array. All other pixels, including any smaller blocks or individual pixels of the non-white color, should be turned white (0) in the output. The output array has the same dimensions as the input array.

**YAML Facts:**


```yaml
task_type: object_manipulation
input_domain:
  dimensionality: 1
  pixel_colors:
    - white (0)
    - one other color C (non-zero)
  elements:
    - pixels:
        attributes: [color, position]
    - contiguous_blocks:
        description: Sequences of adjacent pixels of the same non-white color C.
        attributes: [color, start_position, end_position, length]
output_domain:
  dimensionality: 1
  pixel_colors:
    - white (0)
    - the same color C from the input
  elements:
    - pixels:
        attributes: [color, position]
    - single_block:
        description: The largest contiguous block of color C identified from the input.
        attributes: [color, start_position, end_position, length]
transformation:
  operation: filtering / selection
  steps:
    - Identify all contiguous blocks of the non-white color C in the input array.
    - Determine the length of each identified block.
    - Find the block with the maximum length. (Assume the first one found if there are ties in length, though examples don't test this).
    - Create an output array of the same size as the input, filled entirely with white (0) pixels.
    - Copy the pixels corresponding to the largest identified block from the input array to the same positions in the output array.
relationships:
  - Adjacency: Defines contiguous blocks.
  - Size comparison: Used to select the largest block.
  - Positional correspondence: The largest block retains its original position in the output.
invariants:
  - Grid dimensions remain the same.
  - The color of the pixels within the largest block remains the same.
  - The position of the largest block remains the same.
  - White pixels outside the span of the largest block remain white.
```


**Natural Language Program:**

1.  Initialize an output array with the same dimensions as the input array, filling it entirely with white pixels (0).
2.  Identify the single non-white color present in the input array.
3.  Scan the input array to find all contiguous blocks (sequences of one or more adjacent pixels) of this non-white color. Record the start index, end index, and length of each block.
4.  Compare the lengths of all identified blocks and select the block with the greatest length. If multiple blocks share the maximum length, select the one that appears first in the input array.
5.  If a largest block is found (i.e., if the input contains at least one non-white pixel), copy the pixels from this largest block (using its start and end indices) from the input array to the corresponding positions in the output array.
6.  Return the modified output array.
```python
import numpy as np
import collections

"""
Identify the single largest contiguous block of a non-white color in a 1D input array. 
Create an output array of the same size, initially filled with white (0). 
Copy only the pixels belonging to the largest identified block from the input to the output array at the same positions. 
All other pixels in the output remain white. If multiple blocks share the maximum length, the first one encountered is chosen.
"""

def find_contiguous_blocks(grid, target_color):
    """Finds all contiguous blocks of a specific color in a 1D grid."""
    blocks = []
    in_block = False
    start_index = -1
    for i, pixel in enumerate(grid):
        if pixel == target_color and not in_block:
            # Start of a new block
            in_block = True
            start_index = i
        elif pixel != target_color and in_block:
            # End of the current block
            in_block = False
            end_index = i # end index is exclusive
            blocks.append({'start': start_index, 'end': end_index, 'length': end_index - start_index, 'color': target_color})
            start_index = -1 # reset
    
    # Handle block ending at the very end of the grid
    if in_block:
        end_index = len(grid)
        blocks.append({'start': start_index, 'end': end_index, 'length': end_index - start_index, 'color': target_color})
        
    return blocks

def transform(input_grid):
    """
    Transforms the input grid by keeping only the largest contiguous block 
    of the non-white color and turning everything else white.
    
    Args:
        input_grid (list): A 1D list of integers representing pixel colors.

    Returns:
        list: The transformed 1D list of integers.
    """
    
    # Convert input to numpy array for easier handling if needed, though list operations are fine here
    # input_arr = np.array(input_grid)
    grid_len = len(input_grid)
    
    # Initialize output_grid with all white pixels (0)
    output_grid = [0] * grid_len

    # 1. Identify the non-white color C
    non_white_color = None
    for pixel in input_grid:
        if pixel != 0:
            non_white_color = pixel
            break
            
    # If no non-white color is found, return the all-white grid
    if non_white_color is None:
        return output_grid

    # 2. Find all contiguous blocks of the non-white color
    blocks = find_contiguous_blocks(input_grid, non_white_color)

    # 3. Find the largest block
    largest_block = None
    max_length = 0
    
    if not blocks: # No blocks of the non-white color found
      return output_grid

    for block in blocks:
        if block['length'] > max_length:
            max_length = block['length']
            largest_block = block
            
    # Check if a largest block was actually found (handles cases with only white pixels correctly via the initial check)
    if largest_block:
        # 4. Copy the largest block to the output grid
        start = largest_block['start']
        end = largest_block['end']
        output_grid[start:end] = input_grid[start:end]

    return output_grid
```
