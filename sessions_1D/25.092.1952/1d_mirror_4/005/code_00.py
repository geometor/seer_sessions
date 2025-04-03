import numpy as np
from typing import List, Tuple, Optional

"""
Reflects a contiguous colored line segment across a fixed maroon pivot pixel (9) 
within a 1D grid represented as a list. The background color is white (0). 
The transformation preserves the segment's color and length but changes its 
position based on reflection relative to the pivot index. The pivot pixel's 
position remains unchanged.
"""

# Helper function to find the pivot pixel (color 9)
def find_pivot(grid_list: List[int]) -> Optional[int]:
    """
    Finds the index of the pivot pixel (maroon, 9).
    
    Args:
        grid_list: The input grid as a list of integers.

    Returns:
        The index of the pivot pixel, or None if not found.
    """
    for i, pixel in enumerate(grid_list):
        if pixel == 9:
            return i
    return None # Pivot not found

# Helper function to find the colored segment
def find_segment(grid_list: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the segment (color, start_index, end_index) of non-white, non-pivot color.
    
    Args:
        grid_list: The input grid as a list of integers.

    Returns:
        A tuple containing (segment_color, start_index, end_index), 
        or None if no segment is found.
    """
    segment_color = -1
    start_index = -1
    end_index = -1
    
    for i, pixel in enumerate(grid_list):
        # Look for the start of a segment (non-zero, non-nine)
        if pixel != 0 and pixel != 9: 
            if start_index == -1: # Found the start
                segment_color = pixel
                start_index = i
            # Check if the segment continues with the same color
            # If it's the last pixel or the next pixel is different, the segment ends here
            # Make sure we only return a segment if we found its end.
            if start_index != -1 and (i == len(grid_list) - 1 or grid_list[i+1] != segment_color):
                end_index = i
                # Found the complete segment, return its details
                return segment_color, start_index, end_index
                
    # If loop finishes without returning, no valid segment was found
    return None 

# Main transformation function
def transform(input_grid) -> List[int]:
    """
    Transforms the input grid by reflecting the colored segment across the pivot.
    
    Args:
        input_grid: The input grid, typically a 1D numpy array or list.

    Returns:
        The transformed grid as a list.
    """
    # Ensure input is a list for consistent processing and to avoid numpy bool ambiguity
    if isinstance(input_grid, np.ndarray):
      # Handle potential multi-dimensional arrays if necessary, flatten for 1D task
      if input_grid.ndim > 1:
          input_list = list(input_grid.flatten())
      else:
          input_list = list(input_grid)
    else:
       input_list = list(input_grid) # Assume it's already list-like

    grid_size = len(input_list)
    
    # Initialize output_grid with background color (0)
    output_grid = [0] * grid_size
    
    # Step 1: Locate the pivot pixel (maroon, 9)
    pivot_index = find_pivot(input_list)
    
    # Handle case where pivot is missing 
    if pivot_index is None:
        # Based on task structure, this shouldn't happen, but return empty grid as a fallback
        return output_grid 
        
    # Place the pivot in the output grid - it doesn't move
    output_grid[pivot_index] = 9
  
    # Step 2: Locate the colored segment
    segment_info = find_segment(input_list)

    # If no segment found (only background and pivot), return grid with just pivot
    if segment_info is None:
       return output_grid 
       
    segment_color, start_in, end_in = segment_info

    # Step 3: Calculate distances from pivot to segment ends in input
    dist_start_in = pivot_index - start_in 
    dist_end_in = pivot_index - end_in # Note: end_in is inclusive

    # Step 4: Calculate new segment position based on reflection
    # New start relative distance = old end relative distance
    # New end relative distance = old start relative distance
    start_out = pivot_index + dist_end_in
    end_out = pivot_index + dist_start_in

    # Step 5: Place the reflected segment in the output grid
    # Determine the iteration range, ensuring correct order regardless of reflection direction
    min_out_idx = min(start_out, end_out)
    max_out_idx = max(start_out, end_out)
  
    for i in range(min_out_idx, max_out_idx + 1):
        # Basic boundary check to ensure we stay within the grid
        if 0 <= i < grid_size: 
            # Crucially, check we are not overwriting the pivot pixel
            if i != pivot_index: 
                output_grid[i] = segment_color
            # If i == pivot_index, we do nothing, preserving the pivot placed in Step 1.

    # Return the completed output grid
    return output_grid