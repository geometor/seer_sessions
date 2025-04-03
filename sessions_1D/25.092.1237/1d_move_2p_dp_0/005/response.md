```python
"""
Transforms an input 1D grid (list of integers) based on a specific pattern.
The pattern consists of a contiguous block of identical, non-white/non-blue pixels
("Main Block"), followed immediately by two white pixels ("Separator"), followed
immediately by a single blue pixel ("Marker"). Any white pixels before the Main
Block are "Leading Background", and any white pixels after the Marker are
"Trailing Background".

The transformation swaps the positions of the Main Block and the Separator,
while keeping the Leading Background, Marker, and Trailing Background in their
original absolute positions relative to the grid boundaries.

1.  Scan the input row to locate the unique blue pixel (color 1); this is the "Marker". Record its index.
2.  Identify the two pixels immediately preceding the Marker's index. Verify they are both white (color 0); these form the "Separator".
3.  Identify the contiguous block of pixels immediately preceding the Separator. Verify these pixels are all the same color and that the color is *not* white (0) or blue (1). This block is the "Main Block". Record its start index, end index, color, and length.
4.  Identify the sequence of pixels from the start of the row up to (but not including) the start index of the Main Block. This is the "Leading Background".
5.  Identify the sequence of pixels from the index immediately after the Marker to the end of the row. This is the "Trailing Background".
6.  Construct the output row by concatenating the identified components in the following specific order: Leading Background, Separator, Main Block, Marker, Trailing Background.
7.  The resulting concatenated row is the final output grid. If the pattern is not found at any step, the original input grid is returned.
"""

import numpy as np
from typing import List, Optional, Tuple

# --- Helper Functions ---

def find_first_occurrence(arr: np.ndarray, value: int) -> Optional[int]:
    """Finds the index of the first occurrence of a value in a numpy array."""
    indices = np.where(arr == value)[0]
    if len(indices) == 0:
        return None # Value not found
    return indices[0]

def find_main_block_before(arr: np.ndarray, end_exclusive_idx: int) -> Optional[Tuple[int, int, int]]:
    """
    Finds the contiguous block of identical, non-white/non-blue pixels
    ending just before the specified index.

    Args:
        arr: The numpy array representing the grid row.
        end_exclusive_idx: The index immediately *after* the desired block ends.

    Returns:
        A tuple (start_idx, end_idx, color) if found, otherwise None.
        end_idx is inclusive.
    """
    # Check if there's anything before the target index
    if end_exclusive_idx <= 0:
        return None # Cannot be a block before the start

    # Identify the potential last pixel of the block and its color
    main_block_end_idx = end_exclusive_idx - 1
    main_block_color = arr[main_block_end_idx]

    # Check if the block color is valid (not white 0 or blue 1)
    if main_block_color == 0 or main_block_color == 1:
        return None # Invalid color for main block

    # Find the start of the main block by searching backwards
    main_block_start_idx = main_block_end_idx
    while main_block_start_idx > 0 and arr[main_block_start_idx - 1] == main_block_color:
        main_block_start_idx -= 1
        
    # Return the start index (inclusive), end index (inclusive), and color
    return main_block_start_idx, main_block_end_idx, main_block_color


# --- Main Transformation Function ---

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A list of integers representing the input row.

    Returns:
        A list of integers representing the transformed output row,
        or the original input_grid if the required pattern is not found.
    """
    
    # Convert input list to numpy array for efficient processing
    input_array = np.array(input_grid)
    n = len(input_array) # Length of the grid

    # 1. Find the Marker (blue pixel, value 1)
    marker_idx = find_first_occurrence(input_array, 1)
    if marker_idx is None:
        # If no marker is found, the pattern is invalid. Return original.
        return input_grid 

    # 2. Identify and verify the Separator (two white pixels before marker)
    # Check if there are at least two pixels before the marker
    if marker_idx < 2:
        # Not enough space for the separator. Pattern invalid. Return original.
        return input_grid 
        
    # Define the expected start index and content of the separator
    separator_start_idx = marker_idx - 2
    separator_content = [0, 0] # Expected separator pixels
    
    # Verify the pixels at the separator location match the expected content
    if not np.array_equal(input_array[separator_start_idx : marker_idx], separator_content):
        # Separator content doesn't match [0, 0]. Pattern invalid. Return original.
        return input_grid 

    # 3. Identify the Main Block (contiguous non-white/non-blue block before separator)
    # Use the helper function to find the block ending just before the separator starts
    block_info = find_main_block_before(input_array, separator_start_idx)
    if block_info is None:
        # Main block pattern (contiguous, same color, not 0 or 1) not found. Return original.
        return input_grid 
        
    # Extract block details from the returned tuple
    main_block_start_idx, main_block_end_idx, _ = block_info
        
    # Extract the main block content as a list
    main_block = input_array[main_block_start_idx : main_block_end_idx + 1].tolist()

    # 4. Identify Leading Background (pixels before Main Block)
    # These are all pixels from the start of the array up to the main block's start index
    leading_bg = input_array[0 : main_block_start_idx].tolist()
    # Optional check: Can verify here if leading_bg contains only 0s if required by stricter rules.

    # 5. Identify Trailing Background (pixels after Marker)
    # These are all pixels from the position after the marker to the end of the array
    trailing_bg = input_array[marker_idx + 1 :].tolist()
    # Optional check: Can verify here if trailing_bg contains only 0s if required by stricter rules.

    # 6. Construct Output by concatenating in the new order
    # The new order is: Leading Background, Separator, Main Block, Marker, Trailing Background
    output_grid_list = leading_bg + separator_content + main_block + [1] + trailing_bg
    
    # 7. Return the resulting list
    return output_grid_list
```