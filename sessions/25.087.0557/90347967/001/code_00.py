import numpy as np

"""
Rotates all non-background pixels 90 degrees clockwise around a central pivot 
pixel identified by the color gray (5). The background color is white (0).
The output grid has the same dimensions as the input grid. Pixels rotated 
outside the grid boundaries are discarded.
"""

def find_pivot(grid, pivot_color=5):
    """Finds the coordinates of the first pixel with the pivot_color."""
    for r_idx, row in enumerate(grid):
        for c_idx, color in enumerate(row):
            if color == pivot_color:
                return r_idx, c_idx
    # Raise an error or return None if pivot not found? 
    # For this task, based on examples, we assume it always exists.
    return None 

def transform(input_grid):
    """
    Rotates the non-background pixels of the input grid 90 degrees clockwise 
    around the gray (5) pixel.

    Args:
        input_grid (list[list[int]]): The input grid as a 2D list of integers.

    Returns:
        list[list[int]]: The transformed grid as a 2D list of integers.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    background_color = 0
    pivot_color = 5

    # Initialize output grid with background color
    output_np = np.full_like(input_np, background_color)

    # 1. Locate the coordinates (center_row, center_col) of the gray pixel
    center_coords = find_pivot(input_np, pivot_color)
    if center_coords is None:
        # Handle case where pivot is not found - maybe return input or raise error
        # Based on task description, assuming pivot always exists.
        # For safety, return the input grid unchanged if no pivot.
        print("Warning: Pivot color (gray, 5) not found in input grid.")
        return input_grid 
    center_row, center_col = center_coords

    # 2. Iterate through every pixel in the input grid
    for input_row in range(rows):
        for input_col in range(cols):
            color = input_np[input_row, input_col]

            # 3. If the color is not the background color
            if color != background_color:
                # a. Calculate relative coordinates
                relative_row = input_row - center_row
                relative_col = input_col - center_col

                # b. Apply 90-degree clockwise rotation transformation
                # (x, y) rotated +90 deg becomes (y, -x)
                # In grid coords (row, col):
                # relative_row is like y, relative_col is like x
                # new_relative_col = relative_row
                # new_relative_row = -relative_col 
                # Let's re-verify the NL program logic:
                # NL: new_relative_row = relative_col, new_relative_col = -relative_row
                new_relative_row = relative_col
                new_relative_col = -relative_row

                # c. Calculate new absolute coordinates
                output_row = center_row + new_relative_row
                output_col = center_col + new_relative_col

                # d. Check if new coordinates are within bounds and place the color
                if 0 <= output_row < rows and 0 <= output_col < cols:
                    output_np[output_row, output_col] = color

    # Convert back to list of lists for the required output format
    output_grid = output_np.tolist()
    
    # 4. Return the completed output grid
    return output_grid