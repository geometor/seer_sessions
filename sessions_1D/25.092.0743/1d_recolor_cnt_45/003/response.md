```python
"""
Transforms the input grid by replacing horizontal contiguous segments of azure pixels (8) 
with segments of the same length but different colors based on the segment length.
Length 1 -> orange (7), Length 2 -> green (3), Length 3 -> red (2).
Other pixels remain unchanged. The transformation is applied row by row.
"""

import numpy as np

def find_horizontal_segments(row, target_color):
    """
    Finds all contiguous horizontal segments of a target color in a given row.

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.
        target_color (int): The color value to search for segments of.

    Returns:
        list: A list of tuples, where each tuple is (start_col, length).
    """
    segments = []
    n_cols = len(row)
    col = 0
    while col < n_cols:
        if row[col] == target_color:
            start_col = col
            length = 0
            # Count consecutive target_color pixels
            while col < n_cols and row[col] == target_color:
                length += 1
                col += 1
            # Store the found segment
            segments.append((start_col, length))
            # col is already advanced past the segment
        else:
            # Move to the next column if not target_color
            col += 1
    return segments

def transform(input_grid):
    """
    Applies the segment replacement transformation to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    # Create a copy to store the output, initialized with the input grid values
    output_grid = grid.copy()
    
    # Define the mapping from segment length to the replacement color
    length_to_color_map = {
        1: 7,  # orange
        2: 3,  # green
        3: 2,  # red
    }
    # Define the target color to find segments of
    target_color = 8 # azure

    n_rows, _ = grid.shape

    # Iterate through each row of the grid
    for r in range(n_rows):
        # Find all horizontal segments of the target color in the current row
        segments = find_horizontal_segments(grid[r, :], target_color)
        
        # Process each found segment
        for start_col, length in segments:
            # Check if the segment length has a defined replacement color
            if length in length_to_color_map:
                replacement_color = length_to_color_map[length]
                # Replace the segment in the output grid row with the new color
                # Slicing end index is exclusive, so start_col + length is correct
                output_grid[r, start_col:start_col + length] = replacement_color
            # If length is not in the map, the segment remains unchanged (as output_grid is a copy)

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
```