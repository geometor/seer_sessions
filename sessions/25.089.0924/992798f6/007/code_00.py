import numpy as np

"""
Transforms an input grid based on the following process:
1. Identifies the unique blue pixel (value 1) as the start point (r0, c0) and the unique red pixel (value 2) as the end point (r1, c1).
2. Calculates the sequence of grid coordinates forming a path between the start and end points. This uses a specific grid-based line-drawing algorithm that appears unique to ARC tasks, as standard algorithms like Bresenham or DDA do not perfectly replicate the paths seen in the training examples. The algorithm implemented here is a standard Bresenham variant, which is known to be *incorrect* for some examples but serves as a placeholder.
3. Creates an output grid by copying the input grid.
4. Colors the pixels corresponding to the calculated path coordinates green (value 3), *excluding* the start (blue) and end (red) pixels themselves.
5. Returns the modified grid.
"""

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

def get_arc_line_coords(r0, c0, r1, c1):
    """
    Calculates the coordinates of pixels on the line segment between (r0, c0) 
    and (r1, c1).
    
    NOTE: This function implements a standard Bresenham algorithm. Testing revealed
    that this does NOT perfectly match the paths generated in the ARC training
    examples for this specific task. The true ARC algorithm for this task remains
    unidentified based on the provided examples. This implementation is used as
    a placeholder.
    
    Args:
        r0, c0 (int): Starting row and column.
        r1, c1 (int): Ending row and column.
        
    Returns:
        list: A list of (row, col) tuples representing the pixels on the line,
              including the start and end points.
    """
    points = []
    dr = r1 - r0
    dc = c1 - c0
    sr = 1 if dr > 0 else -1
    sc = 1 if dc > 0 else -1
    # Handle zero delta cases for sign
    if dr == 0: sr = 0
    if dc == 0: sc = 0
    
    dr = abs(dr)
    dc = abs(dc)
    r, c = r0, c0
    
    points.append((r, c)) # Add start point
    
    # Determine major axis
    is_steep = dr > dc 
    
    if is_steep: # Row is major axis
        err = 2 * dc - dr
        major_steps = dr
        minor_delta = 2 * dc
        major_delta = 2 * (dc - dr) # Error update when minor step IS taken
        error_increment = minor_delta   # Error update when minor step is NOT taken
    else: # Column is major axis (or equal)
        err = 2 * dr - dc
        major_steps = dc
        minor_delta = 2 * dr
        major_delta = 2 * (dr - dc) # Error update when minor step IS taken
        error_increment = minor_delta   # Error update when minor step is NOT taken

    for _ in range(major_steps):
        if err >= 0: # Time to take a step in the minor direction
            if is_steep:
                c += sc
            else:
                r += sr
            err += major_delta
        
        # Always take a step in the major direction
        if is_steep:
            r += sr
        else:
            c += sc
        err += error_increment
        
        # Append the new point
        points.append((r, c))
            
    # Ensure the last point is exactly the target, handling potential off-by-one issues
    # in some Bresenham variants or edge cases.
    if points[-1] != (r1, c1):
         # If Bresenham didn't quite reach, check if we are adjacent and add final point
         last_r, last_c = points[-1]
         if abs(last_r - r1) <= 1 and abs(last_c - c1) <= 1:
             points.append((r1, c1))
         # else: More complex recovery might be needed, but indicates algo issue.

    # Remove potential duplicates added by the final check
    unique_points = []
    seen = set()
    for p in points:
        if p not in seen:
            unique_points.append(p)
            seen.add(p)
            
    return unique_points


def transform(input_grid):
    """
    Transforms the input grid by finding blue (1) and red (2) pixels
    and drawing a green (3) line between them using a placeholder line algorithm,
    excluding the endpoints.
    
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
        # using the placeholder line algorithm.
        line_coords = get_arc_line_coords(r0, c0, r1, c1)

        # Color the path pixels green (3)
        # Iterate through all calculated coordinates on the line
        for r, c in line_coords:
            # Only color the pixel if it is NOT the start point AND NOT the end point
            if (r, c) != start_coords and (r, c) != end_coords:
                # Check grid bounds as a safety measure
                if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                     output_grid[r, c] = 3 # Set color to green

    # Convert the final numpy array back to a list of lists for the required output format
    return output_grid.tolist()