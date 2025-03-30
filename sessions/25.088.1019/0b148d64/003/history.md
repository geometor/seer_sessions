
Previous Code:
```python
import numpy as np
from typing import List, Tuple, Optional

"""
Identifies the bottom-most contiguous block of non-background (non-zero) pixels 
in the input grid, where blocks are separated by horizontal rows consisting 
entirely of the background color (0). The transformation extracts the bounding 
box of this bottom-most block.

1. Scan the input grid from bottom to top to find the index of the last row 
   containing any non-background pixel. This is the bottom edge of the target region.
2. Scan from this bottom edge row upwards to find the index of the first row 
   encountered that consists entirely of the background color (0). The row below 
   this separator row is the top edge of the target region. If no separator row 
   is found above the bottom edge, the top edge is the first row (index 0) of 
   the grid.
3. Within the identified rows (from top edge to bottom edge, inclusive), find the 
   minimum and maximum column indices that contain a non-background pixel across 
   any of these rows. These are the left and right edges of the target region.
4. Extract the subgrid defined by these row and column boundaries.
"""

def find_last_non_background_row(grid: np.ndarray, background_color: int = 0) -> Optional[int]:
    """
    Finds the index of the last row containing any non-background pixels.
    Scans from bottom to top. Returns None if the grid is empty or all background.
    """
    height = grid.shape[0]
    for r in range(height - 1, -1, -1):
        if np.any(grid[r] != background_color):
            return r
    return None

def find_last_all_background_row_before(grid: np.ndarray, end_row_index: int, background_color: int = 0) -> Optional[int]:
    """
    Finds the index of the last row consisting entirely of background_color,
    searching upwards from (but not including) end_row_index down to row 0.
    Returns None if no such row is found.
    """
    for r in range(end_row_index - 1, -1, -1):
        if np.all(grid[r] == background_color):
            return r
    return None

def find_column_bounds(grid: np.ndarray, start_row: int, end_row: int, background_color: int = 0) -> Optional[Tuple[int, int]]:
    """
    Finds the minimum and maximum column indices containing non-background pixels
    within the specified row range (inclusive).
    Returns None if no non-background pixels are found in the range.
    """
    min_col = grid.shape[1]
    max_col = -1
    found_non_bg = False

    for r in range(start_row, end_row + 1):
        non_bg_indices = np.where(grid[r] != background_color)[0]
        if non_bg_indices.size > 0:
            found_non_bg = True
            current_min = np.min(non_bg_indices)
            current_max = np.max(non_bg_indices)
            min_col = min(min_col, current_min)
            max_col = max(max_col, current_max)

    if not found_non_bg:
        return None
    return min_col, max_col


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Extracts the bottom-most non-background region from the input grid.
    
    Args:
        input_grid: A list of lists representing the input grid.
        
    Returns:
        A list of lists representing the extracted subgrid (the bottom region).
    """
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    background_color = 0
    height, width = grid.shape

    if height == 0 or width == 0:
        return [] # Handle empty input

    # 1. Find the bottom row index of the target region
    last_row = find_last_non_background_row(grid, background_color)
    
    # If no non-background pixels exist anywhere, return empty grid
    if last_row is None:
        return [] 

    # 2. Find the top row index of the target region
    # Scan upwards from the last_row to find the first all-background separator row
    separator_row = find_last_all_background_row_before(grid, last_row, background_color)

    # The target region starts the row *after* the separator, or row 0 if no separator found
    first_row = 0 if separator_row is None else separator_row + 1
        
    # 3. Find the column bounds (left and right edges) within the target rows
    col_bounds = find_column_bounds(grid, first_row, last_row, background_color)
    
    # This check might be redundant if last_row was found, but good practice
    if col_bounds is None:
        # This case should ideally not be reached if last_row is not None,
        # but handles potential edge cases or empty regions between separators.
        # Let's return an empty grid or the single row/column if that makes sense.
        # Based on examples, an empty result is unlikely if a non-bg row was found.
        # If last_row exists, there must be columns.
         return [] # Or potentially handle differently if needed.
        
    first_col, last_col = col_bounds

    # 4. Extract the subgrid using numpy slicing
    output_grid_np = grid[first_row : last_row + 1, first_col : last_col + 1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 0 2 2 2 2 0 0 0 0 2 0 2 2 2 2 0 0 2
2 2 2 2 0 2 2 0 0 0 0 2 2 2 2 2 0 0 0
0 0 2 2 0 2 0 0 0 0 2 2 2 0 2 2 2 2 2
2 0 2 0 2 2 0 0 0 0 0 2 2 2 2 2 2 0 0
0 2 0 2 2 2 2 0 0 0 0 0 0 2 2 0 2 2 2
2 2 2 0 2 0 2 0 0 0 2 0 2 2 2 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 0 0 2 0 0 0 0 3 3 3 3 3 0 3 3
0 2 2 0 0 2 2 0 0 0 3 3 3 0 0 0 3 3 0
0 2 2 0 0 2 0 0 0 0 3 3 3 0 3 0 3 0 0
2 2 2 0 0 2 2 0 0 0 3 3 0 0 0 3 3 3 3
2 0 0 2 2 2 0 0 0 0 3 0 0 0 3 0 3 0 3
2 0 2 0 0 0 2 0 0 0 0 3 3 0 3 3 3 0 3
0 2 2 0 2 2 0 0 0 0 0 3 3 0 0 3 0 3 0
```
Expected Output:
```
0 3 3 3 3 3 0 3 3
3 3 3 0 0 0 3 3 0
3 3 3 0 3 0 3 0 0
3 3 0 0 0 3 3 3 3
3 0 0 0 3 0 3 0 3
0 3 3 0 3 3 3 0 3
0 3 3 0 0 3 0 3 0
```
Transformed Output:
```
2 0 2 0 0 0 2 0 0 0 0 3 3 3 3 3 0 3 3
0 2 2 0 0 2 2 0 0 0 3 3 3 0 0 0 3 3 0
0 2 2 0 0 2 0 0 0 0 3 3 3 0 3 0 3 0 0
2 2 2 0 0 2 2 0 0 0 3 3 0 0 0 3 3 3 3
2 0 0 2 2 2 0 0 0 0 3 0 0 0 3 0 3 0 3
2 0 2 0 0 0 2 0 0 0 0 3 3 0 3 3 3 0 3
0 2 2 0 2 2 0 0 0 0 0 3 3 0 0 3 0 3 0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None

## Example 2:
Input:
```
8 8 8 8 8 0 8 8 8 8 0 0 0 0 8 8 8 8 0 8 8
8 0 0 8 0 8 0 8 8 8 0 0 0 0 8 8 8 0 0 0 8
8 8 8 0 0 0 8 8 8 8 0 0 0 0 8 8 0 8 8 8 8
8 8 0 8 8 8 8 0 8 8 0 0 0 0 8 8 0 0 0 8 8
8 8 8 8 0 8 8 0 8 8 0 0 0 0 8 8 8 0 8 8 8
0 0 0 8 8 0 8 0 0 8 0 0 0 0 8 0 0 0 8 0 0
8 8 8 8 0 0 8 0 8 0 0 0 0 0 8 8 8 0 8 8 8
8 0 0 8 0 0 8 8 0 8 0 0 0 0 8 0 8 8 8 8 8
8 8 8 8 8 8 0 8 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 2 0 0 0 0 8 8 0 8 8 0 8
2 0 2 2 2 0 0 2 2 2 0 0 0 0 8 8 8 8 0 8 0
0 2 2 2 2 2 2 0 2 0 0 0 0 0 8 8 8 0 0 0 8
2 2 2 2 0 2 2 2 2 2 0 0 0 0 8 8 0 8 8 8 0
2 2 2 2 2 2 0 2 0 0 0 0 0 0 8 8 8 8 8 0 0
2 2 2 2 2 0 2 0 2 2 0 0 0 0 8 0 8 0 8 8 8
2 2 0 2 2 0 0 0 0 0 0 0 0 0 8 8 0 8 0 0 8
0 2 2 0 0 2 2 0 0 2 0 0 0 0 8 0 0 0 8 8 0
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 8 8 0 0 8 8
2 0 2 2 0 2 2 2 2 2 0 0 0 0 8 8 8 0 8 8 8
```
Expected Output:
```
0 2 2 2 0 0 2 2 2 2
2 0 2 2 2 0 0 2 2 2
0 2 2 2 2 2 2 0 2 0
2 2 2 2 0 2 2 2 2 2
2 2 2 2 2 2 0 2 0 0
2 2 2 2 2 0 2 0 2 2
2 2 0 2 2 0 0 0 0 0
0 2 2 0 0 2 2 0 0 2
2 2 2 2 2 2 2 2 2 2
2 0 2 2 0 2 2 2 2 2
```
Transformed Output:
```
0 2 2 2 0 0 2 2 2 2 0 0 0 0 8 8 0 8 8 0 8
2 0 2 2 2 0 0 2 2 2 0 0 0 0 8 8 8 8 0 8 0
0 2 2 2 2 2 2 0 2 0 0 0 0 0 8 8 8 0 0 0 8
2 2 2 2 0 2 2 2 2 2 0 0 0 0 8 8 0 8 8 8 0
2 2 2 2 2 2 0 2 0 0 0 0 0 0 8 8 8 8 8 0 0
2 2 2 2 2 0 2 0 2 2 0 0 0 0 8 0 8 0 8 8 8
2 2 0 2 2 0 0 0 0 0 0 0 0 0 8 8 0 8 0 0 8
0 2 2 0 0 2 2 0 0 2 0 0 0 0 8 0 0 0 8 8 0
2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 8 8 0 0 8 8
2 0 2 2 0 2 2 2 2 2 0 0 0 0 8 8 8 0 8 8 8
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None

