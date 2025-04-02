
## train_1

**input:**
```
0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 1 0
```


**output:**
```
0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 1 0
```


## train_2

**input:**
```
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 1 0
```


**output:**
```
0 0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 1 0
```


## train_3

**input:**
```
0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 0 0 1 0
```


**output:**
```
0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 1 0
```

*   **Perception of the elements**:
    *   The input and output are both single-row grids (1D arrays).
    *   The grids contain pixels of white (0), blue (1), and one other color (magenta (6) or yellow (4)).
    *   Each input grid features a structure: some initial white pixels, a contiguous block of a single non-white/non-blue color (the "main block"), followed by exactly two white pixels, a single blue pixel, and a final white pixel.
    *   The transformation involves rearranging the pixels within the row.
    *   The main block of color appears shifted to the right in the output compared to the input.
    *   The number of leading white pixels increases by two in the output.
    *   The two white pixels that were immediately before the blue pixel in the input are no longer there in the output; instead, two white pixels appear at the beginning.
    *   The blue pixel and the final white pixel remain fixed at the end of the grid.
    *   The color and length of the main block remain unchanged.
    *   The overall length of the grid remains unchanged.

*   **YAML Facts**:
    
```yaml
    task_description: Rearrange elements in a 1D grid based on specific markers.
    elements:
      - object: grid
        property: single row (1D array)
      - object: main_block
        property: contiguous sequence of a single color (not white or blue)
        location: variable start index in input
      - object: marker_sequence
        property: sequence of [blue, white] pixels (values [1, 0])
        location: fixed at the end of the grid
      - object: preceding_whites
        property: sequence of two white pixels (values [0, 0])
        location: immediately before the marker_sequence in the input
    transformation:
      action: move
      source_object: preceding_whites
      destination: beginning of the grid
    constraints:
      - grid size remains constant
      - main_block color and length remain constant
      - marker_sequence position remains constant relative to the end
      - input always contains the [0, 0, 1, 0] sequence towards the end
    ```


*   **Natural Language Program**:
    1.  Identify the sequence `[0, 0, 1, 0]` (two whites, one blue, one white) near the end of the input grid row.
    2.  Remove the two white pixels (`[0, 0]`) that immediately precede the blue pixel (`1`).
    3.  Insert these two removed white pixels (`[0, 0]`) at the very beginning of the grid row.
    4.  The resulting arrangement of pixels forms the output grid row.
```python
import numpy as np
from typing import List, Tuple

"""
Identifies the sequence [0, 0, 1, 0] (two white, one blue, one white) near the end of the input grid row.
Removes the two white pixels ([0, 0]) that immediately precede the blue pixel (1).
Inserts these two removed white pixels ([0, 0]) at the very beginning of the grid row.
The resulting arrangement of pixels forms the output grid row.
"""

def find_pattern_index(input_list: List[int]) -> int:
    """
    Finds the index of the '1' in the pattern [0, 0, 1, 0] near the end.

    Args:
        input_list: The 1D list representing the grid row.

    Returns:
        The index of the '1' in the pattern, or -1 if not found.
    """
    # Iterate backwards to find the last occurrence first
    # Need index i, i+1, i-1, i-2, so start loop from len - 2
    for i in range(len(input_list) - 2, 1, -1):
        # Check for the pattern [0, 0, 1, 0] centered around index i (the '1')
        if (input_list[i] == 1 and
            input_list[i+1] == 0 and
            input_list[i-1] == 0 and
            input_list[i-2] == 0):
            return i  # Return the index of the '1'
    return -1 # Pattern not found

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by moving two white pixels preceding a 
    specific marker sequence ([1, 0]) to the beginning of the row.

    Args:
        input_grid: A list containing a single list (the row) of integers.

    Returns:
        A list containing the single transformed row as a list of integers.
    """
    # Ensure input is treated as a single row
    if not input_grid or not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
         raise ValueError("Input grid must be a list containing one list (row)")
         
    input_row = input_grid[0]
    
    # Find the index of the '1' in the specific [0, 0, 1, 0] pattern
    marker_index = find_pattern_index(input_row)

    if marker_index == -1:
        # If the pattern isn't found, return the input unchanged or handle error
        # Based on examples, pattern should always exist. Returning unchanged for safety.
        print("Warning: Pattern [0, 0, 1, 0] not found. Returning original grid.")
        return input_grid

    # Indices of the two white pixels to move (immediately before the '1')
    white_pixel_index1 = marker_index - 2
    white_pixel_index2 = marker_index - 1

    # Initialize the output row with the two moved white pixels
    output_row = [0, 0]

    # Iterate through the input row and append elements, skipping the moved ones
    for idx, pixel in enumerate(input_row):
        if idx != white_pixel_index1 and idx != white_pixel_index2:
            output_row.append(pixel)

    # Return the transformed row within a list structure
    return [output_row]

```
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a single-row input grid based on a specific pattern.
1. Identifies the sequence `[0, 0, 1, 0]` (two whites, one blue, one white) located near the end of the input grid row. Let the index of the blue pixel (`1`) be `M`.
2. Identifies the two white pixels (`[0, 0]`) immediately preceding the blue pixel. These are at indices `M-2` and `M-1`. Call this sequence `moved_zeros`.
3. Identifies the sequence of pixels from the beginning of the row up to index `M-3` (inclusive). Call this the `prefix`.
4. Identifies the final sequence consisting of the blue pixel and the last white pixel (`[1, 0]`) at indices `M` and `M+1`. Call this the `suffix`.
5. Constructs the output row by concatenating:
    *   The `moved_zeros` sequence (`[0, 0]`).
    *   The `prefix` sequence, *excluding its last element*. If the prefix has 0 or 1 elements, this part is empty.
    *   The `suffix` sequence (`[1, 0]`).
