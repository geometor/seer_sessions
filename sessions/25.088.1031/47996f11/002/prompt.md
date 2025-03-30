
Previous Code:
```python
import numpy as np

"""
Transforms the input grid by replacing each magenta pixel (6) with the 
color of its nearest non-magenta neighbor. 
Distance is measured using Manhattan distance (|row1 - row2| + |col1 - col2|).
If multiple non-magenta neighbors are equidistant, a tie-breaking rule based 
on direction is applied: Up is preferred, then Left, then Down, then Right. 
If there's still a tie (e.g., two equidistant 'Up' neighbors, though unlikely 
with Manhattan distance unless they are the same point relative to the center), 
the one with the smallest row index is chosen, and finally the one with the 
smallest column index.
Non-magenta pixels remain unchanged in the output grid.
"""

def get_sort_key(coord, center_r, center_c):
    """
    Generates a sort key for a candidate coordinate based on its position 
    relative to a center point (the magenta pixel).
    The key prioritizes directions: Up (0), Left (1), Down (2), Right (3).
    Other relative positions (like diagonals) get a lower priority (4).
    Secondary and tertiary sorting uses row and column index for stability.
    
    Args:
        coord (tuple): The (row, column) of the candidate neighbor.
        center_r (int): The row index of the center pixel (magenta).
        center_c (int): The column index of the center pixel (magenta).

    Returns:
        tuple: A sort key (priority, row, column).
    """
    nr, nc = coord
    r, c = center_r, center_c
    
    # Calculate relative position
    dr = nr - r
    dc = nc - c

    # Assign priority based on cardinal direction relative to center
    if dr < 0 and dc == 0:  # Up
        priority = 0
    elif dr == 0 and dc < 0:  # Left
        priority = 1
    elif dr > 0 and dc == 0:  # Down
        priority = 2
    elif dr == 0 and dc > 0:  # Right
        priority = 3
    else: # Diagonal or other relative position (less preferred than cardinal)
        priority = 4 

    # Return tuple for sorting: (priority, absolute_row, absolute_col)
    return (priority, nr, nc)


def find_closest_non_magenta(grid, r, c):
    """
    Finds the color of the nearest non-magenta pixel to the given (r, c).

    Iterates through the grid, calculates Manhattan distances to non-magenta
    pixels, finds the minimum distance, collects all candidates at that minimum
    distance, and then sorts them using the directional priority rule defined
    in `get_sort_key`.

    Args:
        grid (np.array): The input grid.
        r (int): The row index of the magenta pixel.
        c (int): The column index of the magenta pixel.

    Returns:
        int: The color value of the selected nearest non-magenta neighbor.
    """
    rows, cols = grid.shape
    min_dist = float('inf')
    candidates = [] # Stores tuples of (nr, nc) for pixels at min_dist

    # Step 1: Find the minimum distance to any non-magenta pixel
    for nr in range(rows):
        for nc in range(cols):
            # Check if the pixel is non-magenta (color != 6)
            if grid[nr, nc] != 6: 
                # Calculate Manhattan distance
                dist = abs(r - nr) + abs(c - nc)
                
                # Update minimum distance found so far
                if dist < min_dist:
                    min_dist = dist
    
    # If min_dist remains infinity, it means the grid has no non-magenta pixels
    # (or is empty). Return the original color (magenta) as a fallback.
    if min_dist == float('inf'):
        return grid[r,c] 

    # Step 2: Collect all non-magenta pixels exactly at the minimum distance
    for nr in range(rows):
        for nc in range(cols):
            if grid[nr, nc] != 6:
                dist = abs(r - nr) + abs(c - nc)
                if dist == min_dist:
                    candidates.append((nr, nc))

    # Step 3: Apply tie-breaking sort based on directional priority
    # The sort key uses Up(0)/Left(1)/Down(2)/Right(3) priority, then row, then col.
    candidates.sort(key=lambda coord: get_sort_key(coord, r, c)) 
    
    # Step 4: The first candidate after sorting is the chosen one
    best_nr, best_nc = candidates[0]
    
    # Return the color of the chosen neighbor
    return grid[best_nr, best_nc]

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    # Create a copy to store the output, preserving non-magenta pixels initially
    output_grid = np.copy(grid)
    rows, cols = grid.shape

    # Find coordinates of all magenta pixels that need processing
    magenta_coords = np.argwhere(grid == 6)

    # Iterate only through the magenta pixels found
    for r, c in magenta_coords:
        # For each magenta pixel, find the color of its prioritized nearest neighbor
        replacement_color = find_closest_non_magenta(grid, r, c)
        # Update the corresponding pixel in the output grid
        output_grid[r, c] = replacement_color
                
    # Convert the final numpy array back to a list of lists format for the output
    return output_grid.tolist()
```
Results for code_00.py:
Train Set Error: Timeout: Code execution exceeded 10 seconds
