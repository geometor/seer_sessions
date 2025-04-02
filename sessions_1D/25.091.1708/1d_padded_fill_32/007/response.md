```python
import numpy as np

"""
Transforms the input grid by processing each row independently. 
For each row:
1. Identifies the non-background color (any color other than white/0). Assumes only one non-background color per row if any exist.
2. Finds the leftmost (minimum column index) and rightmost (maximum column index) occurrences of this non-background color within that row.
3. If a non-background color exists in the row, it fills the segment between the leftmost and rightmost occurrences (inclusive) in the output grid's corresponding row with that non-background color.
4. Rows containing only the background color (white/0) remain unchanged.
The output grid has the same dimensions as the input grid.
"""

def transform(input_grid):
    """
    Fills the horizontal span between the first and last non-background pixel 
    in each row independently.

    Args:
        input_grid (list of list of int): The input grid represented as a 2D list.

    Returns:
        list of list of int: The transformed grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    
    # Create a copy of the input array to modify for the output.
    # This ensures that rows with only background color are handled correctly 
    # as they won't be modified later.
    output_np = input_np.copy()
    
    # Get the number of rows in the grid
    rows = input_np.shape[0]
    
    # Define the background color explicitly (standard is 0 for white)
    background_color = 0
    
    # Iterate through each row index
    for r in range(rows):
        # Get the current row from the input grid
        row = input_np[r, :]
        
        # Find the column indices of all pixels that are NOT the background color
        # np.where returns a tuple of arrays; for a 1D array like a row, 
        # we need the first element which contains the indices.
        foreground_indices = np.where(row != background_color)[0]
        
        # Check if any non-background pixels were found in this row
        if foreground_indices.size > 0:
            # Determine the non-background color present in this row.
            # Based on examples, we assume only one non-background color per row.
            # We can reliably get this color from the first foreground pixel found.
            foreground_color = row[foreground_indices[0]]
            
            # Find the minimum column index (leftmost occurrence) among the foreground pixels
            min_col = np.min(foreground_indices)
            
            # Find the maximum column index (rightmost occurrence) among the foreground pixels
            max_col = np.max(foreground_indices)
            
            # In the output grid's corresponding row, fill the pixels
            # from min_col up to max_col (inclusive) with the identified foreground color.
            # NumPy slicing is [start:end], where end is exclusive, so use max_col + 1.
            output_np[r, min_col : max_col + 1] = foreground_color
            
        # else: If foreground_indices is empty, the row contains only background pixels.
        # Since output_np started as a copy of the input, this row is already 
        # correct and requires no changes.

    # Convert the modified NumPy array back to a standard list of lists format
    # for the return value, as expected by the ARC environment.
    return output_np.tolist()

```