6. The resulting row is the output grid, wrapped in a list. The length of the output row will be one less than the input row.
"""

def find_pattern_1_index(row: List[int]) -> Optional[int]:
    """
    Finds the index of the '1' in the pattern [..., 0, 0, 1, 0].

    Args:
        row: The list of integers representing the grid row.

    Returns:
        The index of the '1' if the pattern is found, otherwise None.
    """
    # Iterate backwards from the second-to-last possible position of '1'
    for i in range(len(row) - 2, 1, -1): 
        # Check if the pattern [0, 0, 1, 0] exists centered around index i (the '1')
        if (row[i] == 1 and
            row[i+1] == 0 and
            row[i-1] == 0 and
            row[i-2] == 0):
            return i  # Return the index of the '1'
    return None # Pattern not found

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list containing a single list (the row) of integers.
                    Can also handle a NumPy array input.

    Returns:
        A list containing the single transformed row as a list of integers.
        Returns the original grid if the pattern is not found or input is invalid.
    """
    # --- Input Validation and Preparation ---
    if not isinstance(input_grid, (list, np.ndarray)):
        print("Warning: Invalid input_grid type. Expected list or numpy array.")
        # Attempt to handle potential edge cases or return original
        return input_grid if isinstance(input_grid, list) else [] 

    if len(input_grid) != 1:
         print(f"Warning: Expected input grid with 1 row, got {len(input_grid)}. Returning original.")
         # Ensure output matches expected format even on error return
         if isinstance(input_grid, np.ndarray):
             return input_grid.tolist()
         return input_grid

    # Extract the row, handle numpy array case
    if isinstance(input_grid, np.ndarray):
        input_row = input_grid[0].tolist()
    elif isinstance(input_grid[0], list):
         input_row = input_grid[0]
    else: # Should not happen based on ARC rules but good for robustness
         print("Warning: First element of input_grid is not a list.")
         return input_grid # Or convert if possible based on structure

    # --- Core Logic ---
    # 1. Find the index 'M' of the '1' in the pattern [0, 0, 1, 0]
    marker_1_index = find_pattern_1_index(input_row)

    if marker_1_index is None:
        print("Warning: Pattern [0, 0, 1, 0] not found. Returning original grid.")
        # Return in standard list-of-lists format
        return [input_row] 
        
    # Calculate the start index of the pattern [0, 0, 1, 0]
    pattern_start_index = marker_1_index - 2

    # 2. Identify moved_zeros ([0, 0] before '1')
    # Indices are pattern_start_index and pattern_start_index + 1
    moved_zeros = input_row[pattern_start_index : marker_1_index] # Slices up to, but not including, marker_1_index
    # Explicitly check if they are indeed [0, 0] if needed for robustness
    # if moved_zeros != [0, 0]:
    #    print("Warning: Pixels before '1' are not [0, 0].") # Or handle error

    # 3. Identify prefix (elements before the pattern starts)
    prefix = input_row[0 : pattern_start_index]

    # 4. Identify suffix ([1, 0] starting at marker_1_index)
    suffix = input_row[marker_1_index : marker_1_index + 2]
    # Explicitly check if they are indeed [1, 0] if needed
    # if suffix != [1, 0]:
    #    print("Warning: Pixels starting from '1' are not [1, 0].")

    # 5. Construct the output row
    # Concatenate: moved_zeros + prefix (without last element) + suffix
    if len(prefix) > 0:
        modified_prefix = prefix[:-1] # Remove the last element
    else:
        modified_prefix = [] # Handle empty prefix case

    output_row = moved_zeros + modified_prefix + suffix

    # 6. Return the output grid in the standard format
    return [output_row]
```
