"""
Processes each row of the input grid independently.
If a row contains exactly two non-white pixels, P1 (left, color C1, col1) and P2 (right, color C2, col2),
and the pair of colors (C1, C2) is one of {(1, 8), (8, 1), (4, 7), (7, 4)} (blue/azure or yellow/orange pairs),
then the right pixel P2 moves immediately to the right of the left pixel P1.
Specifically, the pixel at (row, col2) becomes white (0), and the pixel at (row, col1 + 1) becomes color C2.
Rows that do not meet these criteria remain unchanged.
"""

import numpy as np

def find_non_white_pixels(row):
    """Finds the indices and colors of non-white pixels in a row."""
    pixels = []
    for col_idx, color in enumerate(row):
        if color != 0:
            pixels.append({'col': col_idx, 'color': color})
    # Ensure pixels are sorted by column index (they should be already, but good practice)
    pixels.sort(key=lambda p: p['col'])
    return pixels

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Moves the right pixel leftward next to the left pixel if they form an active color pair
    in a row with exactly two non-white pixels.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    num_rows, num_cols = input_np.shape

    # Define the active color pairs
    active_pairs = {(1, 8), (8, 1), (4, 7), (7, 4)} # (blue, azure), (azure, blue), (yellow, orange), (orange, yellow)

    # Iterate through each row
    for r in range(num_rows):
        row_data = output_grid[r, :]
        
        # Find non-white pixels in the current row
        non_white_pixels = find_non_white_pixels(row_data)
        
        # Check if there are exactly two non-white pixels
        if len(non_white_pixels) == 2:
            # Get the properties of the two pixels
            p1 = non_white_pixels[0] # Left pixel
            p2 = non_white_pixels[1] # Right pixel
            
            color1 = p1['color']
            col1 = p1['col']
            color2 = p2['color']
            col2 = p2['col']
            
            # Check if the color pair is one of the active pairs
            if (color1, color2) in active_pairs:
                # Apply the transformation: move the right pixel next to the left one
                # Ensure the target position is within bounds (should be, as col1 < col2)
                if col1 + 1 < num_cols:
                    output_grid[r, col2] = 0      # Make original position of right pixel white
                    output_grid[r, col1 + 1] = color2 # Move right pixel's color next to left pixel
                    
    # Convert back to list of lists if necessary, depending on expected output format
    return output_grid.tolist()
