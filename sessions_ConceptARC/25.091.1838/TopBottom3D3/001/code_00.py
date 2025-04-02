import numpy as np
from typing import List, Tuple, Set, Dict, Optional

"""
Identifies two non-background colors in the input grid. One color ('inner_color') 
has a horizontal span (min_col to max_col) that is contained within or equal 
to the horizontal span of the other color ('outer_color'). The transformation 
creates an output grid where the 'inner_color' is removed. The 'outer_color' 
then fills a rectangular horizontal band in the output. This band spans the 
minimum to maximum column index occupied by *any* non-background color in the 
input. The filling only occurs on rows where the 'outer_color' was originally 
present in the input grid. All other cells are set to the background color (white, 0).
"""

def _find_non_background_colors(grid: np.ndarray) -> List[int]:
    """Finds unique non-zero colors in the grid."""
    return [color for color in np.unique(grid) if color != 0]

def _get_color_horizontal_bounds(grid: np.ndarray, color: int) -> Optional[Tuple[int, int]]:
    """Finds the minimum and maximum column index for a given color."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_col, max_col

def _get_global_horizontal_bounds(grid: np.ndarray) -> Optional[Tuple[int, int]]:
    """Finds the minimum and maximum column index for any non-zero color."""
    coords = np.argwhere(grid != 0)
    if coords.size == 0:
        return None
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])
    return min_col, max_col
    
def _get_rows_with_color(grid: np.ndarray, color: int) -> Set[int]:
    """Finds the set of row indices where a given color appears."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return set()
    return set(coords[:, 0])

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the described rule:
    1. Identify the two non-background colors (c1, c2).
    2. Determine which color's horizontal span is contained within the other's. 
       The contained color is 'inner', the other is 'outer'.
    3. Find the rows where the 'outer' color appears in the input.
    4. Find the overall min/max column index of any non-background color.
    5. Create an output grid filled with background color.
    6. In the output grid, fill the overall horizontal span with the 'outer' 
       color, but only on the rows identified in step 3.
    """
    
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(grid)

    # 1. Identify the non-background colors
    colors = _find_non_background_colors(grid)
    
    # Handle cases with less than two colors (though examples show two)
    if len(colors) < 2:
        # If only one color, maybe just return it or an empty grid?
        # Based on the problem description, we expect two colors. 
        # If not, maybe return the input or an empty grid.
        # Let's return an empty grid for now, as the core logic requires two colors.
         return output_grid.tolist() 
         
    c1, c2 = colors[0], colors[1]

    # 2. Determine inner and outer colors based on horizontal bounds containment
    bounds_c1 = _get_color_horizontal_bounds(grid, c1)
    bounds_c2 = _get_color_horizontal_bounds(grid, c2)

    if bounds_c1 is None or bounds_c2 is None:
        # Should not happen if colors were found, but handle defensively
        return output_grid.tolist() 

    min_c1, max_c1 = bounds_c1
    min_c2, max_c2 = bounds_c2

    c1_is_contained = (min_c2 <= min_c1) and (max_c1 <= max_c2)
    c2_is_contained = (min_c1 <= min_c2) and (max_c2 <= max_c1)

    # Determine outer color (the one NOT contained, or if bounds are equal, default?)
    # The logic assumes one is strictly contained or they are different.
    # If c1 is contained and c2 is not, outer is c2.
    # If c2 is contained and c1 is not, outer is c1.
    # If neither is contained (e.g., overlap), or both (bounds equal), the rule needs refinement.
    # Based on examples, one is clearly contained horizontally within the other's span.
    
    outer_color = -1 # Initialize with invalid value
    if c1_is_contained and not c2_is_contained:
        outer_color = c2
    elif c2_is_contained and not c1_is_contained:
        outer_color = c1
    elif c1_is_contained and c2_is_contained: # Bounds are identical
         # This case isn't in examples. Need a tie-breaker.
         # Let's arbitrarily choose one, maybe the first one found? Or error?
         # For now, let's assume this won't happen based on examples.
         # If it does, this might fail. Let's pick c1 arbitrarily for now.
         # outer_color = c1 # Or maybe c2? Or raise error? Let's stick to defined cases.
         print(f"Warning: Colors {c1} and {c2} have identical horizontal bounds. Rule unclear.")
         return output_grid.tolist() # Return empty for ambiguous case
    else: # Neither contained (e.g. side-by-side or overlapping without containment)
         print(f"Warning: Neither color {c1} nor {c2} is horizontally contained within the other. Rule unclear.")
         return output_grid.tolist() # Return empty for ambiguous case

    if outer_color == -1:
         print("Error: Could not determine outer color.")
         return output_grid.tolist()


    # 3. Find rows where the outer color appears
    outer_rows = _get_rows_with_color(grid, outer_color)

    # 4. Find the overall global horizontal bounds
    global_bounds = _get_global_horizontal_bounds(grid)
    if global_bounds is None:
        return output_grid.tolist() # No non-zero pixels found
    global_min_col, global_max_col = global_bounds
    
    # 5 & 6. Fill the output grid
    for r in outer_rows:
        # Check row index is valid (should be, but defensive)
        if 0 <= r < height:
            # Fill columns from global_min_col to global_max_col inclusive
            for c in range(global_min_col, global_max_col + 1):
                 # Check column index is valid (should be, but defensive)
                 if 0 <= c < width:
                     output_grid[r, c] = outer_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()