## Example 3:
Input:
```
0 1 0 1 1 1 0 0 1 1 0 1 0 0 0 0 0
1 0 1 0 0 0 0 0 1 1 1 1 1 1 0 1 1
1 1 0 1 1 0 0 0 1 1 1 1 1 1 0 1 1
1 1 0 0 1 1 0 0 1 1 0 1 1 1 1 1 1
0 1 1 1 0 0 0 0 1 1 0 0 0 1 1 1 0
1 0 0 1 0 0 0 0 1 1 0 0 1 1 1 1 1
0 0 0 1 1 0 0 0 1 1 1 0 0 1 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 0 0 4 0 4 0 0 1 0 0 1 1 1 1 1 1
4 4 4 4 0 4 0 0 1 0 1 1 1 1 1 1 0
4 0 4 0 0 4 0 0 0 1 0 0 1 1 1 1 1
0 4 4 4 4 0 0 0 1 1 0 0 1 0 1 0 1
4 4 4 0 4 4 0 0 1 1 1 1 1 1 1 1 0
0 4 4 4 4 0 0 0 0 1 0 0 0 0 1 1 1
0 4 4 4 0 4 0 0 0 1 0 1 0 1 1 1 0
0 4 0 0 0 0 0 0 1 0 1 1 1 0 1 0 1
4 4 0 4 0 4 0 0 1 1 1 0 0 1 1 1 0
```
Expected Output:
```
4 0 0 4 0 4
4 4 4 4 0 4
4 0 4 0 0 4
0 4 4 4 4 0
4 4 4 0 4 4
0 4 4 4 4 0
0 4 4 4 0 4
0 4 0 0 0 0
4 4 0 4 0 4
```
Transformed Output:
```
4 0 0 4 0 4 0 0 1 0 0 1 1 1 1 1 1
4 4 4 4 0 4 0 0 1 0 1 1 1 1 1 1 0
4 0 4 0 0 4 0 0 0 1 0 0 1 1 1 1 1
0 4 4 4 4 0 0 0 1 1 0 0 1 0 1 0 1
4 4 4 0 4 4 0 0 1 1 1 1 1 1 1 1 0
0 4 4 4 4 0 0 0 0 1 0 0 0 0 1 1 1
0 4 4 4 0 4 0 0 0 1 0 1 0 1 1 1 0
0 4 0 0 0 0 0 0 1 0 1 1 1 0 1 0 1
4 4 0 4 0 4 0 0 1 1 1 0 0 1 1 1 0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: False
Color Count Correct: False
Score: None
## General Assessment

The previous transformation attempt correctly identified the concept of a "bottom-most block" separated by white rows. However, it extracted the entire bounding box of *all* non-white pixels within that block. The results clearly show that the expected output is a sub-region of that block, specifically the bounding box containing only *certain* colors within that block.

The key insight missed was how to select the relevant color(s) whose bounding box should be extracted from the bottom block. Analysis of the three examples suggests a relationship between the colors in the block *above* the separator row and the colors in the block *below* it. The target color for extraction appears to be the color(s) present in the bottom block but *absent* from the block immediately above the separator.

The strategy is to:
1.  Precisely define and locate the "bottom block" and the "block above" based on the last all-white separator row.
2.  Identify the unique non-white colors in each of these two blocks.
3.  Determine the "target color(s)" by finding colors unique to the bottom block compared to the block above.
4.  Calculate the minimal bounding box enclosing only the pixels of the target color(s) within the vertical extent of the bottom block.
5.  Extract this specific bounding box from the input grid.

## Metrics Gathering

Let's verify the separator rows, block definitions, and color sets for each example. We define white = 0.



*code_execution:*
```python
import numpy as np

