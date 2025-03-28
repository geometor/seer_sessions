import numpy as np
from typing import List, Tuple

"""
Identifies different types of corners within non-white shapes based on the 
configuration of adjacent white (background) pixels and recolors them.

Rule 1: A non-white pixel is changed to red (2) if it has exactly two white 
        neighbors, and these neighbors are diagonally adjacent relative to the 
        pixel (e.g., North and East neighbors are white, or South and West are 
        white).
Rule 2: A non-white pixel is changed to yellow (4) if it has three or more 
        white neighbors.
Rule 3: Otherwise, the pixel retains its original color.
"""

def get_neighbors_info(grid: np.ndarray, r: int, c: int) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Gets the count and relative positions of white neighbors for a given pixel.

    Args:
        grid: The input grid (numpy array).
        r: Row index of the pixel.
        c: Column index of the pixel.

    Returns:
        A tuple containing:
        - white_neighbor_count: The number of white neighbors.
        - white_neighbor_coords: A list of relative coordinates (dr, dc) for 
                                 each white neighbor.
    """
    height, width = grid.shape
    white_neighbor_count = 0
    white_neighbor_coords = []
    
    # Define relative coordinates for 8 neighbors
    neighbor_deltas = [
        (-1, 0), (-1, 1), (0, 1), (1, 1), # N, NE, E, SE
        (1, 0), (1, -1), (0, -1), (-1, -1) # S, SW, W, NW
    ]

    for dr, dc in neighbor_deltas:
        nr, nc = r + dr, c + dc
        # Check if neighbor is within grid bounds
        if 0 <= nr < height and 0 <= nc < width:
            if grid[nr, nc] == 0: # Check if neighbor is white
                white_neighbor_count += 1
                white_neighbor_coords.append((dr, dc))
        else: # Treat out-of-bounds as white neighbors
            white_neighbor_count += 1
            white_neighbor_coords.append((dr, dc))
            
    return white_neighbor_count, white_neighbor_coords

def is_red_corner(white_neighbor_coords: List[Tuple[int, int]]) -> bool:
    """
    Checks if the white neighbors form a configuration for a red corner.
    
    Red corner configurations (relative coordinates):
    - N and E: (-1, 0) and (0, 1)
    - S and E: (1, 0) and (0, 1)
    - S and W: (1, 0) and (0, -1)
    - N and W: (-1, 0) and (0, -1)

    Args:
        white_neighbor_coords: List of relative coordinates of white neighbors.

    Returns:
        True if the configuration matches a red corner, False otherwise.
    """
    if len(white_neighbor_coords) != 2:
        return False
        
    # Convert list of tuples to set of tuples for easier comparison
    coord_set = set(white_neighbor_coords)

    red_configs = [
        {(-1, 0), (0, 1)}, # N, E
        {(1, 0), (0, 1)},  # S, E
        {(1, 0), (0, -1)}, # S, W
        {(-1, 0), (0, -1)}  # N, W
    ]

    for config in red_configs:
        if coord_set == config:
            return True
            
    return False

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by recoloring corner pixels based on neighbors.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output_grid as a copy of the input
    output_array = np.copy(input_array)

    # Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            # Skip white pixels
            if input_array[r, c] == 0:
                continue

            # Analyze non-white pixels
            original_color = input_array[r, c]
            
            # Get information about white neighbors
            white_neighbor_count, white_neighbor_coords = get_neighbors_info(input_array, r, c)

            # Apply coloring rules
            # Rule 1: Check for red corners (exactly 2 specific diagonal white neighbors)
            if white_neighbor_count == 2 and is_red_corner(white_neighbor_coords):
                output_array[r, c] = 2 # Red
            # Rule 2: Check for yellow corners (3 or more white neighbors)
            elif white_neighbor_count >= 3:
                output_array[r, c] = 4 # Yellow
            # Rule 3: Otherwise, keep the original color (already handled by copy)
            # else:
            #     output_array[r, c] = original_color 

    # Convert the output numpy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid