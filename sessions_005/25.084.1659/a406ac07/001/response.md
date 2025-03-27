```python
import numpy as np

"""
This program transforms an input grid based on patterns found in its last row.

1.  Initialize an output grid of the same size as the input, filled with the background color (0, white).
2.  Copy the last row and the last column from the input grid to the corresponding positions in the output grid.
3.  Analyze the last row of the input grid to identify contiguous horizontal segments (blocks) of identical, non-background colors.
4.  For each identified segment:
    a.  Record its color (C).
    b.  Record its length (n).
    c.  Record the starting column index (idx) of the segment.
    d.  In the output grid, draw a solid square of size n x n using color C, with its top-left corner positioned at (row=idx, column=idx).
5.  Return the modified output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by drawing squares based on color blocks in the last row.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid with background color (0)
    output_grid = np.zeros_like(input_np)
    
    # Copy the last row and last column from input to output
    if height > 0:
        output_grid[height - 1, :] = input_np[height - 1, :]
    if width > 0:
        output_grid[:, width - 1] = input_np[:, width - 1]
        
    # Handle edge case of 1x1 grid - already copied
    if height == 1 or width == 1:
        return output_grid.tolist()

    # Analyze the last row of the input grid (excluding the last column pixel as it's just border)
    last_row = input_np[height - 1, :]
    
    current_color = None
    start_index = -1
    count = 0
    
    # Iterate through the last row to find contiguous blocks
    for col in range(width): # Iterate through the full width
        color = last_row[col]
        
        if color != 0: # Found a non-background pixel
            if color == current_color:
                # Continue the current block
                count += 1
            else:
                # End of the previous block (if one exists)
                if current_color is not None and current_color != 0:
                    # Draw the square for the previous block
                    # Ensure the square fits within the non-border area
                    draw_size = min(count, height - 1 - start_index, width - 1 - start_index)
                    if draw_size > 0:
                         output_grid[start_index : start_index + draw_size, start_index : start_index + draw_size] = current_color

                # Start a new block
                current_color = color
                start_index = col
                count = 1
        else: # Found a background pixel (0)
            # End of the previous block (if one exists)
            if current_color is not None and current_color != 0:
                 # Draw the square for the previous block
                 # Ensure the square fits within the non-border area
                 draw_size = min(count, height - 1 - start_index, width - 1 - start_index)
                 if draw_size > 0:
                    output_grid[start_index : start_index + draw_size, start_index : start_index + draw_size] = current_color

            # Reset block tracking
            current_color = None
            start_index = -1
            count = 0

    # After the loop, check if the last block needs to be processed
    if current_color is not None and current_color != 0:
        # Draw the square for the final block
        # Ensure the square fits within the non-border area
        draw_size = min(count, height - 1 - start_index, width - 1 - start_index)
        if draw_size > 0:
            output_grid[start_index : start_index + draw_size, start_index : start_index + draw_size] = current_color

    # Ensure the copied last row/column are preserved if squares overlap them (though logic should prevent this if squares stay within top-left (h-1)x(w-1) area)
    # Re-copying is a safe way to ensure this.
    if height > 0:
        output_grid[height - 1, :] = input_np[height - 1, :]
    if width > 0:
        output_grid[:, width - 1] = input_np[:, width - 1]
            
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```