```python
import numpy as np

"""
This program transforms an input grid based on patterns found in its last row.

1.  Initialize an output grid of the same size as the input, filled with the background color (0, white).
2.  Copy the last row and the last column from the input grid to the corresponding positions in the output grid. This acts as a border or frame.
3.  Analyze the last row of the input grid (excluding the bottom-right corner pixel which belongs to both borders) to identify contiguous horizontal segments (blocks) of identical, non-background colors.
4.  For each identified segment:
    a.  Record its color (C).
    b.  Record its length (n).
    c.  Record the starting column index (idx) of the segment.
    d.  Determine the drawing area for a square based on this segment:
        i.  Top row: `row_start = idx`
        ii. Bottom row (exclusive): `row_end = min(idx + n, height - 1)` (Clip to not overwrite the last row border)
        iii.Left column: `col_start = idx`
        iv. Right column (exclusive): `col_end = min(idx + n, width - 1)` (Clip to not overwrite the last column border)
    e.  If the calculated drawing area has valid dimensions (`row_start < row_end` and `col_start < col_end`), fill this rectangular area `output_grid[row_start : row_end, col_start : col_end]` with the color C. Note that this might not be a perfect square if clipped by the boundaries.
5.  Re-copy the last row and the last column from the input grid to the output grid. This ensures that the border pixels retain their original input values, even if the drawing process in step 4 overwrote them.
6.  Return the modified output grid.
"""

def transform(input_grid):
    """
    Transforms the input grid by drawing shapes based on color blocks in the last row,
    preserving the last row and column as borders.

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
    
    # --- Step 2: Copy initial borders ---
    # Copy the last row and last column from input to output
    if height > 0:
        output_grid[height - 1, :] = input_np[height - 1, :]
    if width > 0:
        output_grid[:, width - 1] = input_np[:, width - 1]
        
    # Handle edge case of 1x1 grid - already copied
    if height <= 1 or width <= 1:
        return output_grid.tolist()

    # --- Step 3 & 4: Analyze last row and draw shapes ---
    last_row = input_np[height - 1, :]
    
    current_color = None
    start_index = -1
    segment_length = 0
    
    # Iterate through the last row to find contiguous blocks
    # Iterate up to width-1 because the last pixel is part of the vertical border
    for col in range(width -1): # Exclude the last column pixel
        color = last_row[col]
        
        # Check if the current segment ends
        if color == 0 or color != current_color:
            # If a non-background segment just ended, process it
            if current_color is not None and current_color != 0:
                # --- Step 4d: Determine drawing area ---
                row_start = start_index
                row_end = min(start_index + segment_length, height - 1)
                col_start = start_index
                col_end = min(start_index + segment_length, width - 1)

                # --- Step 4e: Draw the shape if area is valid ---
                if row_start < row_end and col_start < col_end:
                    output_grid[row_start : row_end, col_start : col_end] = current_color

            # Reset or start a new segment
            if color != 0:
                current_color = color
                start_index = col
                segment_length = 1
            else: # color is 0 (background)
                current_color = None
                start_index = -1
                segment_length = 0
        # Continue the current segment
        elif color == current_color:
            segment_length += 1

    # After the loop, check if the last segment needs to be processed
    if current_color is not None and current_color != 0:
        # --- Step 4d: Determine drawing area ---
        row_start = start_index
        row_end = min(start_index + segment_length, height - 1)
        col_start = start_index
        col_end = min(start_index + segment_length, width - 1)

        # --- Step 4e: Draw the shape if area is valid ---
        if row_start < row_end and col_start < col_end:
             output_grid[row_start : row_end, col_start : col_end] = current_color

    # --- Step 5: Re-copy borders to ensure they are preserved ---
    if height > 0:
        output_grid[height - 1, :] = input_np[height - 1, :]
    if width > 0:
        output_grid[:, width - 1] = input_np[:, width - 1]
            
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```