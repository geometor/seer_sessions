import numpy as np
from typing import List, Tuple, Optional, Set

"""
Identify the grid divider color (forming full horizontal and vertical lines).
Identify the two distinct 'payload' colors (neither background nor divider).
Create the output grid by swapping the two payload colors wherever they appear
in the input grid, leaving the background and divider colors unchanged.
"""

def find_divider_color(grid: np.ndarray) -> Optional[int]:
    """
    Identifies the color used for grid divider lines.
    It checks for colors that form at least one complete row AND one complete column.
    Falls back to the most frequent non-background color if the line criteria aren't met.
    """
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    # Consider only non-background colors as potential dividers
    non_bg_colors = unique_colors[unique_colors != 0]

    for color in non_bg_colors:
        has_full_row = False
        # Check if this color forms any full row
        for r in range(rows):
            if np.all(grid[r, :] == color):
                has_full_row = True
                break
        
        # If no full row exists for this color, it can't be the divider by this definition
        if not has_full_row:
            continue

        has_full_col = False
        # Check if this color forms any full column
        for c in range(cols):
             if np.all(grid[:, c] == color):
                has_full_col = True
                break
        
        # If a color forms both a full row and a full column, identify it as the divider
        if has_full_col: # has_full_row is already true if we reached here
            return color

    # Fallback: If no color strictly forms full lines, assume the most frequent
    # non-background color is the divider.
    # print("Warning: Strict divider line not found, using frequency fallback.")
    colors, counts = np.unique(grid[grid != 0], return_counts=True)
    if len(colors) > 0:
        # Find the index of the maximum count
        max_count_index = np.argmax(counts)
        # Return the color corresponding to the maximum count
        return colors[max_count_index]
    else:
        # No non-background colors found at all
        return None

def find_payload_colors(grid: np.ndarray, divider_color: Optional[int]) -> List[int]:
    """
    Identifies the payload colors in the grid.
    These are defined as all unique colors that are not the background (0)
    and not the divider color.
    """
    unique_colors = np.unique(grid)
    payload_colors = []
    for color in unique_colors:
        # Payload colors are not background (0) and not the divider color
        if color != 0 and color != divider_color:
            payload_colors.append(color)
    return payload_colors

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by swapping the two payload colors.

    1. Converts the input list of lists to a NumPy array.
    2. Identifies the divider color.
    3. Identifies the two payload colors.
    4. Creates a copy of the input grid.
    5. Iterates through the grid, swapping payload colors in the copied grid.
    6. Converts the resulting NumPy array back to a list of lists.
    """
    # Convert input to NumPy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    
    # Find the divider color
    divider_color = find_divider_color(grid)
    # If no divider found (e.g., grid is all background), return original
    # if divider_color is None:
        # print("Warning: No divider color identified.")
        # return input_grid # Or grid.tolist()

    # Find the payload colors (expected to be 2)
    payload_colors = find_payload_colors(grid, divider_color)

    # Check if exactly two payload colors were found
    if len(payload_colors) != 2:
        # If not exactly two payload colors, something is unexpected.
        # Based on the examples, swapping isn't defined or needed.
        # Return the original grid unchanged.
        # print(f"Warning: Expected 2 payload colors, found {len(payload_colors)}. Returning original grid.")
        return input_grid # Return original list of lists

    payload1, payload2 = payload_colors

    # Create a copy of the grid to modify
    output_grid = grid.copy()

    # Iterate through each pixel of the grid
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            # If the pixel is the first payload color, change it to the second
            if grid[r, c] == payload1:
                output_grid[r, c] = payload2
            # If the pixel is the second payload color, change it to the first
            elif grid[r, c] == payload2:
                output_grid[r, c] = payload1
            # Otherwise (background or divider color), leave it unchanged (already copied)

    # Convert the result back to a list of lists format
    return output_grid.tolist()
