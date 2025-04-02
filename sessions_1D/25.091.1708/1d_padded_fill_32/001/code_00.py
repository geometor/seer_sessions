import numpy as np

"""
For each row in the input grid:
1. Identify the single non-white foreground color present in the row.
2. Find the column index of the leftmost occurrence (first instance) of this foreground color.
3. Find the column index of the rightmost occurrence (last instance) of this foreground color.
4. If a foreground color exists in the row, change the color of all pixels in the output grid's corresponding row, from the leftmost index to the rightmost index (inclusive), to the identified foreground color.
5. If no foreground color exists (the row is all white), the output row remains unchanged (all white).
Pixels outside the identified range (before the first foreground pixel and after the last foreground pixel) retain their original color (white background).
The dimensions of the output grid are identical to the input grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling the horizontal span between the first and last
    occurrence of the foreground color in each row.

    Args:
        input_grid (list of list of int): The input grid represented as a 2D list.

    Returns:
        list of list of int: The transformed grid.
    """
    # Convert input to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_np = input_np.copy()
    
    # Get the number of rows and columns
    rows, cols = input_np.shape
    
    # Define the background color (white)
    background_color = 0
    
    # Iterate through each row of the grid
    for r in range(rows):
        # Get the current row
        row = input_np[r, :]
        
        # Find the indices of all non-background pixels in the current row
        foreground_indices = np.where(row != background_color)[0]
        
        # Check if there are any foreground pixels in the row
        if foreground_indices.size > 0:
            # Identify the foreground color (assuming only one foreground color per row based on examples)
            # We can take the color of the first foreground pixel found
            foreground_color = row[foreground_indices[0]]
            
            # Find the minimum (leftmost) column index of the foreground color
            min_col = np.min(foreground_indices)
            # Find the maximum (rightmost) column index of the foreground color
            max_col = np.max(foreground_indices)
            
            # Fill the pixels in the output grid's row between min_col and max_col (inclusive)
            # with the foreground color
            output_np[r, min_col : max_col + 1] = foreground_color
            
        # If foreground_indices is empty, the row contains only the background color,
        # and the output row (being a copy) is already correct. No action needed.

    # Convert the numpy array back to a list of lists before returning
    return output_np.tolist()
