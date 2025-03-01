"""
Identify connected components of the same color (excluding black/background). Within each component, detect "H" shapes (two roughly vertical parts connected by a horizontal part, or inferred "H" from diagonal lines). Recolor the 2x2 center of each "H" red. If no "H" is found, check for diagonal lines and convert them into 2x2 red squares.
"""

import numpy as np
from scipy.ndimage import label

def find_center(coords):
    """Finds the approximate center of a set of coordinates."""
    return (int(np.mean(coords[:, 0])), int(np.mean(coords[:, 1])))

def is_h_shape(coords, grid_shape):
    """Checks if a set of coordinates roughly forms an "H" shape."""
    if len(coords) < 3:
        return False, None

    min_row, max_row = np.min(coords[:, 0]), np.max(coords[:, 0])
    min_col, max_col = np.min(coords[:, 1]), np.max(coords[:, 1])
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    # Check if the object is wider than it should be (to eliminate straight lines)
    if width > 1.5 * height or height > 1.5 * width:
        if is_diagonal(coords):
            return False, "diagonal" #flag
        else: return False, None

    # Divide the region into potential left, right, and center parts
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2


    left_coords = coords[(coords[:, 1] <= center_col) & (coords[:,0] != center_row)]
    right_coords = coords[(coords[:, 1] >= center_col) & (coords[:,0] != center_row)]
    center_coords = coords[(coords[:, 0] == center_row)]

    # Basic checks for connectivity (more robust checks could be added)
    if len(left_coords) > 0 and len(right_coords) > 0 and len(center_coords) > 0:
        return True, (center_row, center_col)
    elif len(left_coords) > 0 and len(right_coords) >0:
        #infer
        return True, (center_row, center_col)
    else:
        return False, None


def is_diagonal(coords):
    """Checks for a diagonal line with tolerance."""
    if len(coords) < 2:
        return False

    rows, cols = coords[:, 0], coords[:, 1]
    
    # Calculate slope between consecutive points and check if it's consistent
    slopes = np.diff(rows) / (np.diff(cols) + 1e-5) #add small increment

    # Check if slopes are roughly the same, return if diff within tolerance 
    if np.all(np.abs(np.diff(slopes)) < 0.5) :  # Tolerance
        return True
    else:
        return False
    

def transform(input_grid):
    """Transforms the input grid according to the described rules."""

    output_grid = np.copy(input_grid)
    labeled_grid, num_features = label(input_grid > 0)  # Label connected components, excluding 0

    for i in range(1, num_features + 1):  # Iterate through each labeled object
        coords = np.argwhere(labeled_grid == i)
        is_h, center = is_h_shape(coords, input_grid.shape)
        
        if is_h:
            if center is not None:
                center_row, center_col = center
                 # Recolor 2x2 area, handling boundaries
                row_start = max(0, center_row - 1)
                row_end = min(output_grid.shape[0], center_row + 1)
                col_start = max(0, center_col - 1)
                if output_grid.shape[1] - center_col >= 1:
                  col_end = min(output_grid.shape[1], center_col + 2) #extend if exists
                else:
                    col_end = min(output_grid.shape[1], center_col + 1) #keep if already at max

                output_grid[row_start:row_end, col_start:col_end] = 2
        elif center == "diagonal": #check if flag returned
            center_row, center_col = find_center(coords) #find center for 2x2
            # Recolor 2x2 area, handling boundaries
            row_start = max(0, center_row - 1)
            row_end = min(output_grid.shape[0], center_row + 1)
            col_start = max(0, center_col - 1)
            col_end = min(output_grid.shape[1], center_col + 1)

            output_grid[row_start:row_end, col_start:col_end] = 2
            
    return output_grid