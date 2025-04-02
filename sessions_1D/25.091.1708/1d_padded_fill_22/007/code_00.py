import numpy as np
from typing import List, Dict
from collections import defaultdict

"""
Transforms an input grid by identifying pairs of same-colored non-white pixels 
within each row and filling the horizontal space strictly between them with 
that color.

1.  Initialize the `output_grid` as an identical copy of the `input_grid`.
2.  For each `row` in the `input_grid` (indexed from top to bottom):
    a.  Create a temporary map to store the column locations of non-white pixels found in this `row`, keyed by their `color`.
    b.  Scan across the current `row` (indexed by `col` from left to right):
        i.  If the pixel at (`row`, `col`) is not white (color 0), record its `col` in the map under its `color`.
    c.  After scanning the entire `row`, examine the map:
        i.  For each `color` entry in the map:
            *   If the list of column locations for this `color` contains exactly two columns, let them be `col_A` and `col_B`.
            *   Find the leftmost column: `left_col = min(col_A, col_B)`.
            *   Find the rightmost column: `right_col = max(col_A, col_B)`.
            *   Fill the gap in the `output_grid`: For every column `c_fill` starting from `left_col + 1` up to (but not including) `right_col`, set the pixel in the `output_grid` at (`row`, `c_fill`) to this `color`.
3.  After processing all rows, return the `output_grid`.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Identifies pairs of same-colored non-white pixels in each row and fills 
    the horizontal space between them with that color.
    
    Args:
        input_grid: A list of lists representing the input grid.
        
    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation and copying
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Initialize the output_grid as an identical copy of the input_grid.
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # 2. For each row in the input_grid:
    for r in range(height):
        # a. Create a temporary map to store column locations of non-white pixels.
        #    Using defaultdict simplifies adding to lists.
        color_locations: Dict[int, List[int]] = defaultdict(list)

        # b. Scan across the current row:
        for c in range(width):
            pixel_color = input_array[r, c]
            # i. If the pixel is not white, record its column index.
            if pixel_color != 0:  
                color_locations[pixel_color].append(c)

        # c. After scanning the row, examine the map:
        # i. For each color found in the row:
        for color, locations in color_locations.items():
            # Check if exactly two pixels of this color exist.
            if len(locations) == 2:
                # If yes, get the two column indices.
                col_A, col_B = locations[0], locations[1]
                
                # Find the leftmost and rightmost column indices.
                left_col = min(col_A, col_B)
                right_col = max(col_A, col_B)
                
                # Fill the gap in the output_grid.
                # Iterate from the column *after* the left pixel up to 
                # (but not including) the column of the right pixel.
                for c_fill in range(left_col + 1, right_col):
                    output_array[r, c_fill] = color

    # 3. After processing all rows, convert numpy array back to list of lists.
    output_grid = output_array.tolist()
    return output_grid