```python
import math
import numpy as np # Using numpy for easier array slicing and manipulation

"""
Transforms a 9x9 input grid into a 6x6 output grid based on dividing lines and quadrant mapping.

1.  **Locate Dividers:** Scan the 9x9 input grid to find the row index (`div_r`) and column index (`div_c`) that are entirely filled with the value 8.
2.  **Identify Regions:** Determine the four rectangular regions created by these dividers.
3.  **Extract Value Map:** Identify the 2x2 region among the four that does *not* contain the dividers. Extract the four values from this region into a 2x2 array, `value_map`.
4.  **Extract Pattern Grid:** Identify the 6x6 region among the four that does *not* contain the dividers. Extract the values from this region into a 6x6 array, `pattern_grid`.
5.  **Initialize Output:** Create a new 6x6 grid, `output_grid`, filled with zeros.
6.  **Apply Pattern and Values:** Iterate through each cell `(r, c)` of the `pattern_grid`. If the cell value is 3, determine the corresponding value from `value_map` based on which 3x3 quadrant `(r, c)` falls into within the `pattern_grid`, and place this value in `output_grid[r][c]`.
7.  **Return Result:** The final `output_grid` is the result of the transformation.
"""

def _find_dividers(grid: np.ndarray) -> tuple[int, int]:
    """Finds the row and column index completely filled with 8s."""
    div_r, div_c = -1, -1
    rows, cols = grid.shape
    # Find divider row
    for r in range(rows):
        if np.all(grid[r, :] == 8):
            div_r = r
            break
    # Find divider column
    for c in range(cols):
        if np.all(grid[:, c] == 8):
            div_c = c
            break
    if div_r == -1 or div_c == -1:
        raise ValueError("Divider row or column not found")
    return div_r, div_c

def _extract_subgrid(grid: np.ndarray, r_start: int, r_end: int, c_start: int, c_end: int) -> np.ndarray:
    """Extracts a subgrid using slicing."""
    return grid[r_start:r_end, c_start:c_end]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the quadrant value mapping transformation.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    if rows != 9 or cols != 9:
         raise ValueError("Input grid must be 9x9")

    # 1. Locate Dividers
    div_r, div_c = _find_dividers(input_array)

    # 2. Identify Regions & Extract Value Map and Pattern Grid
    regions = [
        (0, div_r, 0, div_c),          # Top-Left
        (0, div_r, div_c + 1, cols),   # Top-Right
        (div_r + 1, rows, 0, div_c),   # Bottom-Left
        (div_r + 1, rows, div_c + 1, cols) # Bottom-Right
    ]

    value_map_source = None
    pattern_grid_source = None

    for r_start, r_end, c_start, c_end in regions:
        height = r_end - r_start
        width = c_end - c_start
        if height == 2 and width == 2:
            value_map_source = _extract_subgrid(input_array, r_start, r_end, c_start, c_end)
        elif height == 6 and width == 6:
            pattern_grid_source = _extract_subgrid(input_array, r_start, r_end, c_start, c_end)

    if value_map_source is None or pattern_grid_source is None:
        raise ValueError("Could not identify 2x2 value map and 6x6 pattern grid regions")

    # 3. Extract Value Map (ensure it's in the correct format if needed, numpy handles it)
    value_map = value_map_source 
    # [[v00, v01], [v10, v11]] = value_map

    # 4. Extract Pattern Grid
    pattern_grid = pattern_grid_source

    # 5. Initialize Output
    output_grid = np.zeros((6, 6), dtype=int)

    # 6. Apply Pattern and Values
    for r in range(6):
        for c in range(6):
            if pattern_grid[r, c] == 3:
                # Determine quadrant within the 6x6 pattern grid
                if r < 3 and c < 3:        # Top-Left quadrant
                    value = value_map[0, 0]
                elif r < 3 and c >= 3:     # Top-Right quadrant
                    value = value_map[0, 1]
                elif r >= 3 and c < 3:     # Bottom-Left quadrant
                    value = value_map[1, 0]
                else: # r >= 3 and c >= 3  # Bottom-Right quadrant
                    value = value_map[1, 1]
                
                # Set value in output grid
                output_grid[r, c] = value
            # else: output_grid[r, c] remains 0 (initialized value)

    # 7. Return Result (convert back to list of lists)
    return output_grid.tolist()

```