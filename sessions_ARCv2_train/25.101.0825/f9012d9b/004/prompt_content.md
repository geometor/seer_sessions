
Previous Code:
```python
import numpy as np
from typing import List, Tuple, Optional, Dict

"""
Transformation Rule Natural Language Description:

1.  **Identify Template Size:** Locate the bounding box of all white (0) pixels in the input grid. Let its dimensions be Height (H) and Width (W).
2.  **Identify Candidate Patterns:** Scan the input grid and find all unique HxW subgrids that do *not* contain any white pixels (value 0). Store the location (top-left corner) of the first occurrence of each unique pattern.
3.  **Select Target Pattern:** Apply a selection rule to choose one specific pattern (P_target) from the unique candidate patterns identified in step 2. The rule used here is based on comparing the count (k) of unique candidate patterns to the size of the template (H * W):
    - If k equals H * W, select the lexicographically *smallest* candidate pattern.
    - If k does not equal H * W, select the lexicographically *largest* candidate pattern.
    - NOTE: This rule works for train_1 and train_3 but is known to fail for train_2. The correct general rule remains undetermined from the provided examples.
4.  **Find First Occurrence:** Retrieve the pre-recorded location of the first occurrence for the selected Target Pattern (P_target).
5.  **Extract Output:** Return the HxW subgrid from the input grid starting at the location found in step 4.
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
         
    return tuple(map(tuple, grid))

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation based on finding a white template block,
    identifying candidate patterns without white pixels, selecting one based
    on the k vs H*W rule, and finding its first occurrence.
    """
    input_array = np.array(input_grid, dtype=int)
    grid_h, grid_w = input_array.shape

    # 1. Find the white block bounding box to get template H and W
    white_bbox = find_color_bbox(input_array, 0)
    if white_bbox is None:
        # No white block found, cannot determine template size.
        return [] # Return empty list for failure/ambiguity
        
    _, _, h, w = white_bbox # Template height and width

    # Check if template size is valid
    if h <= 0 or w <= 0 or h > grid_h or w > grid_w:
         return []

    # 2. Identify unique candidate patterns (no white pixels) and their first occurrences
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

    # 3. Select Target Pattern using the k vs H*W rule
    candidate_patterns = list(pattern_first_occurrence.keys())
    k = len(candidate_patterns)
    hw = h * w

    # Sort the patterns lexicographically to apply the rule
    sorted_patterns = sorted(candidate_patterns)
    
    target_pattern_key = None
    if k == hw:
        # Rule: If k == H*W, select the lexicographically smallest
        target_pattern_key = sorted_patterns[0]
    else:
        # Rule: If k != H*W, select the lexicographically largest
        target_pattern_key = sorted_patterns[-1]
        
    # Check if a target was actually selected (should always happen if candidates exist)
    if target_pattern_key is None:
         return []

    # 4. Find First Occurrence location (already stored)
    # Retrieve the location where the target pattern *first* appeared.
    try:
        first_occurrence_r, first_occurrence_c = pattern_first_occurrence[target_pattern_key]
    except KeyError:
         # This should not happen if target_pattern_key came from the dictionary keys
         return [] 

    # 5. Extract and return the subgrid found at that first occurrence location.
    output_array = extract_subgrid(input_array, first_occurrence_r, first_occurrence_c, h, w)
    
    # Convert the numpy array back to a list of lists for the final output
    return output_array.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 6 0 6
6 8 6 8
8 6 8 6
6 8 6 8
```
Expected Output:
```
8
```
Transformed Output:
```
8
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
2 1 2 1 2
1 1 1 1 1
2 1 2 1 2
0 0 1 1 1
0 0 2 1 2
```
Expected Output:
```
1 1
2 1
```
Transformed Output:
```
1 1
1 2
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 50.0

## Example 3:
Input:
```
2 2 5 2 2 5 2
2 2 5 2 2 5 2
5 5 5 5 5 5 5
2 2 5 2 2 5 2
2 2 5 2 2 5 2
5 5 5 5 5 0 0
2 2 5 2 2 0 0
```
Expected Output:
```
5 5
5 2
```
Transformed Output:
```
5 5
5 2
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
