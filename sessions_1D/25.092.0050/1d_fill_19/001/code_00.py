import numpy as np

"""
For each row in the input grid:
1. Identify all unique non-white colors present in the row.
2. For each unique non-white color 'C':
    a. Find the index of the first (leftmost) occurrence of 'C'.
    b. Find the index of the last (rightmost) occurrence of 'C'.
    c. If the first and last indices are different (meaning 'C' appears at least twice):
        i. Check if all pixels strictly between the first and last occurrences are white (0).
        ii. If they are all white, change the color of these intervening pixels to 'C' in the output grid.
3. Return the modified grid.
"""

def transform(input_grid):
    """
    Fills segments between the first and last occurrence of a non-white color 
    in a row with that color, if all pixels in between are white.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Convert input to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_array = input_array.copy()
    
    height, width = input_array.shape

    # Iterate through each row of the grid
    for r in range(height):
        # Get the current row
        row = input_array[r, :]
        
        # Find unique non-white colors (values > 0) in this row
        # Using np.unique automatically sorts them, which doesn't matter here
        unique_colors = np.unique(row[row > 0])

        # Process each unique non-white color found
        for color in unique_colors:
            # Find all column indices where this color appears in the current row
            indices = np.where(row == color)[0]

            # Proceed only if the color appears at least twice
            if len(indices) > 1:
                # Find the index of the first (leftmost) occurrence
                first_idx = np.min(indices)
                # Find the index of the last (rightmost) occurrence
                last_idx = np.max(indices)

                # Check if there's actually a gap between the first and last occurrences
                # (i.e., they are not adjacent)
                if last_idx > first_idx + 1:
                    # Extract the segment of pixels strictly between the first and last occurrences
                    segment_to_check = row[first_idx + 1 : last_idx]

                    # Check if all pixels within this segment are white (0)
                    if np.all(segment_to_check == 0):
                        # If all are white, fill this segment in the output grid's corresponding row with the current color
                        output_array[r, first_idx + 1 : last_idx] = color

    # Convert the result back to a list of lists format
    return output_array.tolist()
