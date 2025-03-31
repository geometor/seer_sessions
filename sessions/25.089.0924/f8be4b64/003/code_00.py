import numpy as np

"""
The transformation identifies "plus" shapes made of green pixels (3) in the input grid. 
A plus shape is defined by a central pixel having four green neighbors (North, South, East, West).
The color of this central pixel (the "core color") determines a fill operation on the grid.
These fill operations only affect pixels that were originally background (white, 0). 
Original non-background pixels are preserved.

Fill Operations based on Core Color:
- Azure (8): Fill the corresponding row with Azure.
- Magenta (6): Fill the corresponding column with Magenta.
- Gray (5): Fill the corresponding row AND column with Gray.
- Red (2): Fill the corresponding row AND column with Red.
- Yellow (4): Fill the corresponding row with Yellow.
- Other colors (e.g., 0): No operation.

Priority of Overlapping Fills:
If multiple fill operations target the same original background pixel, the color is determined by the operation with the highest priority, applied in this order:
1. Azure (8)
2. Magenta (6)
3. Gray (5)
4. Red (2)
5. Yellow (4)

Higher priority fills overwrite the effects of lower priority fills on background pixels.
"""

def find_plus_centers(grid):
    """
    Finds all pixels that are centers of a green plus shape.
    A center is a pixel (r, c) where grid[r-1, c], grid[r+1, c], 
    grid[r, c-1], and grid[r, c+1] are all green (3).
    
    Args:
        grid (np.array): Input grid.

    Returns:
        list: A list of tuples, where each tuple is ((row, col), core_color).
    """
    centers = []
    height, width = grid.shape
    # Iterate through possible center locations (avoiding edges)
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # Check orthogonal neighbors
            if (grid[r - 1, c] == 3 and
                grid[r + 1, c] == 3 and
                grid[r, c - 1] == 3 and
                grid[r, c + 1] == 3):
                core_color = grid[r, c]
                centers.append(((r, c), core_color))
    return centers

def transform(input_grid):
    """
    Transforms the input grid based on green plus shapes and their core colors,
    applying fill operations with priority rules.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy() # Start with a copy
    height, width = grid_np.shape

    # Find all green plus centers and their core colors
    plus_centers = find_plus_centers(grid_np)

    # Define priority order and associated fill types
    # Priority: 8 > 6 > 5 > 2 > 4
    # Fill Types: R=Row, C=Column, RC=Row/Column
    priority_map = {
        8: 'R', 
        6: 'C', 
        5: 'RC',
        2: 'RC',
        4: 'R'
    }
    priority_order = [8, 6, 5, 2, 4]

    # Apply fills based on priority order
    for core_color in priority_order:
        fill_type = priority_map.get(core_color)
        if not fill_type:
            continue # Skip colors without defined actions

        # Find centers with the current core color
        centers_for_color = [center for center in plus_centers if center[1] == core_color]

        for (r, c), color_val in centers_for_color:
            # Determine target cells based on fill type
            target_cells = []
            if 'R' in fill_type:
                for tc in range(width):
                    target_cells.append((r, tc))
            if 'C' in fill_type:
                for tr in range(height):
                     # Avoid adding the center pixel twice if RC
                    if (tr, c) not in target_cells:
                       target_cells.append((tr, c))
            
            # Apply fill to target cells if they were originally background
            for tr, tc in target_cells:
                 # Check bounds just in case, though target_cells should be within bounds
                 if 0 <= tr < height and 0 <= tc < width:
                    # Check if the original pixel was background (0)
                    if grid_np[tr, tc] == 0:
                        output_grid[tr, tc] = color_val # Apply the fill

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()