import numpy as np
from collections import Counter
import math

"""
The transformation operates on two specific columns determined by the input grid's content: 
C1 (the rightmost column with any non-background pixel) and C2 (the second rightmost column with any non-background pixel).
It identifies the topmost non-background pixel in each of these input columns (V_top_C1 at R_top_C1, and V_top_C2 at R_top_C2).
The output grid is initialized with the background color.
Then, column C1 of the output is populated: pixels from input column C1 are copied if they are not background; background pixels in output C1 *above* R_top_C1 are filled with V_top_C2.
Next, column C2 of the output is populated: pixels from input column C2 are copied if they are not background; background pixels in output C2 *above* R_top_C2 are filled with V_top_C2, but *only if* a condition based on the content of column C1 at the same row is met (specifically, if the already computed output value at C1 is background, OR if the original input value at C1 was V_top_C1).
All other columns in the output remain background color.
"""

def find_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid, assumed to be the background.
       More robustly checks if 0 is dominant even if not most frequent.
    """
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default background if grid is empty

    if grid.size > 0:
        # Check if 0 is present and covers a large area (e.g., >50% or most frequent)
        zero_count = counts.get(0, 0)
        if counts:
            most_frequent_color, most_frequent_count = counts.most_common(1)[0]
            # Prioritize 0 if it's the most frequent or covers more than half the grid
            if zero_count == most_frequent_count or zero_count > grid.size * 0.5:
                 background_color = 0
            else:
                 background_color = most_frequent_color # Fallback to simple mode if 0 isn't dominant
        else: # Grid has elements but Counter is empty? Should not happen with ndarray
            background_color = 0

    else: # Grid is empty
        background_color = 0
    return background_color

def find_target_columns(grid: np.ndarray, background_color: int) -> tuple[int | None, int | None]:
    """
    Finds the indices of the rightmost (C1) and second rightmost (C2) columns
    containing non-background pixels.
    Returns (C1, C2). Returns None for an index if not found.
    """
    rows, cols = grid.shape
    non_bg_cols = set()
    if grid.size == 0:
        return None, None
    for c in range(cols):
        # Check if any element in the column is not the background color
        if np.any(grid[:, c] != background_color):
            non_bg_cols.add(c)

    # Sort the column indices that contain non-background colors
    sorted_cols = sorted(list(non_bg_cols))

    # C1 is the largest index (rightmost)
    C1 = sorted_cols[-1] if sorted_cols else None
    # C2 is the second largest index (second rightmost)
    C2 = sorted_cols[-2] if len(sorted_cols) > 1 else None

    return C1, C2

def find_topmost_non_background(grid: np.ndarray, col_idx: int | None, background_color: int) -> tuple[int | None, int | None]:
    """
    Finds the row index (R_top) and value (V_top) of the topmost
    non-background pixel in the specified column.
    Returns (R_top, V_top). If column is empty, invalid, or None,
    returns (None, None).
    """
    height = grid.shape[0]
    # Check if the column index is valid
    if col_idx is None or col_idx < 0 or col_idx >= grid.shape[1]:
        return None, None # Indicate no pixel found / invalid column

    # Extract the column data
    column_data = grid[:, col_idx]
    # Find indices of non-background pixels
    non_bg_indices = np.where(column_data != background_color)[0]

    # If no non-background pixels found in the column
    if non_bg_indices.size == 0:
        return None, None # Indicate no pixel found

    # The topmost non-background pixel is the first one found
    R_top = non_bg_indices[0]
    V_top = grid[R_top, col_idx]
    return R_top, V_top


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the defined logic involving C1, C2,
    and upward filling based on topmost pixels V_top_C1 and V_top_C2.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Handle empty input grid case
    if input_np.size == 0:
        return []
        
    height, width = input_np.shape

    # Step 1: Determine the background color
    bg = find_background_color(input_np)

    # Step 2 & 3: Identify target columns C1 and C2
    C1, C2 = find_target_columns(input_np, bg)

    # Handle edge case: No non-background pixels found at all
    if C1 is None:
        # Return a grid filled with background color, or the original grid
        # Returning original seems safer based on some ARC task behaviors
        return input_grid

    # Step 4: Find topmost non-background pixel in C1
    R_top_C1, V_top_C1 = find_topmost_non_background(input_np, C1, bg)

    # Step 5: Find topmost non-background pixel in C2
    R_top_C2, V_top_C2 = find_topmost_non_background(input_np, C2, bg)
    
    # If V_top_C2 wasn't found (e.g., C2 is None or empty), default fill value for C1 gaps might be background
    # The logic uses V_top_C2 for filling, so we need a defined value. Let's use bg if V_top_C2 is None.
    fill_val_for_c1_gaps = V_top_C2 if V_top_C2 is not None else bg
    # Similarly, for C2 gaps
    fill_val_for_c2_gaps = V_top_C2 if V_top_C2 is not None else bg

    # Step 6: Create the output grid initialized with the background color
    output_np = np.full_like(input_np, bg)

    # Step 7: Process output column C1
    for r in range(height):
        # Get the value from the input grid at this position
        V_current_C1 = input_np[r, C1]
        # If the input pixel is not background, copy it to the output
        if V_current_C1 != bg:
            output_np[r, C1] = V_current_C1
        # If the input pixel IS background AND we are above the topmost pixel in C1
        elif R_top_C1 is not None and r < R_top_C1:
             # Fill this background cell with the topmost value from C2 (or bg if C2 had no top pixel)
            output_np[r, C1] = fill_val_for_c1_gaps
        # Otherwise (it's background at or below R_top_C1), leave it as background (already initialized)

    # Step 8: Process output column C2 (only if C2 exists)
    if C2 is not None:
        for r in range(height):
            # Get the value from the input grid at this position
            V_current_C2 = input_np[r, C2]
             # If the input pixel is not background, copy it to the output
            if V_current_C2 != bg:
                output_np[r, C2] = V_current_C2
            # If the input pixel IS background AND we are above the topmost pixel in C2
            elif R_top_C2 is not None and r < R_top_C2:
                # Check the condition for upward fill in C2
                # Condition: (output[r, C1] == bg) OR (input[r, C1] == V_top_C1)
                condition_met = False
                # Part 1: Check if the corresponding cell in the *output* C1 is background
                if output_np[r, C1] == bg:
                    condition_met = True
                # Part 2: Check if the corresponding cell in the *input* C1 equals V_top_C1
                # This check is only valid if V_top_C1 was actually found (R_top_C1 is not None)
                elif R_top_C1 is not None and input_np[r, C1] == V_top_C1:
                     condition_met = True

                # If the condition is met, fill this background cell with V_top_C2 (or bg if C2 had no top pixel)
                if condition_met:
                    output_np[r, C2] = fill_val_for_c2_gaps
            # Otherwise (it's background at or below R_top_C2, or condition not met), leave it as background

    # Step 9: Convert the final NumPy array back to a list of lists and return
    return output_np.tolist()