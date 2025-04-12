```python
import numpy as np
from typing import List, Tuple, Optional, Dict

"""
Transformation Rule Natural Language Description:

1.  **Identify Template Size:** Locate the bounding box of all white (0) pixels in the input grid. Determine its height (H) and width (W).
2.  **Identify & Count Candidates:** Scan the input grid to find all unique HxW subgrids that contain *no* white pixels. Store the location (top-left corner) of the first occurrence of each unique pattern. Count the number of unique patterns found (k).
3.  **Sort Candidates:** Create a list of these unique candidate patterns and sort them lexicographically. Let the sorted list be S = [S0, S1, ..., S(k-1)].
4.  **Select Target Pattern:**
    *   If the count `k` is equal to the template area `H * W`: Select the pattern at index `1 % k` in the sorted list (effectively index 1 if k>1, index 0 if k=1) as the Target Pattern.
    *   If the count `k` is *not* equal to the template area `H * W`: Select the pattern at index `k-1` (the last pattern / lexicographically largest) in the sorted list as the Target Pattern.
5.  **Find First Occurrence:** Retrieve the pre-recorded location of the first occurrence for the selected Target Pattern.
6.  **Extract Output:** Return the HxW subgrid from the input grid starting at the location found in step 5.
"""


# Helper function to find the bounding box of all pixels of a specific color
def find_color_bbox(grid: np.ndarray, color: int) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the minimum bounding box containing all pixels of the given color.
    Returns (min_row, min_col, height, width) or None if color not found.
    """
    rows, cols = np.where(grid == color)
    if rows.size == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    # Return the top-left corner (min_row, min_col) as well
    return min_row, min_col, height, width 

# Helper function to extract a subgrid
def extract_subgrid(grid: np.ndarray, r: int, c: int, h: int, w: int) -> np.ndarray:
    """Extracts a subgrid of size h x w starting at (r, c)."""
    return grid[r:r+h, c:c+w]

# Helper function to convert numpy array to tuple for dict keys/sorting
def grid_to_tuple(grid: np.ndarray) -> tuple:
    """Converts a numpy array (grid) to a hashable tuple of tuples."""
    # Ensure the input is a 2D numpy array before mapping
    if not isinstance(grid, np.ndarray):
         return tuple() # Should not happen with proper slicing
    if grid.ndim == 1:
         grid = grid.reshape(1, -1) # Handle 1D case (e.g., 1xN or Nx1)
    elif grid.ndim == 0:
         grid = grid.reshape(1, 1) # Handle scalar case (1x1)
         
    # Ensure elements within rows are tuples of standard Python ints if needed,
    # although numpy types are usually hashable. Stick with numpy types for now.
    return tuple(map(tuple, grid))

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation based on finding a white template block,
    identifying candidate patterns without white pixels, selecting one based
    on comparing candidate count (k) to template area (H*W), 
    and finding the first occurrence of the selected pattern.
    """
    input_array = np.array(input_grid, dtype=int)
    grid_h, grid_w = input_array.shape

    # 1. Identify Template Size
    white_bbox = find_color_bbox(input_array, 0)
    if white_bbox is None:
        # No white block found, cannot determine template size.
        return [] # Return empty list for failure/ambiguity
        
    _, _, h, w = white_bbox # Template height and width

    # Check if template size is valid
    if h <= 0 or w <= 0 or h > grid_h or w > grid_w:
         return []

    # 2. Identify & Count Candidates (unique patterns without white pixels)
    #    Store the first occurrence location for each unique pattern found.
    pattern_first_occurrence: Dict[tuple, Tuple[int, int]] = {}

    for r in range(grid_h - h + 1):
        for c in range(grid_w - w + 1):
            subgrid = extract_subgrid(input_array, r, c, h, w)
            
            # Skip if the subgrid contains any white pixels (color 0)
            if np.any(subgrid == 0):
                continue
                
            pattern_key = grid_to_tuple(subgrid)
            
            # Record the first time (top-leftmost location) we encounter this pattern
            if pattern_key not in pattern_first_occurrence:
                pattern_first_occurrence[pattern_key] = (r, c)

    # If no non-white patterns of the required size were found
    if not pattern_first_occurrence:
         return []

    # 3. Sort Candidates
    candidate_patterns = list(pattern_first_occurrence.keys())
    k = len(candidate_patterns)
    sorted_patterns = sorted(candidate_patterns)
    
    # 4. Select Target Pattern
    hw = h * w
    target_pattern_key = None

    if k > 0: # Ensure there are candidates to select from
        if k == hw:
            # Rule: If k == H*W, select the pattern at index (1 % k)
            # This handles k=1 case correctly (1%1=0), and k>1 case (selects index 1)
            select_index = 1 % k
            target_pattern_key = sorted_patterns[select_index]
        else:
            # Rule: If k != H*W, select the pattern at index k-1 (largest)
            select_index = k - 1
            target_pattern_key = sorted_patterns[select_index]
    
    # If no target pattern was selected (e.g., if k=0, although handled above)
    if target_pattern_key is None:
        return []

    # 5. Find First Occurrence location (already stored)
    try:
        first_occurrence_r, first_occurrence_c = pattern_first_occurrence[target_pattern_key]
    except KeyError:
         # This should not happen if target_pattern_key came from the dictionary keys
         return [] 

    # 6. Extract and return the subgrid found at that first occurrence location.
    output_array = extract_subgrid(input_array, first_occurrence_r, first_occurrence_c, h, w)
    
    # Convert the numpy array back to a list of lists for the final output
    return output_array.tolist()
```