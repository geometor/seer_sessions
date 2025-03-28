"""
Identify 2x2 squares of a uniform color (not the border color) within the input grid.
Determine the border color from the input grid's edge.
Find the unique row and column coordinates of the top-left corners of these 2x2 squares.
Create an output grid with dimensions determined by the number of unique rows and columns found (minimum 2x2), initialized with the border color.
Place the color of each identified 2x2 square into the output grid at the position corresponding to the relative order of its row and column coordinates.
"""

import numpy as np

def find_uniform_2x2_squares(grid, border_color):
    """
    Finds all 2x2 squares of a single color, excluding the border color.

    Args:
        grid (np.array): The input grid.
        border_color (int): The color of the border.

    Returns:
        list: A list of tuples, where each tuple contains (color, row, col)
              of the top-left corner of a found 2x2 square.
    """
    squares = []
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            # Extract the 2x2 subgrid
            subgrid = grid[r:r+2, c:c+2]
            
            # Check if all elements are the same
            first_pixel = subgrid[0, 0]
            if np.all(subgrid == first_pixel):
                # Check if the color is not the border color
                if first_pixel != border_color:
                    squares.append((first_pixel, r, c))
    return squares

def transform(input_grid):
    """
    Transforms the input grid based on the locations of 2x2 uniform color squares.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier slicing
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Determine the border_color
    # Assuming the border is always 1 pixel thick and consistent
    border_color = grid[0, 0]

    # 2. Search for 2x2 squares
    found_squares = find_uniform_2x2_squares(grid, border_color)

    # 3. Record square colors and coordinates (already done in find_uniform_2x2_squares)
    
    # Handle case where no squares are found
    if not found_squares:
        # Default to a 2x2 output grid filled with border color
        output_grid = np.full((2, 2), border_color, dtype=int)
        return output_grid.tolist()

    # 4. Collect unique row and column coordinates
    unique_rows = sorted(list(set(r for _, r, _ in found_squares)))
    unique_cols = sorted(list(set(c for _, _, c in found_squares)))

    # 5. Calculate output grid dimensions
    num_rows = max(2, len(unique_rows))
    num_cols = max(2, len(unique_cols))

    # 6. Create the output grid, initialized with border_color
    output_grid = np.full((num_rows, num_cols), border_color, dtype=int)

    # 7. Map objects to the output grid
    # Create mappings from coordinate value to output grid index
    row_map = {r: i for i, r in enumerate(unique_rows)}
    col_map = {c: j for i, c in enumerate(unique_cols)}

    # Iterate through the recorded squares and place their colors
    for color, r, c in found_squares:
        output_r = row_map.get(r) # Use get in case a coordinate wasn't found (shouldn't happen here)
        output_c = col_map.get(c)
        
        # Only place if both row and col were found in the unique lists
        if output_r is not None and output_c is not None:
             output_grid[output_r, output_c] = color

    # 9. Return the final grid as a list of lists
    return output_grid.tolist()