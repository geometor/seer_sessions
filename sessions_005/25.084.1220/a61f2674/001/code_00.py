"""
Transforms an input grid by analyzing the count of gray pixels (5) in each column.
Gray pixels in columns with the maximum count are changed to blue (1).
Gray pixels in columns with the minimum non-zero count are changed to red (2).
All other gray pixels are changed to white (0).
The background remains white (0).
"""

import numpy as np

def get_column_counts(grid):
    """
    Counts the number of gray pixels (5) in each column.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        dict: A dictionary where keys are column indices and values are the 
              counts of gray pixels in that column (only includes columns with count > 0).
    """
    counts = {}
    height, width = grid.shape
    for col in range(width):
        count = np.sum(grid[:, col] == 5)
        if count > 0:
            counts[col] = count
    return counts

def transform(input_grid):
    """
    Applies the transformation rule based on gray pixel counts per column.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid with the same dimensions, filled with white (0)
    output_grid = np.zeros_like(input_np)

    # 1. Analyze the input grid column by column to count gray pixels (5)
    column_counts = get_column_counts(input_np)

    # 2. Handle the case where there are no gray pixels
    if not column_counts:
        return output_grid.tolist() # Return as list of lists

    # 3. Identify the maximum and minimum non-zero counts
    counts_values = list(column_counts.values())
    max_count = max(counts_values)
    min_count = min(counts_values)

    # 4. Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # 5. Check if the pixel is gray (5)
            if input_np[r, c] == 5:
                # a. Get the count for the current column
                current_col_count = column_counts.get(c) # Use .get() in case a column had 0 gray pixels (though already filtered)
                
                # b. Apply transformation based on max count
                if current_col_count == max_count:
                    output_grid[r, c] = 1 # Set to blue
                # c. Apply transformation based on min count
                elif current_col_count == min_count:
                    output_grid[r, c] = 2 # Set to red
                # d. Otherwise, it remains white (0) as initialized

    # 6. Return the completed output grid as a list of lists
    return output_grid.tolist()