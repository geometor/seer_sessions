import numpy as np

"""
Transforms the input grid by identifying solid blue (1) rectangular shapes
and recoloring the pixels inside based on their minimum distance 'd' to the
nearest edge (a non-blue pixel or grid boundary).
- Pixels with distance d=0 (on the edge) remain blue (1).
- Pixels with distance d=1 (one step inside) become red (2).
- Pixels with distance d>=2 become green (3) if d is even, and red (2) if d is odd.
- Non-blue pixels (e.g., white 0) remain unchanged.
"""

def calculate_min_distance(grid, r, c):
    """
    Calculates the minimum distance from a blue pixel (r, c) to the nearest
    non-blue pixel or grid boundary. This corresponds to the number of steps
    inside the blue rectangle from the edge.

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.

    Returns:
        int: The minimum distance 'd'. Returns -1 if grid[r, c] is not blue.
    """
    height, width = grid.shape
    
    # Check if the current pixel is blue; this function assumes it is.
    if grid[r, c] != 1:
        # This case shouldn't be reached if called correctly from transform()
        return -1 

    # Calculate distance to the top edge
    # Scan upwards from the row above (r-1) down to the grid boundary (-1)
    dist_top = 0
    for i in range(r - 1, -2, -1): 
        if i < 0 or grid[i, c] != 1: # Hit boundary or non-blue pixel
            # Distance is the number of blue pixels strictly above (r,c)
            # which is r - (i + 1) 
            dist_top = r - (i + 1) 
            break

    # Calculate distance to the bottom edge
    # Scan downwards from the row below (r+1) up to the grid boundary (height)
    dist_bottom = 0
    for i in range(r + 1, height + 1): 
        if i >= height or grid[i, c] != 1: # Hit boundary or non-blue pixel
            # Distance is the number of blue pixels strictly below (r,c)
            # which is (i - 1) - r
            dist_bottom = (i - 1) - r 
            break

    # Calculate distance to the left edge
    # Scan leftwards from the column left (c-1) down to the grid boundary (-1)
    dist_left = 0
    for j in range(c - 1, -2, -1): 
        if j < 0 or grid[r, j] != 1: # Hit boundary or non-blue pixel
            # Distance is the number of blue pixels strictly left of (r,c)
            # which is c - (j + 1)
            dist_left = c - (j + 1) 
            break

    # Calculate distance to the right edge
    # Scan rightwards from the column right (c+1) up to the grid boundary (width)
    dist_right = 0
    for j in range(c + 1, width + 1): 
        if j >= width or grid[r, j] != 1: # Hit boundary or non-blue pixel
            # Distance is the number of blue pixels strictly right of (r,c)
            # which is (j - 1) - c
            dist_right = (j - 1) - c 
            break
            
    # The distance 'd' is the minimum steps *inside* the rectangle from any edge
    return min(dist_top, dist_bottom, dist_left, dist_right)


def transform(input_grid):
    """
    Applies the distance-based coloring transformation to blue rectangles.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Only process pixels that are blue (1) in the original input grid
            if input_np[r, c] == 1:
                # Calculate the minimum distance 'd' from this pixel to the 
                # nearest non-blue pixel or grid boundary.
                min_dist = calculate_min_distance(input_np, r, c)

                # Apply the coloring rules based on the calculated distance 'd'
                if min_dist == 0:
                    # Pixels on the edge (d=0) remain blue (1)
                    output_grid[r, c] = 1  
                elif min_dist == 1:
                    # Pixels 1 step inside (d=1) become red (2)
                    output_grid[r, c] = 2  
                else: # min_dist >= 2
                    # For pixels 2 or more steps inside:
                    if min_dist % 2 == 0: # Even distance (d=2, 4, ...)
                        output_grid[r, c] = 3 # Becomes green (3)
                    else: # Odd distance (d=3, 5, ...)
                        output_grid[r, c] = 2 # Becomes red (2)
            # Else (if the input pixel was not blue), the output pixel 
            # retains its original color (already copied)

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()