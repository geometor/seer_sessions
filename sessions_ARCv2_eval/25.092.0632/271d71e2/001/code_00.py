import numpy as np
from scipy.ndimage import label

"""
Transformation Rule:

The primary transformation identifies connected components of gray pixels (color 5) using 8-way connectivity (including diagonals). 
For each distinct gray component found in the input grid:
1. Check all pixels that are orthogonally or diagonally adjacent to any pixel within that gray component.
2. If any of these adjacent pixels in the input grid has the color orange (7), then all pixels belonging to that specific gray component are changed to orange (7) in the output grid.
3. If a gray component has no adjacent orange pixels, it remains unchanged in the output grid.
4. All other pixels (background, white borders, pixels of other colors not involved in this interaction) retain their original color from the input grid.

Note: This rule addresses the consistent gray-to-orange conversion observed. Some examples contain additional changes (e.g., near borders or involving other colors) that are not covered by this primary rule and might represent noise or a secondary, less clear transformation. This implementation focuses on the dominant gray/orange interaction.
"""

def transform(input_grid):
    """
    Applies the gray-to-orange transformation based on adjacency.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    H, W = input_grid.shape

    # Define 8-way connectivity structure
    structure = np.array([[1, 1, 1],
                          [1, 1, 1],
                          [1, 1, 1]], dtype=bool)

    # Create a mask for gray pixels (color 5)
    gray_mask = (input_grid == 5)

    # Label connected components of gray pixels
    labeled_array, num_features = label(gray_mask, structure=structure)

    # Iterate through each found gray component
    for i in range(num_features):
        label_id = i + 1  # Labels start from 1
        
        # Create a mask for the current component
        component_mask = (labeled_array == label_id)
        
        # Get the coordinates of pixels in the current component
        component_coords = np.argwhere(component_mask) # list of [r, c]

        # Check if any pixel in this component is adjacent to an orange pixel (color 7)
        is_adjacent_to_orange = False
        for r, c in component_coords:
            # Check 8 neighbours
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    # Skip the center pixel itself
                    if dr == 0 and dc == 0:
                        continue
                    
                    # Calculate neighbour coordinates
                    nr, nc = r + dr, c + dc
                    
                    # Check if neighbour is within grid bounds
                    if 0 <= nr < H and 0 <= nc < W:
                        # Check if the neighbour is orange
                        if input_grid[nr, nc] == 7:
                            is_adjacent_to_orange = True
                            break # Found adjacent orange, no need to check more neighbours for this component pixel (r, c)
            
            if is_adjacent_to_orange:
                break # Found adjacent orange, no need to check other pixels in this component

        # If the component was adjacent to orange, change all its pixels to orange in the output grid
        if is_adjacent_to_orange:
            output_grid[component_mask] = 7

    return output_grid