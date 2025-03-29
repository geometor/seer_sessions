import numpy as np
from typing import List, Tuple

"""
Transforms the input grid based on the counts and locations of single green and single yellow pixels, with an additional rule for specific counts involving single red and adjacent orange pixels.

1. Find all single green (3) pixels (pixels with no green neighbors, 8-way adjacency) and their count (N_green).
2. Find all single yellow (4) pixels (pixels with no yellow neighbors, 8-way adjacency) and their count (N_yellow).
3. Conditional Transformation:
   - IF N_green == 2 AND N_yellow == 6:
     - Identify the top-leftmost single yellow pixel (minimum row, then minimum column).
     - Change all *other* single yellow pixels to white (0).
   - ELSE IF N_green == 6 AND N_yellow == 7:
     - Sort the locations of all single green pixels (by row, then column).
     - Identify the *second* pixel in the sorted list.
     - Change all *other* single green pixels to white (0).
   - ELSE IF N_green == 1 AND N_yellow == 2:
     - Find all single red (2) pixels (using the same "single" definition).
     - Find all orange (7) pixels that are adjacent (8-way) to at least one other orange pixel.
     - Change all identified single red pixels and all identified adjacent orange pixels to white (0).
   - ELSE:
     - Return the input grid unchanged.
"""

def find_single_pixels(grid_np: np.ndarray, target_color: int) -> List[Tuple[int, int]]:
    """
    Finds all pixels of a target_color that have no neighbors of the same color (8-way adjacency).

    Args:
        grid_np (np.ndarray): The input grid as a numpy array.
        target_color (int): The color to search for.

    Returns:
        List[Tuple[int, int]]: A list of (row, col) tuples representing the locations of single pixels.
    """
    rows, cols = grid_np.shape
    single_pixel_locations = []
    for r in range(rows):
        for c in range(cols):
            if grid_np[r, c] == target_color:
                is_single = True
                # Check 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue # Skip self
                        nr, nc = r + dr, c + dc
                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # If a neighbor has the same color, it's not single
                            if grid_np[nr, nc] == target_color:
                                is_single = False
                                break
                    if not is_single:
                        break # Stop checking neighbors for this pixel
                
                # If after checking all neighbors, it's still considered single
                if is_single:
                    single_pixel_locations.append((r, c))
                    
    return single_pixel_locations

def find_adjacent_pixels(grid_np: np.ndarray, target_color: int) -> List[Tuple[int, int]]:
    """
    Finds all pixels of a target_color that have at least one neighbor of the same color (8-way adjacency).

    Args:
        grid_np (np.ndarray): The input grid as a numpy array.
        target_color (int): The color to search for.

    Returns:
        List[Tuple[int, int]]: A list of (row, col) tuples representing the locations of pixels 
                                that are part of an adjacent group of the target color.
    """
    rows, cols = grid_np.shape
    adjacent_pixel_locations = set() # Use set to store unique locations
    
    for r in range(rows):
        for c in range(cols):
            if grid_np[r, c] == target_color:
                has_same_color_neighbor = False
                # Check 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue # Skip self
                        nr, nc = r + dr, c + dc
                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # If a neighbor has the same color, mark it
                            if grid_np[nr, nc] == target_color:
                                has_same_color_neighbor = True
                                break # Found one neighbor, no need to check others for this pixel
                    if has_same_color_neighbor:
                        adjacent_pixel_locations.add((r, c)) # Add this pixel if it has a neighbor
                        
    return list(adjacent_pixel_locations)


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rules based on counts of single green/yellow pixels,
    or single red/adjacent orange pixels for a specific count case.

    Args:
        input_grid (List[List[int]]): The input grid.

    Returns:
        List[List[int]]: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Create the output grid as a copy initially
    output_grid_np = np.copy(input_grid_np)
    
    # Define target colors and replacement color
    green_color = 3
    yellow_color = 4
    red_color = 2
    orange_color = 7
    replacement_color = 0 # White

    # 1. Find single green pixels and count them
    single_green_locations = find_single_pixels(input_grid_np, green_color)
    n_green = len(single_green_locations)

    # 2. Find single yellow pixels and count them
    single_yellow_locations = find_single_pixels(input_grid_np, yellow_color)
    n_yellow = len(single_yellow_locations)

    # 3. Apply Conditional Logic based on counts
    
    # Rule A: N_green == 2 AND N_yellow == 6
    if n_green == 2 and n_yellow == 6:
        # Sort yellow locations to find the top-leftmost
        single_yellow_locations.sort(key=lambda x: (x[0], x[1]))
        if single_yellow_locations: # Ensure list is not empty
            pixel_to_preserve = single_yellow_locations[0] # Top-leftmost is the first element

            # Change all *other* single yellow pixels to white
            for r, c in single_yellow_locations:
                if (r, c) != pixel_to_preserve:
                    output_grid_np[r, c] = replacement_color
        # If list is empty (shouldn't happen if n_yellow==6), grid remains unchanged (copy of input)

    # Rule B: N_green == 6 AND N_yellow == 7
    elif n_green == 6 and n_yellow == 7:
        # Sort green locations to find the second top-leftmost
        single_green_locations.sort(key=lambda x: (x[0], x[1]))
        # Check if there are at least two elements before accessing index 1
        if len(single_green_locations) > 1:
             pixel_to_preserve = single_green_locations[1] # Second element in sorted list

             # Change all *other* single green pixels to white
             for r, c in single_green_locations:
                 if (r, c) != pixel_to_preserve:
                     output_grid_np[r, c] = replacement_color
        # If less than 2 elements (shouldn't happen if n_green==6), grid remains unchanged

    # Rule C: N_green == 1 AND N_yellow == 2
    elif n_green == 1 and n_yellow == 2:
         # Find single red pixels
         single_red_locations = find_single_pixels(input_grid_np, red_color)
         # Find orange pixels that are adjacent to other orange pixels
         adjacent_orange_locations = find_adjacent_pixels(input_grid_np, orange_color)

         # Change all identified single red pixels to white
         for r, c in single_red_locations:
              output_grid_np[r, c] = replacement_color
              
         # Change all identified adjacent orange pixels to white
         for r, c in adjacent_orange_locations:
              output_grid_np[r, c] = replacement_color

    # Default Rule: Otherwise (no counts match the specific rules)
    # The output grid remains the initial copy of the input grid.
    
    # Convert the result back to a list of lists and return
    return output_grid_np.tolist()
