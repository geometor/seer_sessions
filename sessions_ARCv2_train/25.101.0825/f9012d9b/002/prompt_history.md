
## train_1

**input:**
```
8 6 0 6
6 8 6 8
8 6 8 6
6 8 6 8
```


**output:**
```
8
```


## train_2

**input:**
```
2 1 2 1 2
1 1 1 1 1
2 1 2 1 2
0 0 1 1 1
0 0 2 1 2
```


**output:**
```
1 1
2 1
```


## train_3

**input:**
```
2 2 5 2 2 5 2
2 2 5 2 2 5 2
5 5 5 5 5 5 5
2 2 5 2 2 5 2
2 2 5 2 2 5 2
5 5 5 5 5 0 0
2 2 5 2 2 0 0
```


**output:**
```
5 5
5 2
```

## Perception

The task involves identifying a specific subgrid within a larger input grid and outputting that subgrid. The key seems to lie in using the block of white pixels (color 0) present in the input grid.

1.  **Identifying the Template Size:** The input grid contains a distinct region composed solely of white pixels (value 0). The dimensions (height H, width W) of the bounding box of these white pixels define the size of the subgrid we are looking for.
2.  **Identifying the Target Pattern:** The output grid corresponds to a subgrid of size HxW found within the input grid. This target subgrid is *not* the block of white pixels itself.
3.  **Selection Rule:** The crucial step is determining *which* HxW subgrid (that isn't the white block) is the correct output.
    *   In `train_1`, the white block is 1x1. The output `8` is the first non-white 1x1 subgrid encountered when scanning the input top-to-bottom, left-to-right.
    *   In `train_2`, the white block is 2x2. The output pattern `1 1 / 2 1` occurs multiple times in the input. The instance chosen is the one that appears first in reading order (`input[1:3, 2:4]`).
    *   In `train_3`, the white block is 2x2. The output pattern `5 5 / 5 2` occurs multiple times. The instance chosen is the one that appears first in reading order (`input[2:4, 0:2]`).
    *   The challenge lies in identifying *which pattern* (`8` in train_1, `1 1 / 2 1` in train_2, `5 5 / 5 2` in train_3) is the target pattern *before* finding its first occurrence. The rule for selecting the target pattern is not immediately obvious (e.g., it's not simply the first HxW block encountered, nor the most frequent). However, once the target pattern is identified, the rule seems to be "output the first occurrence of this pattern".

## Facts


```yaml
task_elements:
  - Input Grid: A 2D array of pixels (integers 0-9).
  - White Block: A contiguous rectangular subgrid within the input grid consisting solely of white pixels (value 0).
  - Output Grid: A 2D array of pixels, representing a subgrid extracted from the input grid.

properties:
  - White Block defines Template Size:
      object: White Block
      property: dimensions (height H, width W)
      role: Defines the dimensions of the target Output Grid.
  - Output Grid is an Input Subgrid:
      object: Output Grid
      property: content
      relationship: Is identical to a specific HxW subgrid found within the Input Grid.
  - Output Grid is not the White Block:
      object: Output Grid
      relationship: Is distinct from the White Block found in the Input Grid.
  - Selection Ambiguity:
      property: Target Pattern Selection
      description: The specific HxW pattern chosen as the Output Grid is not determined by simple rules like 'first encountered', 'most frequent', 'at (0,0)', etc. based on the provided examples.
  - First Occurrence Rule:
      property: Output Grid Location
      description: Once the correct target pattern P (of size HxW) is identified, the Output Grid corresponds to the first instance of P found when scanning the Input Grid top-to-bottom, left-to-right.

derived_facts:
  - Template Height (H): Determined by the height of the White Block's bounding box.
  - Template Width (W): Determined by the width of the White Block's bounding box.

example_specific_facts:
  - train_1:
      White Block: 1x1 at (0, 2). H=1, W=1.
      Target Pattern: 8.
      Output Location: (0, 0). (First occurrence of '8').
  - train_2:
      White Block: 2x2 at (3, 0). H=2, W=2.
      Target Pattern: [[1, 1], [2, 1]].
      Output Location: (1, 2). (First occurrence of the target pattern).
  - train_3:
      White Block: 2x2 at (5, 5). H=2, W=2.
      Target Pattern: [[5, 5], [5, 2]].
      Output Location: (2, 0). (First occurrence of the target pattern).

```


## Natural Language Program

1.  Identify the rectangular bounding box encompassing all white (0) pixels in the input grid. Determine its height (H) and width (W).
2.  Identify the specific HxW pattern (P_target) that constitutes the output grid based on a currently undetermined selection rule (this rule needs further refinement based on more examples or insights, as simple frequency or positional rules fail).
3.  Scan the input grid from top-to-bottom, then left-to-right, examining all possible HxW subgrids.
4.  Find the first subgrid encountered during the scan whose pixel pattern exactly matches the identified target pattern (P_target).
5.  Return this first matching subgrid as the output grid.
```python
import numpy as np
from typing import List, Tuple, Optional, Dict

"""
Transformation Rule Natural Language Description:

1. Identify the rectangular bounding box encompassing all white (0) pixels in the input grid. Determine its height (H) and width (W). This defines the template size.
2. Identify a specific target HxW pattern (P_target) from the input grid. This pattern is not the all-white pattern. (The rule for selecting P_target from multiple candidate patterns is not definitively determined from the provided examples).
3. Scan the input grid from top-to-bottom, then left-to-right, examining all possible HxW subgrids.
4. Find the first subgrid encountered during the scan whose pixel pattern exactly matches the identified target pattern (P_target).
5. Return this first matching subgrid as the output grid.

NOTE: The implementation below uses a placeholder rule for step 2 ('select the non-white pattern whose first occurrence is top-leftmost'), which is known to be incorrect for some examples (train_2, train_3). The correct selection rule remains elusive based solely on the provided training data.
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
    return min_row, min_col, height, width

# Helper function to extract a subgrid
def extract_subgrid(grid: np.ndarray, r: int, c: int, h: int, w: int) -> np.ndarray:
    """Extracts a subgrid of size h x w starting at (r, c)."""
    # Ensure bounds are valid before slicing
    if r + h > grid.shape[0] or c + w > grid.shape[1]:
        # This case should ideally not be reached if loops are correct
        return np.array([[]]) 
    return grid[r:r+h, c:c+w]

# Helper function to check if a grid contains only a specific color
def is_solid_color(grid: np.ndarray, color: int) -> bool:
    """Checks if all elements in the grid are equal to the given color."""
    if grid.size == 0: # Handle empty subgrids if they occur
        return False
    return np.all(grid == color)

# Helper function to convert numpy array to tuple for dict keys
def grid_to_tuple(grid: np.ndarray) -> tuple:
    """Converts a numpy array (grid) to a hashable tuple of tuples."""
    return tuple(map(tuple, grid))

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation based on finding a white template block,
    identifying a target pattern based on that block's size using a placeholder rule, 
    and finding the first occurrence of that target pattern.
    """
    input_array = np.array(input_grid, dtype=int)
    grid_h, grid_w = input_array.shape

    # 1. Find the white block bounding box to get template H and W
    # Assumes white is color 0
    white_bbox = find_color_bbox(input_array, 0)
    if white_bbox is None:
        # No white block found, cannot determine template size.
        # Return empty list as per ARC conventions for failure/ambiguity.
        return [] 
        
    _, _, h, w = white_bbox # Template height and width

    # Check if template size is valid
    if h <= 0 or w <= 0:
         return []

    # --- Start: Step 2 - Identify Target Pattern (P_target) ---
    # This is the step where the rule is ambiguous based on examples.
    # First, find all unique non-white patterns of size HxW and their first occurrence location.
    
    pattern_first_occurrence: Dict[tuple, Tuple[int, int]] = {}

    # Iterate through all possible top-left corners for subgrids of size HxW
    for r in range(grid_h - h + 1):
        for c in range(grid_w - w + 1):
            subgrid = extract_subgrid(input_array, r, c, h, w)
            
            # Skip if it's the all-white pattern (color 0)
            if is_solid_color(subgrid, 0):
                continue
                
            # Use a tuple representation of the subgrid as a dictionary key
            pattern_key = grid_to_tuple(subgrid)
            
            # Record the first time (top-leftmost location) we encounter this pattern
            if pattern_key not in pattern_first_occurrence:
                pattern_first_occurrence[pattern_key] = (r, c)

    # If no non-white patterns of the required size were found
    if not pattern_first_occurrence:
         return []

    # Placeholder Rule for selecting P_target: Choose the pattern whose first
    # occurrence location (r, c) is minimal (first by row `r`, then by column `c`).
    # WARNING: This rule is derived from analysis but fails on train_2 and train_3.
    # The correct rule for choosing among the patterns in `pattern_first_occurrence`
    # is the core unknown element of this task based on provided examples.
    
    target_pattern_key = None
    # Find the pattern associated with the minimum (r, c) first occurrence
    # Sorting the locations and taking the first gives the minimum (top-leftmost)
    min_first_occurrence_loc = min(pattern_first_occurrence.values())
    
    # Find the pattern key that corresponds to this minimum location
    for pattern, loc in pattern_first_occurrence.items():
        if loc == min_first_occurrence_loc:
            target_pattern_key = pattern
            break # Found the pattern corresponding to the top-leftmost first occurrence

    # If somehow no target pattern identified (should not happen if pattern_first_occurrence is populated)
    if target_pattern_key is None:
        return []

    # --- End: Step 2 ---

    # 3 & 4. Scan the grid again (conceptually) to find the first occurrence of the selected P_target.
    # Since we already stored the first occurrence location for each unique pattern,
    # we can retrieve the stored location for the chosen `target_pattern_key`.
    
    # Retrieve the location where the target pattern *first* appeared.
    first_occurrence_r, first_occurrence_c = pattern_first_occurrence[target_pattern_key]
    
    # 5. Extract and return the subgrid found at that first occurrence location.
    # Note: Under the placeholder rule, the output is simply the pattern whose own
    # first occurrence was top-leftmost, extracted from that top-leftmost location.
    output_array = extract_subgrid(input_array, first_occurrence_r, first_occurrence_c, h, w)
    
    # Convert the numpy array back to a list of lists for the final output
    return output_array.tolist()
```
