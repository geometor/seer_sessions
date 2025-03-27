```python
import numpy as np

"""
Iterate through each row of the input grid. For each row, identify contiguous 
horizontal segments of white (0) pixels. If a white segment is bounded immediately 
on its left and immediately on its right by non-white pixels (1-9) within the 
same row, change all the white pixels within that segment to blue (1). All other 
pixels retain their original color.
"""

def transform(input_grid):
    """
    Fills horizontal gaps of white pixels (0) with blue (1) if they are 
    bounded by non-white pixels on both sides within the same row.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed grid.
    """
    # Convert input to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Define color constants
    WHITE = 0
    BLUE = 1

    # Iterate through each row
    for r in range(height):
        c = 0
        while c < width:
            # Check if the current pixel is white
            if input_np[r, c] == WHITE:
                # Found the potential start of a white segment
                start_c = c
                # Find the end of the contiguous white segment
                end_c = start_c
                while end_c + 1 < width and input_np[r, end_c + 1] == WHITE:
                    end_c += 1
                
                # Check if the segment has neighbors within the row bounds
                has_left_neighbor = start_c > 0
                has_right_neighbor = end_c < width - 1

                if has_left_neighbor and has_right_neighbor:
                    # Get the colors of the neighbors
                    left_neighbor_color = input_np[r, start_c - 1]
                    right_neighbor_color = input_np[r, end_c + 1]

                    # Check if both neighbors are non-white
                    if left_neighbor_color != WHITE and right_neighbor_color != WHITE:
                        # Fill the segment in the output grid with blue
                        for fill_c in range(start_c, end_c + 1):
                            output_grid[r, fill_c] = BLUE
                
                # Move the column pointer past the processed segment
                c = end_c + 1
            else:
                # Move to the next column if the current pixel is not white
                c += 1

    return output_grid.tolist() # Return as list of lists to match ARC format
```