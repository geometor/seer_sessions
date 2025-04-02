```python
import numpy as np

def find_non_white_pixels(row):
    """
    Finds the color and indices of the two non-white pixels in a row.

    Args:
        row: A list representing a row of the grid.

    Returns:
        A tuple (color, index1, index2) or None if not exactly two non-white pixels are found.
    """
    non_white_pixels = []
    non_white_color = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            if non_white_color == -1:
                non_white_color = pixel
            elif pixel != non_white_color:
                # Found a second different non-white color, invalid input based on task description
                return None
            non_white_pixels.append(i)

    if len(non_white_pixels) == 2:
        return non_white_color, non_white_pixels[0], non_white_pixels[1]
    else:
        # Did not find exactly two non-white pixels
        return None

def transform(input_grid):
    """
    Identifies two pixels of the same non-white color in a single input row
    and fills the segment between them (exclusive of the endpoints) with that color.
    If there are not exactly two non-white pixels of the same color,
    returns the input grid unchanged.
    """
    # The input is expected to be a single row, represented as a list within a list
    input_row = input_grid[0]
    
    # Find the non-white color and the indices of the two pixels
    result = find_non_white_pixels(input_row)

    # If exactly two non-white pixels of the same color were found
    if result:
        fill_color, idx1, idx2 = result
        
        # Determine the start and end indices for filling
        min_idx = min(idx1, idx2)
        max_idx = max(idx1, idx2)
        
        # Create the output row, starting as a copy of the input row
        output_row = list(input_row) # Make a mutable copy
        
        # Fill the pixels between the two found indices
        # Iterate from the index after the minimum up to (but not including) the maximum
        for i in range(min_idx + 1, max_idx):
            output_row[i] = fill_color
            
        # Return the modified row wrapped in a list, matching the expected output format
        return [output_row]
    else:
        # If the input doesn't match the expected pattern (e.g., not exactly two non-white pixels),
        # return the original input grid.
        # Note: Based on the examples, this case might not occur, but it's safer to handle.
        return input_grid

```