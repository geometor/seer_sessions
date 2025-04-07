```python
import numpy as np
from typing import List, Tuple, Optional, Dict
from collections import Counter

"""
Transformation Rule:
1. Identify vertical columns spanning the full grid height composed of a single uniform color. These are potential 'separators'.
2. Filter out potential separators whose color is the most frequent color in the entire grid (assumed to be the background color).
3. If no separators remain after filtering, the output is an empty grid with the same height as the input.
4. Assume all remaining valid separators share the same color. Identify this separator color and the indices of all columns with this color.
5. If the separator color is red (2):
   - Select the index of the rightmost separator column.
   - Extract the portion of the grid strictly to the right of this column.
   - If the rightmost separator is the last column, the output is an empty grid.
6. If the separator color is not red:
   - Select the index of the leftmost separator column.
   - Extract the portion of the grid strictly to the left of this column.
   - If the leftmost separator is the first column (index 0), the output is an empty grid.
7. Represent empty grids (0 width) as a list of empty lists, one for each row of the original grid's height.
"""

def find_true_separators(grid: np.ndarray) -> Tuple[Optional[List[int]], Optional[int]]:
    """
    Finds valid separator columns, filtering out the background color.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple containing:
        - A list of indices of the valid separator columns, or None if none found.
        - The uniform color of the separator columns, or None if none found.
          Assumes all valid separators in a grid share the same color.
    """
    height, width = grid.shape
    
    # Handle empty grid edge case
    if height == 0 or width == 0:
        return None, None

    # 1. Identify all potential separators (full-height, uniform color columns)
    potential_separators: Dict[int, List[int]] = {} # color -> list of indices
    for c in range(width):
        column = grid[:, c]
        if np.all(column == column[0]):
            color = column[0]
            if color not in potential_separators:
                potential_separators[color] = []
            potential_separators[color].append(c)

    if not potential_separators:
        return None, None # No uniform columns found at all

    # 2. Determine the most frequent color (background)
    # Ensure grid is not empty before counting
    if grid.size == 0:
         # Should not happen if height/width checks passed, but defensive check
         background_color = -1 # Assign a value that won't match any separator
    else:
        color_counts = Counter(grid.flatten())
        # Find the color with the maximum count. If ties, Counter picks one.
        background_color = color_counts.most_common(1)[0][0]

    # 3. Filter out separators matching the background color
    valid_separator_colors = list(potential_separators.keys())
    for color in list(valid_separator_colors): # Iterate over a copy for safe removal
        if color == background_color:
            valid_separator_colors.remove(color)
            del potential_separators[color] # Remove from the main dict too

    # 4. Check results and determine final separator color/indices
    if not valid_separator_colors:
        return None, None # No non-background separators found

    # Assumption: Only one separator color remains after filtering background
    # If multiple non-background uniform colors exist, this logic might need refinement,
    # but based on examples, we expect only one relevant separator type per grid.
    separator_color = valid_separator_colors[0]
    separator_indices = sorted(potential_separators[separator_color])

    return separator_indices, separator_color


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on vertical separator lines, extracting
    a subgrid to the left or right depending on the separator color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array
    grid_np = np.array(input_grid, dtype=int)

    # Handle edge case: If input is completely empty ([]) return []
    if not input_grid:
        return []
        
    # Handle edge case: Input like [[], [], ...]
    # numpy array shape will be (height, 0)
    if grid_np.ndim == 1 and len(input_grid) > 0: # Handles cases like [[], []] -> array([]) incorrect shape
         height = len(input_grid)
         width = 0
         grid_np = np.empty((height, 0), dtype=int) # Ensure correct shape (h, 0)
    elif grid_np.size == 0 and grid_np.ndim == 2: # Handles cases like np.array([[]]) -> shape (1,0)
         height = grid_np.shape[0]
         width = grid_np.shape[1]
    elif grid_np.ndim < 2: # Handles 1D or 0D arrays inappropriately formed
         # This case indicates malformed input based on ARC constraints
         # Defaulting to returning an empty list of lists based on input structure
         if isinstance(input_grid[0], list):
             height = len(input_grid)
             return [[] for _ in range(height)]
         else: # Input was like [1, 2, 3] - not a grid
             return [] # Or raise error? Let's return empty list.
    else:
         height, width = grid_np.shape


    # Find valid separator columns and their color (filtering background)
    separator_indices, separator_color = find_true_separators(grid_np)

    # Handle No Separators: If no valid separators are found, return empty grid
    if separator_indices is None:
        # Create a list of empty lists, one for each row
        return [[] for _ in range(height)]

    # Initialize output grid variable
    output_grid_np = None

    # Select Relevant Separator Index and Extract Subgrid based on color
    if separator_color == 2:  # Red separator
        # Find the index of the rightmost separator column.
        relevant_index = max(separator_indices)
        # Define the starting column for the slice (strictly after the separator).
        start_col = relevant_index + 1
        # Extract the portion to the right.
        if start_col < width:
            output_grid_np = grid_np[:, start_col:]
        else:
            # If the rightmost separator is the last column, the output is empty.
            output_grid_np = np.empty((height, 0), dtype=int)

    else:  # Separator color is NOT red
        # Find the index of the leftmost separator column.
        relevant_index = min(separator_indices)
        # Define the ending column for the slice (strictly before the separator).
        end_col = relevant_index
        # Extract the portion to the left.
        if end_col > 0:
            output_grid_np = grid_np[:, :end_col]
        else:
            # If the leftmost separator is the first column (index 0), the output is empty.
            output_grid_np = np.empty((height, 0), dtype=int)

    # Convert the resulting numpy array back to a list of lists
    # np.tolist() correctly handles (h, 0) arrays, returning [[]]*h
    output_grid = output_grid_np.tolist()

    return output_grid
```