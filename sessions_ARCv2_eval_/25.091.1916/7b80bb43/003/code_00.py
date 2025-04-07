import numpy as np
from collections import Counter

def find_colors(grid):
    """Finds the background and foreground colors in the grid."""
    flat_grid = grid.flatten()
    counts = Counter(flat_grid)
    # Assume the most frequent color is background, the other is foreground
    if len(counts) == 1:
        # Handle edge case of a grid with only one color
        return list(counts.keys())[0], None 
    
    # Find the color with the highest count (background)
    background_color = counts.most_common(1)[0][0]
    
    # Find the other color (foreground)
    foreground_color = None
    for color in counts:
        if color != background_color:
            foreground_color = color
            break
            
    return background_color, foreground_color

def transform(input_grid):
    """
    Transforms the input grid by filling horizontal gaps of exactly three background 
    pixels that are bounded by foreground pixels on the same row.

    The transformation identifies the background and foreground colors. Then, for each row,
    it looks for patterns like F B B B F (where F is foreground, B is background). 
    If such a pattern is found, the three background pixels (B B B) are changed to 
    the foreground color (F F F). All other pixels remain unchanged.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Create a copy to modify, which will become the output grid
    output_np = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape

    # Determine the background and foreground colors
    background_color, foreground_color = find_colors(input_np)

    # If there's no foreground color (e.g., grid is uniform), return the copy directly
    if foreground_color is None:
        return output_np.tolist()

    # Iterate through each row of the grid
    for r in range(height):
        # Iterate through possible starting positions of a 5-pixel pattern (F B B B F)
        # We need to check indices c, c+1, c+2, c+3, c+4, so c can go up to width - 5
        for c in range(width - 4):
            # Check if the pattern F B B B F exists at this position
            is_pattern_start = input_np[r, c] == foreground_color
            is_gap_pixel1 = input_np[r, c + 1] == background_color
            is_gap_pixel2 = input_np[r, c + 2] == background_color
            is_gap_pixel3 = input_np[r, c + 3] == background_color
            is_pattern_end = input_np[r, c + 4] == foreground_color

            # If all conditions match the F B B B F pattern
            if is_pattern_start and is_gap_pixel1 and is_gap_pixel2 and is_gap_pixel3 and is_pattern_end:
                # Fill the 3-pixel gap in the output grid with the foreground color
                output_np[r, c + 1] = foreground_color
                output_np[r, c + 2] = foreground_color
                output_np[r, c + 3] = foreground_color

    # Convert the modified numpy array back to a list of lists
    return output_np.tolist()