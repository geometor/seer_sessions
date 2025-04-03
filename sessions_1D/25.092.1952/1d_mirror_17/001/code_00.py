import numpy as np
from typing import List, Tuple, Optional

"""
Reflect a colored horizontal segment across a fixed pivot pixel (maroon, 9) in a 1D grid.

The transformation identifies a single pivot pixel (color 9) and a contiguous horizontal 
segment of a different color (not white 0 and not maroon 9). It then reflects the position 
of this segment across the pivot pixel. The original segment is removed (set to white 0), 
and the segment is redrawn in its reflected position with the same color and length.
"""

def find_pixel(grid: np.ndarray, color: int) -> Optional[int]:
    """Finds the column index of the first pixel with the given color."""
    indices = np.where(grid == color)[0]
    if len(indices) > 0:
        return indices[0]
    return None

def find_segment(grid: np.ndarray, pivot_col: Optional[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the contiguous segment of color that is not white (0) or maroon (9).
    Returns (color, start_col, end_col) or None if not found.
    """
    segment_color = -1
    start_col = -1
    end_col = -1
    
    for col_idx, pixel_color in enumerate(grid):
        # Skip background (0) and pivot (9)
        if pixel_color == 0 or (pivot_col is not None and col_idx == pivot_col):
            # If we were tracking a segment, it ends here
            if start_col != -1:
                end_col = col_idx - 1
                return segment_color, start_col, end_col
            continue

        # Found a potential start of a segment
        if start_col == -1:
            segment_color = pixel_color
            start_col = col_idx
        # If the color changes mid-segment (shouldn't happen based on examples)
        # or continues the current segment
        elif pixel_color != segment_color:
             # This case implies multiple segments or errors, return the first found
             end_col = col_idx - 1
             return segment_color, start_col, end_col

    # Check if the segment runs to the end of the grid
    if start_col != -1:
        end_col = len(grid) - 1
        return segment_color, start_col, end_col
        
    return None # No segment found

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the reflection transformation to the input grid.
    
    Args:
        input_grid: A list of integers representing the 1D input grid.
        
    Returns:
        A list of integers representing the 1D output grid.
    """
    # Convert list to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Initialize output grid as a copy of the input
    output_grid = grid.copy()

    # 1. Find the pivot pixel (color 9)
    pivot_col = find_pixel(grid, 9)
    if pivot_col is None:
        print("Warning: Pivot pixel (9) not found.")
        return input_grid # Return original if pivot is missing

    # 2. Find the colored segment (not 0 and not 9)
    segment_info = find_segment(grid, pivot_col)
    if segment_info is None:
        print("Warning: Colored segment not found.")
        return input_grid # Return original if segment is missing
        
    segment_color, start_col, end_col = segment_info
    
    # 3. Erase the original segment in the output grid
    output_grid[start_col : end_col + 1] = 0 # Set to background color

    # 4. Calculate the new position by reflecting across the pivot
    # Reflection formula: new_pos = pivot_pos + (pivot_pos - old_pos) = 2 * pivot_pos - old_pos
    # The new segment will start at the reflection of the old end point
    # and end at the reflection of the old start point.
    new_start_col = 2 * pivot_col - end_col
    new_end_col = 2 * pivot_col - start_col

    # Ensure calculated indices are within grid bounds (although not strictly needed for simple reflection if grid is large enough)
    grid_width = len(grid)
    new_start_col = max(0, new_start_col)
    new_end_col = min(grid_width - 1, new_end_col)

    # Check if new indices are valid (start <= end)
    if new_start_col > new_end_col:
         print(f"Warning: Invalid reflection indices calculated (new_start={new_start_col}, new_end={new_end_col}). Segment might overlap pivot or calculation error.")
         # Depending on exact rules, might return original or partially drawn segment
         # For now, proceed but it might draw nothing if range is invalid for slicing

    # 5. Draw the segment at the new reflected position
    # Ensure the slice indices are correct for numpy array slicing [start:end+1]
    if new_start_col <= new_end_col:
         output_grid[new_start_col : new_end_col + 1] = segment_color
    
    # Convert numpy array back to list before returning
    return output_grid.tolist()