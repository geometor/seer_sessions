```python
import numpy as np

"""
Transforms an input grid based on the following rules:
1. Create a new output grid with the same dimensions as the input grid, initially filled entirely with white pixels (color 0).
2. Identify the locations (row, column coordinates) of all gray pixels (color 5) in the input grid. Store these locations.
3. Identify all column indices 'c' in the input grid that contain at least one red pixel (color 2).
4. Create an empty set to store the target column indices that will be filled with red in the output grid.
5. For each identified input column 'c' that contains red:
    a. Check if this same column 'c' in the input grid also contains at least one gray pixel (color 5).
    b. If column 'c' contains *both* red and gray, add the index 'c + 1' to the set of target red columns (ensure 'c + 1' is a valid column index within the grid width).
    c. If column 'c' contains red but *does not* contain gray, add the index 'c' to the set of target red columns.
6. For every column index stored in the set of target red columns, fill the entire corresponding column in the output grid with red pixels (color 2).
7. Iterate through the stored locations of the original gray pixels. For each location (r, c), set the pixel at (r, c) in the output grid to gray (color 5). This step overwrites any color previously placed in that cell (including red from step 6).
8. Return the final output grid.
"""

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Initialize the output grid with the same dimensions, filled with white (0).
    output_grid = np.zeros_like(input_grid_np)

    # 2. Identify locations of gray pixels (5) in the *input* grid.
    gray_coords = np.where(input_grid_np == 5)
    # gray_coords is a tuple of arrays: (row_indices, column_indices)

    # 3. Identify source columns containing red pixels.
    source_red_columns = set()
    for c in range(width):
        if np.any(input_grid_np[:, c] == 2):
            source_red_columns.add(c)

    # 4. & 5. Determine the target columns to be filled red.
    target_red_columns = set()
    for c in source_red_columns:
        # 5.a. Check if the source column 'c' also contains gray.
        column_data = input_grid_np[:, c]
        has_gray = np.any(column_data == 5)

        # 5.b. If gray is present, target column is 'c + 1'.
        if has_gray:
            target_col = c + 1
            # Ensure the target column is within grid bounds.
            if 0 <= target_col < width:
                target_red_columns.add(target_col)
        # 5.c. If only red (no gray), target column is 'c'.
        else:
            target_red_columns.add(c)

    # 6. Fill the identified target columns in the output grid with red (2).
    for c in target_red_columns:
        output_grid[:, c] = 2

    # 7. Place the original gray pixels (5) into the output grid, overwriting.
    for r, c in zip(gray_coords[0], gray_coords[1]):
        # Ensure coordinates are valid (though they should be if from input)
        if 0 <= r < height and 0 <= c < width:
             output_grid[r, c] = 5 # Overwrite with gray

    # 8. Convert back to list of lists for ARC standard output format
    return output_grid.tolist()
```