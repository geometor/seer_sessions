import numpy as np
from collections import defaultdict

"""
Identifies pairs of identically colored pixels (excluding white '0' and azure '8') in the input grid. 
Each pair defines the opposite corners of a rectangle. 
Within this rectangle (inclusive of the boundaries defined by the pair), all white ('0') and azure ('8') pixels 
are changed to the color of the pair that defined the rectangle. 
This process is repeated for all unique trigger colors found in the input.
"""

def find_trigger_pixels(grid):
    """
    Finds pixels that are not white (0) or azure (8) and groups them by color.
    Args:
        grid (np.array): The input grid.
    Returns:
        dict: A dictionary where keys are colors (int > 0 and != 8) and 
              values are lists of (row, col) coordinates for that color.
    """
    triggers = defaultdict(list)
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Trigger colors are non-white (0) and non-azure (8)
            if color != 0 and color != 8:
                triggers[color].append((r, c))
    # Filter out colors that don't appear exactly twice (though the prompt implies they always do)
    # For robustness, we could keep only pairs, but based on examples, let's assume pairs.
    # valid_triggers = {color: coords for color, coords in triggers.items() if len(coords) == 2}
    # return valid_triggers
    # Assuming exactly two points per color based on examples
    return triggers


def transform(input_grid):
    """
    Transforms the input grid based on trigger pixel pairs.
    
    1. Finds pairs of same-colored trigger pixels (not white 0 or azure 8).
    2. For each pair, defines an inclusive bounding rectangle.
    3. Within the rectangle, changes all white (0) and azure (8) pixels to the trigger color.
    
    Args:
        input_grid (np.array): The input grid as a NumPy array.
        
    Returns:
        np.array: The transformed output grid.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Find all trigger pixels and group them by color
    trigger_locations_by_color = find_trigger_pixels(input_grid)
    
    # Process each trigger color
    for color, locations in trigger_locations_by_color.items():
        # Expecting exactly two locations per color based on examples
        if len(locations) == 2:
            (r1, c1), (r2, c2) = locations
            
            # Determine the bounding box coordinates (inclusive)
            min_row = min(r1, r2)
            max_row = max(r1, r2)
            min_col = min(c1, c2)
            max_col = max(c1, c2)
            
            # Iterate through the bounding box
            for r in range(min_row, max_row + 1):
                for c in range(min_col, max_col + 1):
                    # Check if the pixel in the *input* grid within the box is white (0) or azure (8)
                    # Note: We check the original input_grid state to avoid interference between overlapping boxes if any
                    # (though examples don't show overlaps being an issue). Using output_grid would also work here
                    # as the trigger colors themselves are not 0 or 8.
                    if output_grid[r, c] == 0 or output_grid[r, c] == 8:
                        # Change the corresponding pixel in the output grid to the trigger color
                        output_grid[r, c] = color
                        
    return output_grid