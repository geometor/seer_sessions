```python
"""
Transforms an input grid by identifying delimiter lines (a single row and column 
composed of the same repeated number) and a unique element (a number appearing 
only once). The output grid is the quadrant defined by the delimiter lines that 
contains the unique element.
"""

import numpy as np
from collections import Counter

def _find_delimiter_lines(grid: np.ndarray) -> tuple[int, int, int]:
    """
    Finds the number and indices forming the complete horizontal and vertical lines.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        A tuple containing:
        - delimiter_num: The number forming the delimiter lines.
        - delimiter_row_idx: The index of the delimiter row.
        - delimiter_col_idx: The index of the delimiter column.

    Raises:
        ValueError: If delimiter lines cannot be uniquely identified.
    """
    rows, cols = grid.shape
    delimiter_row_idx = -1
    delimiter_col_idx = -1
    delimiter_num_row = -1
    delimiter_num_col = -1

    # Check rows
    for r in range(rows):
        if len(set(grid[r, :])) == 1:
            if delimiter_row_idx != -1:
                raise ValueError("Multiple possible delimiter rows found.")
            delimiter_row_idx = r
            delimiter_num_row = grid[r, 0]

    # Check columns
    for c in range(cols):
        if len(set(grid[:, c])) == 1:
            if delimiter_col_idx != -1:
                raise ValueError("Multiple possible delimiter columns found.")
            delimiter_col_idx = c
            delimiter_num_col = grid[0, c]
    
    # Validate findings
    if delimiter_row_idx == -1:
        raise ValueError("No delimiter row found.")
    if delimiter_col_idx == -1:
        raise ValueError("No delimiter column found.")
    if delimiter_num_row != delimiter_num_col:
         raise ValueError(f"Delimiter row number ({delimiter_num_row}) and column number ({delimiter_num_col}) do not match.")
    if grid[delimiter_row_idx, delimiter_col_idx] != delimiter_num_row:
        raise ValueError("Delimiter intersection point does not match delimiter number.")


    return delimiter_num_row, delimiter_row_idx, delimiter_col_idx

def _find_unique_element(grid: np.ndarray) -> tuple[int, int, int]:
    """
    Finds the number that appears only once in the grid and its location.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        A tuple containing:
        - unique_val: The unique number.
        - unique_row_idx: The row index of the unique number.
        - unique_col_idx: The column index of the unique number.
        
    Raises:
        ValueError: If exactly one unique element is not found.
    """
    counts = Counter(grid.flatten())
    unique_val = -1
    found_unique = False

    for val, count in counts.items():
        if count == 1:
            if found_unique:
                 raise ValueError("Multiple unique elements found.")
            unique_val = val
            found_unique = True

    if not found_unique:
         raise ValueError("No unique element found.")

    # Find the location
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == unique_val:
                return unique_val, r, c
                
    # This part should technically not be reachable if a unique value was found
    raise ValueError("Unique element identified but not located in the grid.") 


def _extract_quadrant(grid: np.ndarray, del_row: int, del_col: int, unique_row: int, unique_col: int) -> list[list[int]]:
    """
    Extracts the subgrid (quadrant) containing the unique element.

    Args:
        grid: The input grid as a NumPy array.
        del_row: The index of the delimiter row.
        del_col: The index of the delimiter column.
        unique_row: The row index of the unique element.
        unique_col: The column index of the unique element.

    Returns:
        The selected quadrant as a list of lists.
        
    Raises:
        ValueError: If the unique element lies on a delimiter line.
    """
    if unique_row == del_row or unique_col == del_col:
        raise ValueError("Unique element cannot lie on a delimiter line.")

    # Determine quadrant and extract
    if unique_row < del_row and unique_col < del_col: # Top-Left
        subgrid = grid[0:del_row, 0:del_col]
    elif unique_row < del_row and unique_col > del_col: # Top-Right
        subgrid = grid[0:del_row, del_col+1:]
    elif unique_row > del_row and unique_col < del_col: # Bottom-Left
        subgrid = grid[del_row+1:, 0:del_col]
    elif unique_row > del_row and unique_col > del_col: # Bottom-Right
        subgrid = grid[del_row+1:, del_col+1:]
    else:
         # Should not happen if previous checks are correct
         raise ValueError("Could not determine quadrant for unique element.") 

    return subgrid.tolist()


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms an input grid based on delimiter lines and a unique element.

    1. Identifies a delimiter row and column (lines made of a single repeated number).
    2. Finds the element that appears exactly once in the grid.
    3. Determines which of the four quadrants defined by the delimiter lines contains the unique element.
    4. Returns that quadrant as the output grid.
    """
    # Convert input to NumPy array for easier slicing and analysis
    input_np = np.array(input_grid, dtype=int)

    # Find the delimiter lines
    delimiter_num, delimiter_row_idx, delimiter_col_idx = _find_delimiter_lines(input_np)

    # Find the unique element and its location
    unique_val, unique_row_idx, unique_col_idx = _find_unique_element(input_np)

    # Extract the quadrant containing the unique element
    output_grid = _extract_quadrant(input_np, delimiter_row_idx, delimiter_col_idx, unique_row_idx, unique_col_idx)

    return output_grid
```