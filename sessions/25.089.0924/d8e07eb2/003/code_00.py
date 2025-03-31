import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identify all gray (8) pixels that are adjacent (including diagonals, 8-connectivity) 
       to any pixel that is neither gray (8) nor magenta (6) (these non-gray, non-magenta pixels are termed 'ShapePixels').
    2. Change these identified adjacent gray pixels to green (3).
    3. Keep track if any of the pixels changed to green in step 2 are located 
       within the top 5 rows (rows 0-4).
    4. If any changes occurred in the top 5 rows, change all pixels in the 
       bottom two rows (rows 28-29) to green (3).
    5. Otherwise (if no changes occurred in the top 5 rows), change all pixels 
       in the bottom two rows (rows 28-29) to red (2).
    6. All other pixels, including the original ShapePixels and magenta lines, 
       retain their original color unless modified by rule 2 or rules 4/5.
    """

    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Set to store coordinates (row, col) of gray pixels that need to be changed to green
    pixels_to_change = set()
    # Flag to track if any changes will occur in the top section (rows 0-4)
    top_section_changed = False

    # Iterate through each pixel of the input grid to find ShapePixels
    for r in range(height):
        for c in range(width):
            pixel_color = input_np[r, c]
            
            # Check if the current pixel is a ShapePixel (neither gray nor magenta)
            if pixel_color != 8 and pixel_color != 6:
                # If it's a ShapePixel, check its 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # Skip the center pixel itself
                        if dr == 0 and dc == 0:
                            continue
                        
                        # Calculate neighbor coordinates
                        nr, nc = r + dr, c + dc

                        # Check if the neighbor is within grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            neighbor_color = input_np[nr, nc]
                            # Check if the neighbor is gray (8)
                            if neighbor_color == 8:
                                # If it's a gray neighbor, mark it for change
                                coord = (nr, nc)
                                if coord not in pixels_to_change:
                                    pixels_to_change.add(coord)
                                    # Check if this gray pixel is in the top section (rows 0-4)
                                    # Set the flag if it is and hasn't been set yet
                                    if nr <= 4:
                                        top_section_changed = True

    # Apply the changes: turn marked gray pixels green
    for r, c in pixels_to_change:
        output_grid[r, c] = 3

    # Determine the color for the bottom two rows based on the flag
    bottom_color = 3 if top_section_changed else 2

    # Apply the color change to the bottom two rows
    # Assuming grid height is always 30 as per examples
    if height >= 30:
        # Rows 28 and 29 correspond to indices height-2 and height-1
        output_grid[height-2:height, :] = bottom_color

    # Return the final modified grid as a list of lists
    return output_grid.tolist()