import numpy as np
import copy # Although numpy is used, keeping copy import just in case list operations were preferred later.

"""
Identifies the largest rectangular area composed entirely of white (0) pixels 
in the input grid. It then fills this specific area with azure (8) pixels in 
the output grid, leaving all other pixels unchanged. "Largest" is defined by 
the total number of pixels (area). If multiple rectangles share the same 
maximum area, the one whose top-left corner has the smallest row index is chosen. 
If there is still a tie, the one with the smallest column index for that row 
index is chosen.
"""

def transform(input_grid_list):
    """
    Transforms the input grid by finding the largest rectangle containing only 
    white (0) pixels and filling that area with azure (8) pixels.

    Args:
        input_grid_list: A list of lists representing the input grid, where each 
                         inner list is a row and values are integers 0-9.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    # Convert input list of lists to a NumPy array for efficient slicing and checking
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    
    max_area = -1  # Initialize max area found so far (-1 indicates none found yet)
    best_rect_coords = None # To store coordinates (r1, c1, r2, c2) of the best rectangle

    # Iterate through all possible top-left corners (r1, c1) for potential rectangles
    for r1 in range(height):
        for c1 in range(width):
            # Iterate through all possible bottom-right corners (r2, c2) for potential rectangles
            # Note: r2 starts from r1, c2 starts from c1 to define valid rectangles
            for r2 in range(r1, height):
                for c2 in range(c1, width):
                    
                    # Define the subgrid corresponding to the current potential rectangle
                    # Slicing is [start_row:end_row_exclusive, start_col:end_col_exclusive]
                    # So we use r2+1 and c2+1 to include row r2 and column c2
                    subgrid = input_grid[r1:r2+1, c1:c2+1]
                    
                    # Check if all pixels within this subgrid are white (color code 0)
                    if np.all(subgrid == 0):
                        # If the subgrid is all white, calculate its area
                        current_area = subgrid.size # size attribute gives total number of elements (height * width)
                        
                        # Check if this rectangle's area is greater than the maximum area found so far.
                        # The nested loop structure (iterating r1, then c1, then r2, then c2) ensures
                        # that the first time we encounter a rectangle of the maximum possible size,
                        # it will be the one with the smallest r1 index, and for ties in r1,
                        # the smallest c1 index. By only updating when `current_area > max_area`,
                        # we guarantee that this first, top-leftmost maximal rectangle is chosen.
                        if current_area > max_area:
                            max_area = current_area
                            best_rect_coords = (r1, c1, r2, c2) # Store the inclusive coordinates

    # Create the output grid initially as a copy of the input grid.
    # Using np.copy ensures we don't modify the original input array implicitly.
    output_grid = np.copy(input_grid)

    # If an all-white rectangle was found (i.e., max_area is not -1 and best_rect_coords is set)
    if best_rect_coords:
        # Unpack the coordinates of the largest all-white rectangle found
        r1, c1, r2, c2 = best_rect_coords
        
        # Fill the identified rectangular area in the output grid with azure (color code 8)
        # Use slicing again for efficient modification.
        output_grid[r1:r2+1, c1:c2+1] = 8
                
    # Convert the final NumPy array back to a standard Python list of lists format for the ARC environment
    return output_grid.tolist()
