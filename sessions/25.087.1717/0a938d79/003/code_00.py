import numpy as np

"""
Generates a repeating line pattern (horizontal or vertical) based on the 
location and color of two initial non-white pixels.

1. Find the coordinates and colors of the two non-white pixels.
2. Determine the primary axis ('row' or 'col') for the pattern based 
   on the relative row and column distances between the two pixels.
   - If column difference is 0, axis is 'row'.
   - Else if row difference is 0, axis is 'col'.
   - Else if column difference >= row difference, axis is 'row'.
   - Otherwise, axis is 'col'.
3. Sort the pixels based on their index along the chosen axis (smaller index first). 
   Let the first pixel be P1 (color C1, index idx1) and the second be P2 (color C2, index idx2).
4. Calculate the pattern cycle length L = (idx2 - idx1) * 2. Handle the edge case L=0 by setting L=1 (though not expected based on examples where idx1 != idx2).
5. Create an output grid of the same dimensions as the input, filled with white (0).
6. Fill the output grid based on the axis and pattern:
   - Iterate through indices 'i' from the starting index of P1 (idx1) up to the grid boundary along the determined axis. If (i - idx1) is divisible by L, fill the corresponding row/column 'i' with color C1.
   - Iterate through indices 'i' from the starting index of P2 (idx2) up to the grid boundary along the determined axis. If (i - idx2) is divisible by L, fill the corresponding row/column 'i' with color C2.
7. Return the resulting grid.
"""

def find_non_white_pixels(grid):
    """Finds coordinates and colors of non-white pixels."""
    pixels = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                pixels.append({'row': r, 'col': c, 'color': grid[r, c]})
    # Expecting exactly two pixels based on examples
    if len(pixels) != 2:
        # This case might need specific handling if inputs can vary
        # For now, assume exactly two as per the training data pattern
        print(f"Warning/Error: Expected 2 non-white pixels, found {len(pixels)}")
        pass # Let the main function handle the list length
    return pixels


def transform(input_grid):
    """
    Transforms the input grid by creating a repeating line pattern based on two pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # 1. Find the two non-white pixels
    pixels = find_non_white_pixels(input_np)
    
    # Initialize output grid with white (0) - return if pixel condition not met
    output_grid = np.zeros_like(input_np)
    if len(pixels) != 2:
         print("Error: Did not find exactly two non-white pixels. Returning empty grid.")
         return output_grid.tolist() # Return empty grid

    p_a = pixels[0]
    p_b = pixels[1]

    # 2. Calculate differences and determine axis
    row_diff = abs(p_a['row'] - p_b['row'])
    col_diff = abs(p_a['col'] - p_b['col'])

    axis = None
    # Special case: points are in the same column
    if col_diff == 0:
         axis = 'row'
    # Special case: points are in the same row
    elif row_diff == 0:
         axis = 'col'
    # General case: compare row and column differences
    elif col_diff >= row_diff:
        axis = 'row'
    else: # col_diff < row_diff
        axis = 'col'

    # 3. Sort pixels based on the determined axis index
    if axis == 'row':
        key = 'row'
    else: # axis == 'col'
        key = 'col'
        
    if p_a[key] <= p_b[key]:
        p1 = p_a
        p2 = p_b
    else:
        p1 = p_b
        p2 = p_a
        
    idx1 = p1[key]
    idx2 = p2[key]
    color1 = p1['color']
    color2 = p2['color']

    # 4. Calculate pattern cycle length
    # L is double the distance between the indices along the axis.
    cycle_len = (idx2 - idx1) * 2
    
    # Handle edge case where pixels might have the same index (L=0)
    # This shouldn't happen if pixels are distinct, but as a safeguard:
    if cycle_len <= 0: 
        # If indices are the same, L becomes 0. What should happen?
        # Maybe fill only the line at idx1 with both colors? Or just color1?
        # Let's assume this means the pattern doesn't repeat, just draw the initial lines.
        # Set L=1 to prevent division by zero, but this might not be the correct logic for L=0.
        # Revisit if examples show this case. For now, printing a warning.
        print(f"Warning: Cycle length calculated as {cycle_len}. Setting to 1. Check logic if this occurs.")
        cycle_len = 1 # Avoid division by zero, allows initial lines to be drawn.

    # 5. Initialize output grid (done earlier)

    # 6. Fill the output grid based on the axis and pattern
    if axis == 'row':
        # Fill for color1
        for r in range(idx1, height):
            # Check if the current row index 'r' is a multiple of L steps away from idx1
            if (r - idx1) % cycle_len == 0:
                output_grid[r, :] = color1
        # Fill for color2
        for r in range(idx2, height):
            # Check if the current row index 'r' is a multiple of L steps away from idx2
            if (r - idx2) % cycle_len == 0:
                output_grid[r, :] = color2
    else: # axis == 'col'
        # Fill for color1
        for c in range(idx1, width):
             # Check if the current col index 'c' is a multiple of L steps away from idx1
            if (c - idx1) % cycle_len == 0:
                output_grid[:, c] = color1
        # Fill for color2
        for c in range(idx2, width):
             # Check if the current col index 'c' is a multiple of L steps away from idx2
            if (c - idx2) % cycle_len == 0:
                output_grid[:, c] = color2

    # 7. Convert back to list of lists for the ARC standard format
    return output_grid.tolist()