"""
Rotates all non-background pixels 180 degrees around a central pivot 
pixel identified by the color gray (5). The background color is white (0).
The output grid has the same dimensions as the input grid. Pixels rotated 
outside the grid boundaries are discarded (though based on examples, this may not occur).
"""

import numpy as np

def find_pivot(grid, pivot_color=5):
    """
    Finds the coordinates (row, col) of the first pixel with the pivot_color.

    Args:
        grid (np.ndarray): The grid to search within.
        pivot_color (int): The color value of the pivot pixel.

    Returns:
        tuple[int, int] | None: The (row, col) of the pivot, or None if not found.
    """
    pivot_coords = np.where(grid == pivot_color)
    if len(pivot_coords[0]) > 0:
        # Return the coordinates of the first occurrence
        return int(pivot_coords[0][0]), int(pivot_coords[1][0])
    else:
        # Should not happen based on task description, but handle defensively
        return None 

def transform(input_grid):
    """
    Rotates the non-background pixels of the input grid 180 degrees 
    around the gray (5) pivot pixel.

    Args:
        input_grid (list[list[int]]): The input grid as a 2D list of integers.

    Returns:
        list[list[int]]: The transformed grid as a 2D list of integers.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    background_color = 0
    pivot_color = 5

    # 1. Initialize output grid with background color
    output_np = np.full_like(input_np, background_color)

    # 2. Find the coordinates (center_row, center_col) of the gray pivot pixel
    center_coords = find_pivot(input_np, pivot_color)
    
    # Handle case where pivot is not found (unlikely based on examples)
    if center_coords is None:
        print(f"Warning: Pivot color ({pivot_color}) not found in input grid. Returning original grid.")
        return input_grid 
        
    center_row, center_col = center_coords

    # 3. Iterate through every pixel in the input grid
    for input_row in range(rows):
        for input_col in range(cols):
            color = input_np[input_row, input_col]

            # 4. If the color is not the background color
            if color != background_color:
                # a. Calculate relative coordinates to the pivot
                relative_row = input_row - center_row
                relative_col = input_col - center_col

                # b. Apply 180-degree rotation transformation:
                # (x, y) rotated 180 deg becomes (-x, -y)
                # In grid coords (row, col): relative_row is like y, relative_col is like x
                # new_relative_col = -relative_col
                # new_relative_row = -relative_row 
                new_relative_row = -relative_row
                new_relative_col = -relative_col

                # c. Calculate new absolute coordinates based on the pivot
                output_row = center_row + new_relative_row
                output_col = center_col + new_relative_col

                # d. Check if the new coordinates are within the grid bounds
                if 0 <= output_row < rows and 0 <= output_col < cols:
                    # Place the original color at the new rotated position
                    output_np[output_row, output_col] = color
                # else:
                    # Pixel rotates out of bounds, effectively discarded (left as background)

    # 5. Convert the result back to list of lists for the required output format
    output_grid = output_np.tolist()
    
    # Return the completed output grid
    return output_grid