import numpy as np

"""
Transforms an input grid into an output grid of the same dimensions based on a row-wise rule.
The background color is assumed to be white (0).

For each row in the input grid:
1. Identify all non-white pixels.
2. If there are exactly two non-white pixels in the row, and they share the same color (let's call it C):
    a. Find the column index of the leftmost non-white pixel (start_col).
    b. Find the column index of the rightmost non-white pixel (end_col).
    c. In the corresponding row of the output grid, fill the pixels from start_col to end_col (inclusive) with color C. All other pixels in this output row remain white (0).
3. If a row does not meet the condition in step 2 (i.e., it has 0, 1, or more than 2 non-white pixels, or the two non-white pixels have different colors), the corresponding output row is entirely white (0).

The output grid has the same height and width as the input grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by filling segments in rows based on pairs of identical non-white pixels.

    Args:
        input_grid (list of list of int): The input grid represented as a list of lists.

    Returns:
        list of list of int: The transformed output grid, with the same dimensions as the input.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    num_rows, num_cols = input_np.shape

    # Initialize the output grid with the same shape as the input, filled with the background color (white = 0)
    output_np = np.zeros_like(input_np)

    # Iterate through each row index
    for r in range(num_rows):
        # Get the current row from the input NumPy array
        row = input_np[r, :]
        
        # Find the column indices of all non-white pixels (pixels != 0) in the current row
        non_white_indices = np.where(row != 0)[0]

        # Check if exactly two non-white pixels were found in this row
        if len(non_white_indices) == 2:
            # Get the column indices of the two non-white pixels
            col1 = non_white_indices[0]
            col2 = non_white_indices[1]
            
            # Get the colors of these two pixels from the input row
            color1 = row[col1]
            color2 = row[col2]

            # Check if the colors of the two non-white pixels are the same
            if color1 == color2:
                # Identify the color to use for filling
                fill_color = color1
                
                # Determine the starting and ending columns for the segment to be filled.
                # Ensure start_col is the minimum and end_col is the maximum index.
                start_col = min(col1, col2)
                end_col = max(col1, col2)
                
                # Fill the corresponding segment in the output row.
                # NumPy slicing is [start:end+1] to include the end_col.
                output_np[r, start_col : end_col + 1] = fill_color
                
        # Else (if the row does not have exactly two non-white pixels of the same color):
            # The corresponding output row remains all white (0), 
            # as it was initialized. No action needed in this case.

    # Convert the final NumPy array back to a list of lists format before returning
    return output_np.tolist()