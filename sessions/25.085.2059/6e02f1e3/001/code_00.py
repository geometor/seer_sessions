import numpy as np

"""
Transforms a 3x3 input grid based on the number of distinct non-white colors present.

1.  Counts the number of unique non-white colors in the 3x3 input grid (N).
2.  Creates a 3x3 output grid initialized with white (0).
3.  If N = 1, the top row of the output grid is set to gray (5).
4.  If N = 2, the main diagonal (top-left to bottom-right) of the output grid is set to gray (5).
5.  If N = 3, the anti-diagonal (top-right to bottom-left) of the output grid is set to gray (5).
"""

def count_distinct_non_white_colors(grid):
    """Counts the number of unique colors in the grid, excluding white (0)."""
    unique_colors = np.unique(grid)
    non_white_colors = unique_colors[unique_colors != 0]
    return len(non_white_colors)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_array = np.array(input_grid, dtype=int)
    
    # Ensure input is 3x3, though examples suggest it always is
    if input_array.shape != (3, 3):
        # In a real scenario, might raise an error or handle differently
        # For ARC, assume valid input based on examples
        pass 
        
    # Count the distinct non-white colors in the input
    num_distinct_colors = count_distinct_non_white_colors(input_array)
    
    # Initialize a 3x3 output grid with white (0)
    output_grid = np.zeros((3, 3), dtype=int)
    
    # Apply the pattern based on the count of distinct colors
    if num_distinct_colors == 1:
        # Set the top row to gray (5)
        output_grid[0, :] = 5
    elif num_distinct_colors == 2:
        # Set the main diagonal to gray (5)
        np.fill_diagonal(output_grid, 5)
    elif num_distinct_colors == 3:
        # Set the anti-diagonal to gray (5)
        # This can be done by setting elements where row + col == size - 1
        output_grid[0, 2] = 5
        output_grid[1, 1] = 5
        output_grid[2, 0] = 5
        # Alternative using numpy indexing for anti-diagonal:
        # rows, cols = np.arange(3), np.arange(3)[::-1]
        # output_grid[rows, cols] = 5
        # However, the explicit setting might be clearer for a 3x3 grid

    # Convert the numpy array back to a list of lists for the ARC standard
    return output_grid.tolist()
