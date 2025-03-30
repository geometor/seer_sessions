import numpy as np
from scipy.ndimage import label, generate_binary_structure

"""
Transforms the input grid by selectively changing the color of red (2) pixels within specific 5x5 blocks based on the block's position and internal pattern.

The grid is treated as a 3x2 layout of 5x5 blocks separated by white (0) borders.
The transformation rules are:
1. If a 5x5 block forms a 'frame' pattern (red border, white center), change red pixels to azure (8).
2. If the block is at position (1,1) (top-left block), has 1 connected red component, and is NOT a frame, change red to green (3).
3. If the block is at position (6,1) (middle-left block), has 1 connected red component, and is NOT a frame, change red to azure (8).
4. If the block is at position (6,6) (middle-right block), has 1 connected red component, and is NOT a frame, change red to green (3).
5. If the block is at position (6,6) (middle-right block) and has 3 connected red components, change red to azure (8).
6. If the block is at position (11,6) (bottom-right block) and has 3 connected red components, change red to green (3).
7. Otherwise, the block's red pixels remain unchanged.

Connected components are determined using 4-way adjacency.
"""

def _is_frame(subgrid):
    """Checks if a 5x5 subgrid is a 'frame' shape (red border, white center)."""
    if subgrid.shape != (5, 5):
        return False
    # Check outer border (should be red=2)
    if not np.all(subgrid[0, :] == 2): return False
    if not np.all(subgrid[4, :] == 2): return False
    if not np.all(subgrid[1:4, 0] == 2): return False
    if not np.all(subgrid[1:4, 4] == 2): return False
    # Check inner 3x3 (should be white=0)
    if not np.all(subgrid[1:4, 1:4] == 0): return False
    return True

def _count_connected_components(subgrid, target_color=2):
    """Counts the number of 4-way connected components of a specific color."""
    if subgrid.shape != (5, 5):
        return 0
    binary_grid = (subgrid == target_color)
    # Use 4-connectivity (connectivity=1 for scipy.ndimage.label)
    structure = generate_binary_structure(2, 1) 
    labeled_array, num_features = label(binary_grid, structure=structure)
    return num_features

def _recolor_block(grid, r, c, original_color, new_color):
    """Recolors pixels of original_color to new_color within a 5x5 block."""
    for i in range(r, r + 5):
        for j in range(c, c + 5):
            if grid[i, j] == original_color:
                grid[i, j] = new_color

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Define block top-left coordinates (0-based index)
    block_coords = [
        (1, 1), (1, 6),
        (6, 1), (6, 6),
        (11, 1), (11, 6)
    ]

    RED = 2
    GREEN = 3
    AZURE = 8

    # Process each block
    for r, c in block_coords:
        # Ensure block is within grid bounds (safety check)
        if r + 5 > rows or c + 5 > cols:
            continue 
            
        # Extract the 5x5 subgrid
        subgrid = output_grid[r:r+5, c:c+5]

        # Analyze the subgrid
        is_frame_shape = _is_frame(subgrid)
        component_count = _count_connected_components(subgrid, target_color=RED)
        
        new_color = None # Default: no change

        # Apply transformation rules
        if is_frame_shape:
            new_color = AZURE
        elif r == 1 and c == 1 and component_count == 1: # Position (1,1)
             new_color = GREEN
        elif r == 6 and c == 1 and component_count == 1: # Position (6,1)
             new_color = AZURE
        elif r == 6 and c == 6: # Position (6,6)
            if component_count == 1:
                 new_color = GREEN
            elif component_count == 3:
                 new_color = AZURE
        elif r == 11 and c == 6 and component_count == 3: # Position (11,6)
             new_color = GREEN

        # If a rule matched, recolor the block
        if new_color is not None:
            _recolor_block(output_grid, r, c, original_color=RED, new_color=new_color)

    return output_grid.tolist() # Return as list of lists as per ARC format