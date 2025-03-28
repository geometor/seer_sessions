```python
import numpy as np

"""
Fill horizontal segments between pairs of non-white pixels with red (2).

Iterate through each row of the input grid. For each row, identify the column 
indices of all non-white pixels ("endpoints"). If a row has two or more 
endpoints, consider consecutive pairs of these endpoints (in sorted column order). 
For each pair (col1, col2), check if all pixels in the original input grid 
strictly between col1 and col2 in that row are white (0). If they are, 
change the corresponding pixels in the output grid to red (2).
"""

def transform(input_grid):
    """
    Applies the horizontal fill transformation to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, this will be the output grid
    output_grid = np.copy(input_np)
    
    num_rows, num_cols = input_np.shape

    # Define the fill color
    fill_color = 2
    background_color = 0

    # Iterate through each row
    for r in range(num_rows):
        # Find the column indices of all non-white pixels in the current row
        endpoint_cols = np.where(input_np[r, :] != background_color)[0]
        
        # Sort the indices (np.where usually returns sorted, but being explicit is good)
        endpoint_cols.sort()

        # Need at least two endpoints to form a segment
        if len(endpoint_cols) >= 2:
            # Iterate through consecutive pairs of endpoints
            for i in range(len(endpoint_cols) - 1):
                col1 = endpoint_cols[i]
                col2 = endpoint_cols[i+1]

                # Check if there's a gap between the endpoints
                if col2 > col1 + 1:
                    # Get the segment between the endpoints in the *original* input grid
                    intermediate_segment = input_np[r, col1 + 1 : col2]
                    
                    # Check if all pixels in the intermediate segment are the background color
                    if np.all(intermediate_segment == background_color):
                        # If yes, fill the corresponding segment in the output grid with the fill color
                        output_grid[r, col1 + 1 : col2] = fill_color

    return output_grid.tolist() # Return as list of lists, as per ARC standard format
```