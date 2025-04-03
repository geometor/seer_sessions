
## train_1

**input:**
```
0 0 0 4 0 0 0 4 0 0 0 4 0 0 4 0 4 4 4 4 4 4 4 4 4 4 0 0 0 4 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 0 0 0 0 1 0 0 1 0 0 0 1 0 0 0
```


**output:**
```
0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 8 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 8 0 0 0 0 8 0 0 0
```


**output:**
```
0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The task operates on single-row grids (effectively 1D arrays). Each input row consists of pixels of two colors: a background color (white, represented by 0) and a single foreground color (yellow, blue, or azure in the examples). The foreground color appears in multiple, separate contiguous blocks of varying lengths within the input row.

The transformation identifies the *longest* contiguous block of the foreground color within the input row. The output row is constructed to be the same length as the input. This longest foreground block is preserved in its original position in the output row. All other pixels in the output row, including those that were part of shorter foreground blocks or the original background in the input, are set to the background color (white, 0).

**Facts:**


```yaml
task_type: object_selection_and_filtering
input_features:
  - grid_dimensionality: 1D (single row)
  - background_color: white (0)
  - foreground_color: single non-white color (varies per example)
  - foreground_pixels_form_blocks: Yes, multiple contiguous blocks of the foreground color exist.
  - block_properties:
      - contiguity: horizontal
      - size: variable length
output_features:
  - grid_dimensionality: 1D (single row)
  - dimensions: same as input row length
  - background_color: white (0)
  - foreground_color: same as input foreground color
  - foreground_pixels_form_blocks: Yes, exactly one contiguous block of the foreground color exists.
relationship_input_output:
  - preservation: The single output foreground block corresponds exactly in color, size, and position to the largest foreground block found in the input.
  - modification: All pixels in the output that do not belong to the preserved largest block are set to the background color (white, 0).
objects:
  - object: background
    color: white (0)
  - object: foreground_block
    definition: A maximal contiguous sequence of non-white pixels.
    properties:
      - color: non-white (consistent within a block and within an example)
      - length: number of pixels in the sequence
  - object: target_block
    definition: The foreground_block with the maximum length in the input.
actions:
  - identify_foreground_color: Determine the non-white color present in the input.
  - find_contiguous_blocks: Locate all contiguous sequences (blocks) of the foreground color in the input row.
  - measure_block_length: Calculate the length of each identified foreground block.
  - select_largest_block: Identify the foreground block with the maximum length. If multiple blocks share the maximum length, the examples suggest any one will suffice (implicitly, perhaps the first one encountered).
  - create_output_row: Initialize a new row of the same length as the input, filled entirely with the background color (white, 0).
  - copy_target_block: Copy the pixels of the selected largest block from the input into the corresponding positions in the output row.
```


**Natural Language Program:**

1.  Determine the dimensions (length) of the input row.
2.  Identify the two colors present: the background color (white, 0) and the single foreground color.
3.  Scan the input row to find all contiguous blocks (sequences) of the foreground color. Record the start index, end index, and length of each block.
4.  Compare the lengths of all identified foreground blocks and select the block with the maximum length. Note its start and end indices.
5.  Create a new output row with the same length as the input row, initially filled entirely with the background color (white, 0).
6.  Copy the pixels corresponding to the selected largest foreground block (from its start index to its end index in the input) into the same positions in the new output row.
7.  The resulting row is the final output.
```python
import numpy as np
import sys # adding sys to allow helper function imports

# Add helper functions directory to Python path if needed (adjust path as necessary)
# sys.path.append('/path/to/your/helper_functions') 
# from helper_functions import find_foreground_color, find_longest_block # Example import

# Define helper functions directly within the module for simplicity in this case

def find_foreground_color(row):
    """
    Finds the first non-zero color in the row.
    Assumes 0 is the background color.

    Args:
        row (list): A list of integers representing a row of pixels.

    Returns:
        int or None: The first non-zero color found, or None if only
                     background color (0) exists.
    """
    for pixel in row:
        if pixel != 0:
            return pixel
    return None # Return None if only background color exists

def find_longest_block(row, foreground_color):
    """
    Finds the start index and length of the longest contiguous block 
    of the specified foreground_color in the row.

    Args:
        row (list): A list of integers representing a row of pixels.
        foreground_color (int): The color value to search for blocks of.

    Returns:
        tuple (int, int): A tuple containing:
            - The start index of the longest block found (-1 if no block found).
            - The length of the longest block found (0 if no block found).
    """
    n = len(row)
    max_len = 0
    longest_block_start = -1
    current_start = -1
    current_len = 0

    for i in range(n):
        if row[i] == foreground_color:
            # If this is the start of a new block
            if current_len == 0:  
                current_start = i
            # Increment length of current block
            current_len += 1
        else:  
            # Reached the end of a potential block (or still in background)
            # Check if the block just ended was the longest found so far
            if current_len > 0:  # Only check if we were actually tracking a block
                if current_len > max_len:
                    max_len = current_len
                    longest_block_start = current_start
            # Reset current block tracking
            current_len = 0  

    # After the loop, check if the last sequence was a block and potentially the longest
    # This handles cases where the longest block extends to the end of the row
    if current_len > max_len:
        max_len = current_len
        longest_block_start = current_start

    return longest_block_start, max_len


def transform(input_grid):
    """
    Transforms the input single-row grid by identifying the longest
    contiguous block of the foreground color and preserving only that
    block in the output row. All other pixels in the output row are 
    set to the background color (0).

    Args:
        input_grid (list of lists): A grid represented as a list containing a single list (row) of integers.

    Returns:
        list of lists: A new grid containing the transformed single row.
                       Returns an empty list if the input is invalid.
    """
    # --- Input Validation and Setup ---
    # Check for empty or invalid input format
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
        # Consider logging a warning or raising an error for invalid input
        return [] 

    # Extract the single row from the input grid structure
    input_row = input_grid[0]
    n = len(input_row) # Get the length of the row

    # --- Identify Foreground Color ---
    # Determine the color used for foreground objects (assumes only one non-background color)
    foreground_color = find_foreground_color(input_row)

    # Handle the case where the input row contains only the background color
    if foreground_color is None:
        # Return a new grid of the same size filled with background color
        return [[0] * n] 

    # --- Find the Longest Block ---
    # Locate the starting position and length of the longest continuous sequence 
    # of the foreground color.
    start_index, length = find_longest_block(input_row, foreground_color)

    # --- Create Output Grid ---
    # Initialize a new output row filled entirely with the background color (0)
    output_row = [0] * n

    # If a longest block was actually found (i.e., length > 0)
    if start_index != -1 and length > 0:
        # Copy the pixels corresponding to the longest block from the input 
        # into the output row at the same position.
        for i in range(length):
            # Calculate the index in the output row
            output_index = start_index + i
            # Check bounds just in case, though logic should prevent out-of-bounds
            if 0 <= output_index < n: 
                output_row[output_index] = foreground_color

    # Return the transformed row, wrapped in a list to match the grid format
    return [output_row]
```
