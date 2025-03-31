import numpy as np

"""
This module transforms an input grid according to the following rule:
1. Identify the unique blue pixel (value 1) and the unique red pixel (value 2) in the input grid. These represent the start and end points.
2. Calculate the sequence of grid coordinates that form a path connecting the start and end points using a specific grid-based line drawing algorithm observed in the ARC examples. Note: Standard Bresenham variants tested do not perfectly replicate these paths; the exact algorithm requires precise implementation matching the examples.
3. Create an output grid by copying the input grid.
4. Color the pixels corresponding to the calculated path coordinates green (value 3), *excluding* the coordinates of the original blue (start) and red (end) pixels.
5. Return the modified grid.
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

# Placeholder for the specific line algorithm needed for this ARC task
# The implementations tested (standard Bresenham variants) did not match
# the exact paths from the training examples. This function needs to be
# implemented to replicate the observed behavior accurately.
def get_arc_line_coords(r0, c0, r1, c1):
    """
    Calculates the coordinates of pixels on the specific grid line path
    between (r0, c0) and (r1, c1) as required by the ARC task examples.
    
    (This is a placeholder implementation - it uses a standard integer Bresenham,
    which was shown NOT to match the examples perfectly. The correct algorithm
    needs to replace this.)
    
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
        major_delta = 2 * dr
    else: # Column is major axis (or equal)
        err = 2 * dr - dc
        major_steps = dc
        minor_delta = 2 * dr
        major_delta = 2 * dc

    for _ in range(major_steps):
        if is_steep: # Step row first
            r += sr
            if err >= 0:
                c += sc
                err -= major_delta # equivalent to 2*dr
        else: # Step col first
            c += sc
            if err >= 0:
                r += sr
                err -= major_delta # equivalent to 2*dc
        
        # Update error term for the minor axis check
        err += minor_delta 
        
        # Append the new point
        points.append((r, c))
            
    return points


def transform(input_grid):
    """
    Transforms the input grid by finding blue (1) and red (2) pixels
    and drawing a green (3) line between them according to the specific
    ARC task's line algorithm, excluding the endpoints.
    
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
        # using the specific algorithm required (represented by get_arc_line_coords)
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