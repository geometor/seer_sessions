import numpy as np
import sys

# Add the directory containing py_utils to the Python path
# Note: Replace '/path/to/arc-prize-strategy/lib' with the actual path if needed
sys.path.append('/path/to/arc-prize-strategy/lib')
# Or if the structure is Notebooks/ -> lib/ then use:
# sys.path.append('../lib')
try:
    # Import utility functions if available, otherwise define placeholders
    # This is useful if you have common ARC helper functions
    # from py_utils import get_objects, find_objects, find_objects_by_color
    pass # No specific py_utils needed for this task yet
except ImportError:
    print("Warning: py_utils not found. Proceeding without them.")
    # Define placeholder functions or handle the absence as needed
    pass

"""
Transformation Rule:
Identify four contiguous segments in the input row:
1. `initial_segment`: Any pixels from the start up to the first non-white pixel (can be empty).
2. `movable_block`: The first contiguous block of non-white pixels.
3. `white_gap`: The contiguous block of white (0) pixels immediately following the `movable_block`.
4. `final_segment`: All pixels following the `white_gap` until the end of the row.
Construct the output row by concatenating these segments in the order: `initial_segment`, `white_gap`, `movable_block`, `final_segment`.
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Swaps the first contiguous non-white block with the immediately
    following contiguous white block in a 1D input grid.

    Args:
        input_grid: A numpy array of shape (1, N) representing the input row.

    Returns:
        A numpy array of shape (1, M) representing the transformed row.
        M might be the same as N, assuming no pixels are added/removed.
    """
    # Ensure the input is a 1D array (or treat the first row if 2D)
    if input_grid.ndim == 2 and input_grid.shape[0] == 1:
        input_list = input_grid[0].tolist()
    elif input_grid.ndim == 1:
        input_list = input_grid.tolist()
    else:
        raise ValueError("Input grid must be 1D or have shape (1, N)")

    n = len(input_list)
    
    # --- Find Segment Boundaries ---
    
    movable_start = -1
    movable_end = -1
    gap_start = -1
    gap_end = -1

    # 1. Find the start of the movable_block (first non-white pixel)
    for i in range(n):
        if input_list[i] != 0:
            movable_start = i
            break
    
    # If no non-white pixel found (e.g., all white input), return original
    if movable_start == -1:
        print("Warning: No non-white block found.")
        return input_grid 

    # 2. Find the end of the movable_block (first white pixel *at or after* movable_start)
    # This also marks the potential start of the white_gap
    for i in range(movable_start, n):
        if input_list[i] == 0:
            movable_end = i
            gap_start = i # White gap starts where the movable block ends
            break
    else: 
        # Non-white block extends to the end of the list
        movable_end = n
        # This implies no white_gap exists immediately after, violating the observed pattern.
        print("Warning: Movable block extends to the end. No white gap found immediately after.")
        # Based on examples, this case shouldn't occur for a valid transformation.
        # Return original or raise error depending on stricter requirements.
        return input_grid 

    # 3. Find the end of the white_gap (first non-white pixel *at or after* gap_start)
    for i in range(gap_start, n):
        if input_list[i] != 0:
            gap_end = i
            break
    else: 
        # White gap extends to the end of the list
        gap_end = n

    # --- Validate Segment Presence ---
    # Check if a valid movable block was found (length > 0)
    if movable_start == movable_end : # This shouldn't happen if movable_start != -1
         print(f"Warning: Zero-length movable block found? Start={movable_start}, End={movable_end}")
         return input_grid

    # Check if a valid white gap was found (length > 0)
    if gap_start == gap_end:
        # This means the pixel sequence was ...non-white, non-white... with no white in between
        print(f"Warning: No white gap found immediately after movable block. Movable ends at {movable_end-1}, Gap starts at {gap_start}, Gap ends at {gap_end}.")
        # Based on examples, this shouldn't occur for a valid transformation.
        return input_grid

    # --- Extract Segments ---
    # Segment 1: initial_segment (pixels before movable_block)
    initial_segment = input_list[:movable_start]
    
    # Segment 2: movable_block (the non-white block)
    movable_block = input_list[movable_start:movable_end]
    
    # Segment 3: white_gap (the white block immediately after)
    white_gap = input_list[gap_start:gap_end]
    
    # Segment 4: final_segment (pixels after white_gap)
    final_segment = input_list[gap_end:]

    # --- Reconstruct Output ---
    # Concatenate in the new order: initial + gap + movable + final
    output_list = initial_segment + white_gap + movable_block + final_segment

    # Convert back to numpy array with the shape (1, M)
    # M should be equal to N as we only reordered elements
    output_grid = np.array([output_list], dtype=input_grid.dtype)

    return output_grid