def analyze_example(input_grid_list):
    grid = np.array(input_grid_list, dtype=int)
    height, width = grid.shape
    background_color = 0
    metrics = {}
    metrics['input_shape'] = (height, width)

    # 1. Find last non-background row
    last_row = -1
    for r in range(height - 1, -1, -1):
        if np.any(grid[r] != background_color):
            last_row = r
            break
    metrics['last_non_bg_row'] = last_row
    if last_row == -1:
        metrics['error'] = "Grid is all background"
        return metrics

    # 2. Find last all-background separator row before last_row
    separator_row = -1
    for r in range(last_row - 1, -1, -1):
        if np.all(grid[r] == background_color):
            separator_row = r
            break
    metrics['separator_row'] = separator_row

    # 3. Define blocks
    bottom_block_start_row = separator_row + 1
    bottom_block_end_row = last_row
    top_block_start_row = 0
    top_block_end_row = separator_row -1 # will be -1 if separator_row is 0 or -1

    metrics['bottom_block_rows'] = (bottom_block_start_row, bottom_block_end_row)

    # 4. Colors in top block (above separator row + 1)
    top_colors = set()
    if separator_row >= 0:
       top_block = grid[top_block_start_row : separator_row + 1]
       if top_block.size > 0:
           unique_top = np.unique(top_block)
           top_colors = set(unique_top[unique_top != background_color])
    metrics['top_block_colors'] = top_colors

    # 5. Colors in bottom block
    bottom_block = grid[bottom_block_start_row : bottom_block_end_row + 1]
    bottom_colors = set()
    if bottom_block.size > 0:
        unique_bottom = np.unique(bottom_block)
        bottom_colors = set(unique_bottom[unique_bottom != background_color])
    metrics['bottom_block_colors'] = bottom_colors

    # 6. Target colors
    target_colors = bottom_colors - top_colors
    metrics['target_colors'] = target_colors

    # 7. Bounding box of target colors in bottom block
    min_r, max_r = bottom_block_start_row, bottom_block_end_row
    min_c, max_c = width, -1
    found_target = False
    for r in range(min_r, max_r + 1):
        for c in range(width):
            if grid[r, c] in target_colors:
                found_target = True
                min_c = min(min_c, c)
                max_c = max(max_c, c)

    if found_target:
        metrics['target_bounding_box'] = {
            'rows': (min_r, max_r),
            'cols': (min_c, max_c)
        }
        metrics['output_shape'] = (max_r - min_r + 1, max_c - min_c + 1)
    else:
         metrics['target_bounding_box'] = None
         metrics['output_shape'] = (0, 0) # Or indicate error/empty

    return metrics

