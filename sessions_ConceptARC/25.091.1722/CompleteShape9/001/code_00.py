import numpy as np
from collections import Counter

def find_main_color(grid):
    """
    Finds the most frequent non-background (non-zero) color in the grid.
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        int: The most frequent non-zero color, or 0 if only background exists.
    """
    # Flatten the grid to easily count colors
    colors = grid.flatten()
    
    # Count frequencies of non-zero colors
    color_counts = Counter(c for c in colors if c != 0)
    
    # If no non-zero colors are found, return 0 (background color)
    if not color_counts:
        return 0
        
    # Return the color with the highest frequency
    # most_common(1) returns a list like [(color, count)], so we access [0][0]
    main_color = color_counts.most_common(1)[0][0]
    return main_color

def transform(input_grid):
    """
    Identifies the single most frequent non-white color (C) in the input grid.
    Creates an output grid initially identical to the input.
    Iterates through each white pixel (0) in the input grid.
    If a white pixel has either:
    1. All four cardinal neighbors with color C, OR
    2. Exactly two opposite cardinal neighbors (North/South or East/West) with color C,
    then changes that pixel's color to C in the output grid.
    Returns the modified output grid.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Find the main color C based on frequency (ignoring background 0)
    main_color = find_main_color(input_grid_np)

    # If no main color is found (e.g., grid is all white), return the original grid
    if main_color == 0:
        # Convert back to list of lists format for consistency
        return input_grid_np.tolist()

    # Initialize the output grid as a copy of the input grid
    # Changes will be made to this copy
    output_grid = np.copy(input_grid_np)

    # Iterate through each pixel (cell) in the grid using row (r) and column (c) indices
    for r in range(height):
        for c in range(width):
            # We only consider modifying pixels that are currently white (0)
            if input_grid_np[r, c] == 0:
                
                # Check the color of the four cardinal neighbors
                # Use default None if neighbor is out of bounds
                north = input_grid_np[r-1, c] if r > 0 else None
                south = input_grid_np[r+1, c] if r < height - 1 else None
                west = input_grid_np[r, c-1] if c > 0 else None
                east = input_grid_np[r, c+1] if c < width - 1 else None
                
                # Check if neighbors match the main color
                north_is_main = (north == main_color)
                south_is_main = (south == main_color)
                west_is_main = (west == main_color)
                east_is_main = (east == main_color)
                
                # Count how many neighbors match the main color
                main_color_neighbor_count = sum([north_is_main, south_is_main, west_is_main, east_is_main])

                # Condition 1: The pixel is surrounded by the main color (all 4 neighbors)
                # This implicitly requires the pixel not to be on the border
                is_surrounded = (main_color_neighbor_count == 4) 
                                 # The count automatically handles border cases; if count is 4, it cannot be on border.

                # Condition 2: Exactly 2 neighbors match, and they are opposite pairs
                opposite_pair_match = (main_color_neighbor_count == 2 and 
                                       ((north_is_main and south_is_main) or \
                                        (west_is_main and east_is_main)))

                # If either condition is met, fill the white pixel with the main color
                if is_surrounded or opposite_pair_match:
                    output_grid[r, c] = main_color

    # Return the modified grid, converted back to list of lists format
    return output_grid.tolist()