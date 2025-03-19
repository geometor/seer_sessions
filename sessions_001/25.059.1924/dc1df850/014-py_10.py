"""
1.  **Identify the "L" shape:** Find the largest contiguous "L" shape composed of either red, or green pixels. The "L" shape consists of a corner pixel with exactly two adjacent pixels of the same color, and each of those must have exactly one other neighbor of the same color (not each other).
2.  **Mirror/Flip:** Mirror the "L" shape along the main diagonal (top-left to bottom-right). This effectively swaps the "L"'s orientation.
3. **Change Color:**
    If the original L shape is green, change all pixels in the mirrored shape to blue.
    If the original L shape is red, change all pixels in the mirrored shape to blue, *unless* the "long" side of the L shape has length 2, in which case change all pixels in the mirrored shape to green.
4. All other pixels remain white (0).
"""

import numpy as np

def find_l_shape(input_grid):
    """Finds an L-shaped object in the grid."""
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color == 2 or color == 3:  # Red or green
                # Check for L shape (horizontal and vertical)
                if r + 1 < rows and c + 1 < cols:
                    #   X
                    # X X
                    if input_grid[r+1,c] == color and input_grid[r+1, c+1] == color and input_grid[r,c+1] !=color:
                        return [(r, c), (r + 1, c), (r + 1, c + 1)], color, 'down_right'

                    # X X
                    #   X
                    if input_grid[r,c+1] == color and input_grid[r+1,c+1] == color and input_grid[r+1,c] != color:
                       return [(r, c), (r, c+1), (r + 1, c + 1)], color, 'up_right'

                if r + 1 < rows and c - 1 >= 0:
                    # X
                    # X X
                    if input_grid[r + 1, c] == color and input_grid[r + 1, c - 1] == color and input_grid[r,c-1] != color:
                        return [(r, c), (r + 1, c), (r + 1, c - 1)], color, 'down_left'
                
                if r-1 >= 0 and c+1 < cols:
                    # X X
                    # X
                    if input_grid[r-1,c] == color and input_grid[r-1,c+1] == color and input_grid[r,c+1] != color:
                        return [(r,c), (r-1,c), (r-1, c+1)], color, 'down_right_rev'

    return [], 0, ''

def mirror_l_shape(l_coords):
    """Mirrors the L shape coordinates along the main diagonal."""
    # find the "corner"
    corner = None
    # corner is the pixel that is adjacent to the other two
    
    if l_coords[0][0] == l_coords[1][0] and l_coords[0][1] == l_coords[2][1]:
        corner = l_coords[0]
    elif l_coords[0][1] == l_coords[1][1] and l_coords[0][0] == l_coords[2][0]:
        corner = l_coords[0]
    elif l_coords[1][0] == l_coords[0][0] and l_coords[1][1] == l_coords[2][1]:
        corner = l_coords[1]
    elif l_coords[1][1] == l_coords[0][1] and l_coords[1][0] == l_coords[2][0]:
        corner = l_coords[1]
    elif l_coords[2][0] == l_coords[0][0] and l_coords[2][1] == l_coords[1][1]:
        corner = l_coords[2]
    elif l_coords[2][1] == l_coords[0][1] and l_coords[2][0] == l_coords[1][0]:
        corner = l_coords[2]
    
    mirrored_coords = []
    for r, c in l_coords:
      # transformation: shift by corner, swap coords, and shift back
      mirrored_coords.append( (c - corner[1] + corner[0], r-corner[0] + corner[1]) )
    return mirrored_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # find the L shape and its color
    l_shape_coords, color, orientation = find_l_shape(input_grid)

    if l_shape_coords:
        # mirror the L shape
        mirrored_coords = mirror_l_shape(l_shape_coords)

        # determine the new color
        new_color = 1  # Default to blue
        if color == 2: # if red
          if orientation == 'down_right' or orientation == 'up_right':
            new_color = 3 # set to green

        # set mirrored shape with new color
        for r, c in mirrored_coords:
            if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                output_grid[r, c] = new_color

    return output_grid