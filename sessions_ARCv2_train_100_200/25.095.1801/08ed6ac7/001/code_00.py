import numpy as np # Commonly used for grid operations, though not strictly necessary for this logic
from typing import List # For type hinting

"""
Identifies distinct vertical segments composed of '5's within the input grid. 
Assigns a unique positive integer ID (starting from 1) to each segment based 
on the order in which their top-most '5' is encountered during a top-to-bottom, 
left-to-right scan. Replaces all '5's belonging to a segment with that segment's 
assigned ID in the output grid, leaving zeros unchanged.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms an input grid by identifying vertical segments of '5's and 
    assigning them sequential IDs based on scan order.

    Args:
        input_grid: A list of lists representing the input grid with 0s and 5s.

    Returns:
        A list of lists representing the transformed grid with 0s and segment IDs.
    """
    if not input_grid:
        return []
        
    rows = len(input_grid)
    if rows == 0:
        return [[]]
    cols = len(input_grid[0])
    if cols == 0:
         return [[] for _ in range(rows)]

    # Initialize output_grid with the same dimensions, filled with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Create a grid to keep track of visited '5' cells that belong to an assigned segment
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    # Initialize the segment ID counter
    current_id = 1

    # Scan the input grid: top-to-bottom, left-to-right
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell contains a '5' and has not yet been assigned to a segment
            if input_grid[r][c] == 5 and not visited[r][c]:
                # This is the top-most cell of a new segment encountered in scan order
                segment_id = current_id
                
                # Trace vertically downwards from (r, c) to find all contiguous '5's in this column
                curr_r = r
                while curr_r < rows and input_grid[curr_r][c] == 5:
                    # Assign the current segment ID to the output grid at this position
                    output_grid[curr_r][c] = segment_id
                    # Mark this cell as visited/assigned
                    visited[curr_r][c] = True
                    # Move down to the next cell in the segment
                    curr_r += 1
                
                # Increment the ID for the next segment to be found
                current_id += 1
            
            # If the cell is 0, or a '5' that's already part of an assigned segment, 
            # the output_grid already has the correct value (0 or a previously assigned ID), 
            # so no action is needed here.

    # Return the fully transformed grid
    return output_grid