# Example 1 Input
ex1_input = [
    [2,0,2,2,2,2,0,0,0,0,2,0,2,2,2,2,0,0,2],
    [2,2,2,2,0,2,2,0,0,0,0,2,2,2,2,2,0,0,0],
    [0,0,2,2,0,2,0,0,0,0,2,2,2,0,2,2,2,2,2],
    [2,0,2,0,2,2,0,0,0,0,0,2,2,2,2,2,2,0,0],
    [0,2,0,2,2,2,2,0,0,0,0,0,0,2,2,0,2,2,2],
    [2,2,2,0,2,0,2,0,0,0,2,0,2,2,2,2,0,2,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # separator_row = 10
    [2,0,2,0,0,0,2,0,0,0,0,3,3,3,3,3,0,3,3], # bottom_block starts row 11
    [0,2,2,0,0,2,2,0,0,0,3,3,3,0,0,0,3,3,0],
    [0,2,2,0,0,2,0,0,0,0,3,3,3,0,3,0,3,0,0],
    [2,2,2,0,0,2,2,0,0,0,3,3,0,0,0,3,3,3,3],
    [2,0,0,2,2,2,0,0,0,0,3,0,0,0,3,0,3,0,3],
    [2,0,2,0,0,0,2,0,0,0,0,3,3,0,3,3,3,0,3],
    [0,2,2,0,2,2,0,0,0,0,0,3,3,0,0,3,0,3,0]  # last_non_bg_row = 17
]
ex1_metrics = analyze_example(ex1_input)
print("--- Example 1 Metrics ---")
print(ex1_metrics)

# Example 2 Input
ex2_input = [
    [8,8,8,8,8,0,8,8,8,8,0,0,0,0,8,8,8,8,0,8,8],
    [8,0,0,8,0,8,0,8,8,8,0,0,0,0,8,8,8,0,0,0,8],
    [8,8,8,0,0,0,8,8,8,8,0,0,0,0,8,8,0,8,8,8,8],
    [8,8,0,8,8,8,8,0,8,8,0,0,0,0,8,8,0,0,0,8,8],
    [8,8,8,8,0,8,8,0,8,8,0,0,0,0,8,8,8,0,8,8,8],
    [0,0,0,8,8,0,8,0,0,8,0,0,0,0,8,0,0,0,8,0,0],
    [8,8,8,8,0,0,8,0,8,0,0,0,0,0,8,8,8,0,8,8,8],
    [8,0,0,8,0,0,8,8,0,8,0,0,0,0,8,0,8,8,8,8,8],
    [8,8,8,8,8,8,0,8,0,0,0,0,0,0,8,8,8,8,8,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # separator_row = 10
    [0,2,2,2,0,0,2,2,2,2,0,0,0,0,8,8,0,8,8,0,8], # bottom_block starts row 11
    [2,0,2,2,2,0,0,2,2,2,0,0,0,0,8,8,8,8,0,8,0],
    [0,2,2,2,2,2,2,0,2,0,0,0,0,0,8,8,8,0,0,0,8],
    [2,2,2,2,0,2,2,2,2,2,0,0,0,0,8,8,0,8,8,8,0],
    [2,2,2,2,2,2,0,2,0,0,0,0,0,0,8,8,8,8,8,0,0],
    [2,2,2,2,2,0,2,0,2,2,0,0,0,0,8,0,8,0,8,8,8],
    [2,2,0,2,2,0,0,0,0,0,0,0,0,0,8,8,0,8,0,0,8],
    [0,2,2,0,0,2,2,0,0,2,0,0,0,0,8,0,0,0,8,8,0],
    [2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,8,8,0,0,8,8],
    [2,0,2,2,0,2,2,2,2,2,0,0,0,0,8,8,8,0,8,8,8]  # last_non_bg_row = 20
]
ex2_metrics = analyze_example(ex2_input)
print("\n--- Example 2 Metrics ---")
print(ex2_metrics)

# Example 3 Input
ex3_input = [
    [0,1,0,1,1,1,0,0,1,1,0,1,0,0,0,0,0],
    [1,0,1,0,0,0,0,0,1,1,1,1,1,1,0,1,1],
    [1,1,0,1,1,0,0,0,1,1,1,1,1,1,0,1,1],
    [1,1,0,0,1,1,0,0,1,1,0,1,1,1,1,1,1],
    [0,1,1,1,0,0,0,0,1,1,0,0,0,1,1,1,0],
    [1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,1,1],
    [0,0,0,1,1,0,0,0,1,1,1,0,0,1,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], # separator_row = 9
    [4,0,0,4,0,4,0,0,1,0,0,1,1,1,1,1,1], # bottom_block starts row 10
    [4,4,4,4,0,4,0,0,1,0,1,1,1,1,1,1,0],
    [4,0,4,0,0,4,0,0,0,1,0,0,1,1,1,1,1],
    [0,4,4,4,4,0,0,0,1,1,0,0,1,0,1,0,1],
    [4,4,4,0,4,4,0,0,1,1,1,1,1,1,1,1,0],
    [0,4,4,4,4,0,0,0,0,1,0,0,0,0,1,1,1],
    [0,4,4,4,0,4,0,0,0,1,0,1,0,1,1,1,0],
    [0,4,0,0,0,0,0,0,1,0,1,1,1,0,1,0,1],
    [4,4,0,4,0,4,0,0,1,1,1,0,0,1,1,1,0] # last_non_bg_row = 18
]
ex3_metrics = analyze_example(ex3_input)
print("\n--- Example 3 Metrics ---")
print(ex3_metrics)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Metrics ---
{'input_shape': (18, 19), 'last_non_bg_row': 17, 'separator_row': 10, 'bottom_block_rows': (11, 17), 'top_block_colors': {np.int64(2)}, 'bottom_block_colors': {np.int64(2), np.int64(3)}, 'target_colors': {np.int64(3)}, 'target_bounding_box': {'rows': (11, 17), 'cols': (10, 18)}, 'output_shape': (7, 9)}

--- Example 2 Metrics ---
{'input_shape': (21, 21), 'last_non_bg_row': 20, 'separator_row': 10, 'bottom_block_rows': (11, 20), 'top_block_colors': {np.int64(8)}, 'bottom_block_colors': {np.int64(8), np.int64(2)}, 'target_colors': {np.int64(2)}, 'target_bounding_box': {'rows': (11, 20), 'cols': (0, 9)}, 'output_shape': (10, 10)}

--- Example 3 Metrics ---
{'input_shape': (19, 17), 'last_non_bg_row': 18, 'separator_row': 9, 'bottom_block_rows': (10, 18), 'top_block_colors': {np.int64(1)}, 'bottom_block_colors': {np.int64(1), np.int64(4)}, 'target_colors': {np.int64(4)}, 'target_bounding_box': {'rows': (10, 18), 'cols': (0, 5)}, 'output_shape': (9, 6)}

```
The metrics calculated confirm the hypothesis:
- The separator row and bottom block rows are correctly identified.
- The `top_block_colors` and `bottom_block_colors` are correctly identified.
- The `target_colors` (bottom colors minus top colors) correctly isolate the color whose bounding box forms the output (Green=3, Red=2, Yellow=4 for examples 1, 2, 3 respectively).
- The calculated `target_bounding_box` rows and columns, and the resulting `output_shape`, match the dimensions of the `Expected Output` for each example.

## YAML Facts Documentation


```yaml
task_description: |-
  Extract a subgrid representing the bounding box of specific color(s) found only in the bottom-most horizontal region of the input grid, where regions are separated by rows of the background color (white, 0). The specific color(s) to extract are those present in the bottom region but not in the region immediately above it.

definitions:
  - background_color: 0 (white)
  - separator_row: A horizontal grid row consisting entirely of the background_color.
  - bottom_block: The contiguous set of rows from the row immediately following the last separator_row down to the last row containing any non-background color. If no separator_row exists, the bottom_block starts from the first row (index 0).
  - top_block: The contiguous set of rows from the first row (index 0) down to the last separator_row. If no separator_row exists, the top_block is considered empty.

grid_properties:
  - structure: Composed of potentially multiple horizontal blocks of non-background pixels separated by one or more separator_rows.
  - background: White (0) pixels separate distinct blocks vertically and can exist within blocks.

objects:
  - type: Color Region
    definition: A collection of pixels within a block sharing the same non-background color.
    properties:
      - color: The specific non-background color (1-9).
      - location: Resides within either the top_block or the bottom_block.
  - type: Target Color Region
    definition: A Color Region within the bottom_block whose color is not present in any Color Region within the top_block.
    properties:
      - color: The specific non-background color unique to the bottom_block relative to the top_block.
      - bounding_box: The minimum rectangle (defined by min/max row/col) enclosing all pixels of this color within the bottom_block's row range.

actions:
  - name: Identify Separator
    input: Input grid
    output: Index of the last row composed entirely of background_color that occurs *before* the last row containing any non-background color. Returns null/None/-1 if no such row exists.
  - name: Identify Blocks
    input: Input grid, Separator index
    output: Row ranges for top_block and bottom_block.
  - name: Identify Colors
    input: Input grid, Top block row range, Bottom block row range
    output: Set of unique non-background colors in top_block, Set of unique non-background colors in bottom_block.
  - name: Determine Target Colors
    input: Set of top_block colors, Set of bottom_block colors
    output: Set of colors present in bottom_block but not in top_block.
  - name: Find Target Bounding Box
    input: Input grid, Bottom block row range, Target color set
    output: Minimum and maximum row and column indices enclosing all pixels matching target colors within the bottom block's row range.
  - name: Extract Subgrid
    input: Input grid, Target bounding box (rows and columns)
    output: The portion of the input grid corresponding to the target bounding box.

constraints:
  - The output grid contains only pixels from the original input grid.
  - The output grid's rows correspond to the full vertical extent of the bottom_block.
  - The output grid's columns correspond to the minimal horizontal extent required to contain all pixels of the target color(s) within the bottom_block.
  - Assumes there will be at least one color unique to the bottom block compared to the top block in valid test cases matching the training pattern.
```


## Natural Language Program

1.  Define the background color as white (value 0).
2.  Scan the input grid from bottom to top to find the row index of the last row containing any non-background pixel. Let this be `last_row`. If no non-background pixels exist, return an empty grid.
3.  Scan downwards from `last_row - 1` to row 0 to find the index of the highest row that consists entirely of the background color. Let this be `separator_row`. If no such row exists, set `separator_row` to -1.
4.  Define the row range for the "bottom block" as `(separator_row + 1)` to `last_row`.
5.  Define the row range for the "top block" as row 0 to `separator_row`. If `separator_row` is -1, the top block is empty.
6.  Create a set of unique non-background colors found within the top block's rows (`top_colors`). If the top block is empty, this set is empty.
7.  Create a set of unique non-background colors found within the bottom block's rows (`bottom_colors`).
8.  Determine the set of `target_colors` by taking the colors in `bottom_colors` that are *not* present in `top_colors`.
9.  Initialize `min_target_col` to the grid width and `max_target_col` to -1.
10. Iterate through each row (`r`) from `separator_row + 1` to `last_row`, and each column (`c`) in that row:
    *   If the pixel `grid[r][c]` has a color that is in the `target_colors` set:
        *   Update `min_target_col = min(min_target_col, c)`.
        *   Update `max_target_col = max(max_target_col, c)`.
11. If `max_target_col` is still -1 (meaning no target colors were found, which shouldn't happen based on examples but is a safe check), return an empty grid.
12. Extract the subgrid from the input grid using the row range `separator_row + 1` to `last_row` (inclusive) and the column range `min_target_col` to `max_target_col` (inclusive).
13. Return the extracted subgrid.
