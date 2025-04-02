import numpy as np
from typing import List, Tuple, Optional, Dict
from collections import Counter

"""
Transformation Rule:
1. Analyze Input: Receive the input grid (a 2D array of color codes). Determine its height and width. Handle edge cases: If the input grid is entirely empty (`[]`) or has zero width (`[[], [], ...]`), return an empty list (`[]` or `[[], [], ...]`, matching the input structure's height for zero-width cases).
2. Identify Potential Separators: Iterate through each column of the grid. A column is a "potential separator" if it spans the full height of the grid and all pixels within that column have the same color. Keep track of these potential separators, noting their color and column index.
3. Determine Background Color: Calculate the frequency of each color across all pixels in the entire grid. The color with the highest frequency is the "background color". Handle empty grids gracefully.
4. Filter Separators: Remove any potential separators whose color matches the determined background color. The remaining ones are "valid separators".
5. Check for Valid Separators:
   - If no valid separators remain after filtering, construct and return an "empty" output grid. This grid should have the same height as the input grid but zero width (represented as a list of N empty lists, where N is the input height).
   - If valid separators exist, assume they *all* share the same color (based on observed examples and initial code logic). Identify this common "separator color" and collect all column indices where these valid separators occur.
6. Extract Subgrid based on Color:
   - If the separator color is Red (code 2): Find the *maximum* (rightmost) index among the valid separator indices. Extract the portion of the input grid containing all columns strictly to the *right* of this index. If the rightmost separator index was the last column of the input grid, the result is an empty grid (width 0).
   - If the separator color is NOT Red: Find the *minimum* (leftmost) index among the valid separator indices. Extract the portion of the input grid containing all columns strictly to the *left* of this index. If the leftmost separator index was the first column (index 0) of the input grid, the result is an empty grid (width 0).
7. Format Output: Convert the extracted subgrid (which might be a NumPy array slice) into the required output format (a list of lists). Ensure that empty grids resulting from slicing are correctly represented as a list of empty lists with the original height.
"""

def _find_potential_separators(grid: np.ndarray) -> Optional[Dict[int, List[int]]]:
    """
    Identifies columns that are uniform in color and span the full grid height.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A dictionary mapping color -> list of column indices for potential separators,
        or None if the grid is empty or has no uniform columns.
    """
    if grid.size == 0: # Handles both (0, w) and (h, 0) shapes
        return None

    height, width = grid.shape
    if height == 0 or width == 0: # Redundant check, but safe
        return None

    potential_separators: Dict[int, List[int]] = {}
    for c in range(width):
        column = grid[:, c]
        # Check if all elements in the column are the same
        if np.all(column == column[0]):
            color = column[0]
            if color not in potential_separators:
                potential_separators[color] = []
            potential_separators[color].append(c)

    return potential_separators if potential_separators else None

def _get_background_color(grid: np.ndarray) -> Optional[int]:
    """
    Determines the most frequent color in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        The most frequent color code, or None if the grid is empty.
    """
    if grid.size == 0:
        return None

    color_counts = Counter(grid.flatten())
    if not color_counts: # Should not happen if grid.size > 0, but defensive
        return None
    # most_common(1) returns a list of tuples [(color, count)]
    background_color = color_counts.most_common(1)[0][0]
    return background_color

def _filter_separators(
    potential_separators: Dict[int, List[int]],
    background_color: Optional[int]
) -> Tuple[Optional[List[int]], Optional[int]]:
    """
    Filters potential separators, removing those matching the background color.
    Assumes remaining valid separators share the same color.

    Args:
        potential_separators: Dict from _find_potential_separators.
        background_color: The background color determined by _get_background_color.

    Returns:
        A tuple containing:
        - A sorted list of indices of the valid separator columns, or None.
        - The uniform color of the valid separator columns, or None.
    """
    if potential_separators is None:
      return None, None

    valid_separator_colors = list(potential_separators.keys())

    # Remove background color if it exists among separators
    if background_color is not None and background_color in valid_separator_colors:
         # Make a copy to iterate over while modifying the original list
        for color in list(valid_separator_colors):
            if color == background_color:
                valid_separator_colors.remove(color)


    if not valid_separator_colors:
        return None, None # No non-background separators found

    # Assumption: Only one separator color remains after filtering background.
    # If multiple non-background uniform colors exist, use the first one found.
    # (The order depends on dict iteration order, which is insertion order in Python 3.7+)
    # A more robust rule might be needed if this assumption fails on hidden tests.
    separator_color = valid_separator_colors[0]
    # Retrieve the indices for this specific color from the original dict
    separator_indices = sorted(potential_separators[separator_color])

    return separator_indices, separator_color

def _create_empty_output(height: int) -> List[List[int]]:
    """Creates an empty grid representation with the specified height."""
    return [[] for _ in range(height)]

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on vertical separator lines, extracting
    a subgrid to the left or right depending on the separator color.
    """

    # --- 1. Analyze Input & Handle Edge Cases ---
    if not input_grid:
        return [] # Input is []

    # Attempt to convert to numpy array
    try:
        grid_np = np.array(input_grid, dtype=int)
    except ValueError:
        # Handles cases like [[1], [1, 2]] - inconsistent row lengths
        # Decide on behavior: return empty, raise error, etc. Let's return [].
        # This case technically violates ARC grid constraints.
        return []

    # Check for shapes like (n, 0) which result from [[], [], ...]
    if grid_np.ndim == 1 and len(input_grid) > 0 and isinstance(input_grid[0], list) and not input_grid[0]:
         # Input was [[], [], ...]
         height = len(input_grid)
         return _create_empty_output(height) # Return list of empty lists
    elif grid_np.ndim == 2:
         height, width = grid_np.shape
         if width == 0:
             # Input was [[]] or similar resulting in shape (h, 0)
             return _create_empty_output(height)
         if height == 0:
              # Input was [] resulting in shape (0,w) - handled by initial check
              # but being thorough.
              return []
    else:
        # Malformed input not conforming to 2D grid structure
        return [] # Default return for unexpected formats

    # --- 2. Identify Potential Separators ---
    potential_separators = _find_potential_separators(grid_np)

    # If no uniform columns at all, return empty grid (implicitly handled later if needed)
    # This check is not strictly necessary as filtering would also yield no valid separators

    # --- 3. Determine Background Color ---
    background_color = _get_background_color(grid_np)

    # --- 4. Filter Separators ---
    separator_indices, separator_color = _filter_separators(potential_separators, background_color)

    # --- 5. Check for Valid Separators ---
    if separator_indices is None:
        # No valid (non-background) separators found
        return _create_empty_output(height)

    # --- 6. Extract Subgrid based on Color ---
    output_grid_np = None

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

    # --- 7. Format Output ---
    # Convert the resulting numpy array back to a list of lists
    # np.tolist() correctly handles (h, 0) arrays, returning [[]]*h
    output_grid = output_grid_np.tolist()

    return output_grid