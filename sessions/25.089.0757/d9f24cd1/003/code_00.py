import numpy as np

"""
Transforms an input grid based on the following rules:
1. Initialize an output grid of the same dimensions as the input, filled with white (0).
2. Identify all columns 'c' in the input grid that contain at least one red pixel (2).
3. For each such column 'c':
    a. Check if this column 'c' also contains a gray pixel (5).
    b. If column 'c' contains both red and gray, the corresponding column to be filled red in the output grid is 'c + 1'.
    c. If column 'c' contains red but no gray, the corresponding column to be filled red in the output grid is 'c'.
4. Collect all the target column indices determined in step 3.
5. Fill the entirety of these target columns in the output grid with red (2).
6. Identify the locations of all gray pixels (5) in the input grid.
7. Place these gray pixels (5) at their original locations in the output grid, overwriting any existing color (including the red fill from step 5).
"""

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Initialize the output grid with the same dimensions, filled with white (0).
    output_grid = np.zeros_like(input_grid_np) # Defaults to 0 (white)

    # 2. & 3. Identify source columns containing red pixels and determine target columns based on gray pixel presence.
    target_red_columns = set()
    for c in range(width):
        column_data = input_grid_np[:, c]
        has_red = np.any(column_data == 2)

        if has_red:
            has_gray = np.any(column_data == 5)
            # 3b. If column 'c' contains both red and gray, target column is c + 1.
            if has_gray:
                target_col = c + 1
            # 3c. If column 'c' contains red but no gray, target column is c.
            else:
                target_col = c
                
            # 3d. Ensure target column is within grid bounds (although not strictly necessary based on examples)
            if 0 <= target_col < width:
                target_red_columns.add(target_col)

    # 5. Fill the identified target columns in the output grid with red (2).
    for c in target_red_columns:
        output_grid[:, c] = 2

    # 6. & 7. Identify locations of gray pixels (5) in the input and place them in the output, overwriting.
    gray_coords = np.where(input_grid_np == 5)
    # gray_coords is a tuple of arrays: (row_indices, column_indices)
    for r, c in zip(gray_coords[0], gray_coords[1]):
        # Ensure gray pixels are placed within bounds (original locations)
        if 0 <= r < height and 0 <= c < width:
             output_grid[r, c] = 5 # Overwrite with gray

    # Convert back to list of lists for ARC standard
    return output_grid.tolist()