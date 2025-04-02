import numpy as np
from typing import List, Tuple

"""
Identifies the single dominant non-white color in the input grid.
Finds all horizontal segments ('stripes') of this dominant color.
Filters these segments to find the 'incomplete' ones (those shorter than the grid width).
Calculates the bounding box (min/max row and column) enclosing all pixels of these incomplete stripes.
Determines the output grid dimensions: height = bounding_box_height + 2, width = bounding_box_width.
Creates the output grid filled entirely with the dominant color using the calculated dimensions.
"""

def _find_dominant_color(grid: np.ndarray) -> int:
    """Finds the unique non-white color in the grid."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return int(color)
    # Should not happen based on task description, but handle gracefully
    return 0 

def _find_incomplete_stripes(grid: np.ndarray, dominant_color: int) -> List[Tuple[int, int, int]]:
    """
    Finds all horizontal segments of the dominant color that are shorter than the grid width.
    Returns a list of tuples: (row_index, start_col_index, end_col_index).
    """
    height, width = grid.shape
    incomplete_stripes = []
    
    for r in range(height):
        start_col = -1
        for c in range(width):
            # Start of a potential segment
            if grid[r, c] == dominant_color and start_col == -1:
                start_col = c
            # End of a segment (either different color or end of row)
            if (grid[r, c] != dominant_color or c == width - 1) and start_col != -1:
                end_col = c - 1 if grid[r, c] != dominant_color else c
                segment_len = end_col - start_col + 1
                # Check if the segment is incomplete
                if segment_len < width:
                     # Check if the whole segment actually consists of the dominant color
                     # This handles cases where a non-dominant color might be within the segment bounds
                     is_solid = np.all(grid[r, start_col:end_col+1] == dominant_color)
                     if is_solid:
                         incomplete_stripes.append((r, start_col, end_col))
                start_col = -1 # Reset for the next potential segment in the row
                
    return incomplete_stripes

def _calculate_bounding_box(stripes: List[Tuple[int, int, int]]) -> Tuple[int, int, int, int]:
    """
    Calculates the min/max row and column indices covering all incomplete stripes.
    Returns (min_row, max_row, min_col, max_col).
    Returns (0, -1, 0, -1) if no stripes are provided, indicating an empty box.
    """
    if not stripes:
        return (0, -1, 0, -1) # Indicates no bounding box found

    min_r, min_c = float('inf'), float('inf')
    max_r, max_c = float('-inf'), float('-inf')

    for r, start_c, end_c in stripes:
        min_r = min(min_r, r)
        max_r = max(max_r, r)
        min_c = min(min_c, start_c)
        max_c = max(max_c, end_c)
        
    return min_r, max_r, min_c, max_c


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the properties of incomplete horizontal stripes.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # 1. Identify the dominant non-white color
    dominant_color = _find_dominant_color(grid_np)
    if dominant_color == 0: # Handle edge case where input might be all white
        return [] # Or return an empty grid of appropriate size? Task unclear. Returning empty list for now.

    # 2. Find all incomplete horizontal stripes of the dominant color
    incomplete_stripes = _find_incomplete_stripes(grid_np, dominant_color)
    
    # Handle case where no incomplete stripes are found (unlikely based on examples)
    if not incomplete_stripes:
        # Fallback behavior: Maybe return a 1x1 grid of the dominant color? Or original?
        # Let's return a 1x1 grid of the dominant color as a guess.
        return [[dominant_color]] 

    # 3. Calculate the bounding box encompassing all incomplete stripes
    min_r, max_r, min_c, max_c = _calculate_bounding_box(incomplete_stripes)
    
    # 4. Determine the dimensions of the bounding box
    bbox_h = max_r - min_r + 1
    bbox_w = max_c - min_c + 1
    
    # 5. Calculate the output grid dimensions
    output_h = bbox_h + 2
    output_w = bbox_w
    
    # 6. Create the output grid filled with the dominant color
    output_grid_np = np.full((output_h, output_w), dominant_color, dtype=int)
    
    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid