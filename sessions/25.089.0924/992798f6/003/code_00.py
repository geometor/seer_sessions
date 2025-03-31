import numpy as np

def find_pixel_coords(grid, color_value):
    """
    Finds the coordinates (row, col) of the first pixel with the given color value.
    
    Args:
        grid (np.array): The input grid.
        color_value (int): The color value to search for.
        
    Returns:
        tuple: (row, col) coordinates or None if not found.
    """
    coords = np.argwhere(grid == color_value)
    if len(coords) > 0:
        # Return the coordinates of the first occurrence
        return tuple(coords[0])
    return None

def get_line_coords_rc(r0, c0, r1, c1):
    """
    Calculates the coordinates of pixels on the line segment between (r0, c0) 
    and (r1, c1) using a Bresenham-like algorithm.
    This version aims to replicate standard integer-based line drawing.
    
    Args:
        r0, c0 (int): Starting row and column.
        r1, c1 (int): Ending row and column.
        
    Returns:
        list: A list of (row, col) tuples representing the pixels on the line,
              including the start and end points.
    """
    points = []
    dr = abs(r1 - r0)
    dc = abs(c1 - c0)
    sr = 1 if r0 < r1 else -1 # Step direction for row
    sc = 1 if c0 < c1 else -1 # Step direction for column
    
    # Initialize error term based on differences (one common Bresenham variant)
    err = dr - dc 

    r, c = r0, c0
    while True:
        points.append((r, c)) # Add current point to the list
        if r == r1 and c == c1:
            # Stop if we have reached the end point
            break
            
        e2 = 2 * err # Store error*2 for comparison
        
        # Check conditions for moving row-wise (vertical step)
        # This condition checks if moving vertically is preferred or necessary
        if e2 >= -dc: 
            if r == r1: break # Safety check: don't overshoot target row
            err -= dc # Adjust error by -delta_col
            r += sr   # Move vertically
            
        # Check conditions for moving column-wise (horizontal step)
        # This condition checks if moving horizontally is preferred or necessary
        if e2 <= dr: 
            if c == c1: break # Safety check: don't overshoot target column
            err += dr  # Adjust error by delta_row
            c += sc   # Move horizontally
            
    return points


def transform(input_grid):
    """
    Identifies a blue (1) and a red (2) pixel in the input grid.
    Draws a green (3) line connecting these two pixels on the output grid.
    The line consists of pixels determined by a Bresenham-like algorithm.
    The start (blue) and end (red) pixels themselves are not colored green.
    
    Args:
        input_grid (list of lists): The input grid represented as a 2D list.
        
    Returns:
        list of lists: The transformed grid with the green line added.
    """
    # Convert input list of lists to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # Create a copy of the input grid to modify as the output
    output_grid = np.copy(input_np)

    # Find the coordinates of the blue (1 - start) and red (2 - end) pixels
    start_coords = find_pixel_coords(input_np, 1)
    end_coords = find_pixel_coords(input_np, 2)

    # Proceed only if both start and end points are found
    if start_coords is not None and end_coords is not None:
        r0, c0 = start_coords
        r1, c1 = end_coords

        # Calculate all coordinates for the line connecting the start and end points
        line_coords = get_line_coords_rc(r0, c0, r1, c1)

        # Color the path pixels green (3)
        # Iterate through all calculated coordinates on the line
        for r, c in line_coords:
            # Only color the pixel if it is NOT the start point AND NOT the end point
            if (r, c) != start_coords and (r, c) != end_coords:
                # Check grid bounds as a safety measure, although line algo should stay within
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                     output_grid[r, c] = 3 # Set color to green

    # Convert the final numpy array back to a list of lists for the required output format
    return output_grid.tolist()