```python
import numpy as np
from typing import List, Tuple

"""
Transforms an input grid based on patterns identified in its bottom-left (Q3) and bottom-right (Q4) quadrants.

1. Divide the `input_grid` into four equal quadrants: top-left (Q1), top-right (Q2), bottom-left (Q3), and bottom-right (Q4).
2. Analyze the complexity (number of unique non-zero values) of Q3 and Q4. Designate the quadrant with higher complexity as `pattern_quadrant`. If complexities are equal, designate Q4 as `pattern_quadrant`. Designate the other quadrant as `fill_quadrant`.
3. Determine the `fill_value` by finding the most frequent non-zero value in `fill_quadrant`. If `fill_quadrant` contains only zeros, `fill_value` is 0.
4. Apply a specific transformation rule based on the characteristics of `pattern_quadrant` and `fill_quadrant`:

    *   **Rule A (Direct Copy - train_4):** If `fill_value` is 0 and `pattern_quadrant` is Q3, the `output_grid` is identical to `pattern_quadrant`.
    *   **Rule B (Value Combination Tiling - train_1):** If `pattern_quadrant` is Q4 containing values {5, 6} (often with 0s) and `fill_quadrant` is Q3 containing value {1} (often with 0s), create a 2x2 `base_tile` `[[6, 5], [5, 6]]`. Tile this `base_tile` to create an `output_grid` that is 4 times the dimensions of the `pattern_quadrant` (e.g., if Q4 is 4x4, output is 16x16).
    *   **Rule C (Pattern Application Tiling - train_2):** If `pattern_quadrant` is Q4 containing value {4} (often with 0s, forming a pattern like a border) and `fill_quadrant` is Q3 containing values {1, 5} (often in uniform rows/blocks), create a `base_tile` the same size as `pattern_quadrant` by taking `pattern_quadrant` and replacing its 0s with the corresponding element from `fill_quadrant`. Tile this `base_tile` 4x4 times to create the `output_grid` (e.g., if `base_tile` is 4x4, output is 16x16).
    *   **Rule D (Zero Replacement and Modification - train_3):** If `pattern_quadrant` is Q4 containing values {6, 8} (often with 0s) and `fill_quadrant` is Q3 containing value {1}, create a temporary grid `P_mod` by replacing the 0s in `pattern_quadrant` with the `fill_value` (1). Select rows `[0, 1, 2, 3, 4, 0, 1, 2, 3, 4]` from `P_mod`. Form the `output_grid` by taking these selected rows and appending two new columns filled entirely with the `fill_value` (1) to the right.
    *   **Rule E (Zero Replacement and Row Selection - train_5):** If `pattern_quadrant` is Q4 containing value {1} (often with 0s) and `fill_quadrant` is Q3 containing value {6}, create a temporary grid by replacing the 0s in `pattern_quadrant` with the `fill_value` (6). The `output_grid` consists of the first 3 rows of this temporary grid.

5. Return the generated `output_grid`.
"""


# Helper Functions
def get_quadrants(grid: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Splits the grid into four equal quadrants."""
    rows, cols = grid.shape
    r_mid, c_mid = rows // 2, cols // 2
    q1 = grid[0:r_mid, 0:c_mid]
    q2 = grid[0:r_mid, c_mid:cols]
    q3 = grid[r_mid:rows, 0:c_mid]
    q4 = grid[r_mid:rows, c_mid:cols]
    return q1, q2, q3, q4

def calculate_complexity(grid: np.ndarray) -> int:
    """Calculates a simple complexity score (number of unique non-zero values)."""
    unique_vals = np.unique(grid)
    non_zero_unique = unique_vals[unique_vals != 0]
    return len(non_zero_unique)

def get_dominant_non_zero(grid: np.ndarray) -> int:
    """Finds the most frequent non-zero value. Returns 0 if all zeros or empty."""
    non_zero_elements = grid[grid != 0]
    if non_zero_elements.size == 0:
        return 0
    unique_vals, counts = np.unique(non_zero_elements, return_counts=True)
    return unique_vals[np.argmax(counts)]


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic based on Q3 and Q4 analysis.
    """
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Divide into quadrants
    q1, q2, q3, q4 = get_quadrants(input_array)

    # 2. Analyze complexity of Q3 and Q4
    c3 = calculate_complexity(q3)
    c4 = calculate_complexity(q4)

    # 3. Determine pattern and fill quadrants
    # Higher complexity = pattern. If equal, Q4 is pattern.
    if c3 > c4:
        pattern_quadrant = q3
        fill_quadrant = q4
    else: # c4 >= c3
        pattern_quadrant = q4
        fill_quadrant = q3
        
    # 4. Extract fill value
    fill_value = get_dominant_non_zero(fill_quadrant)
    
    # Get unique non-zero values for precise rule matching
    pattern_unique_nz = set(np.unique(pattern_quadrant[pattern_quadrant != 0]))
    fill_unique_nz = set(np.unique(fill_quadrant[fill_quadrant != 0]))

    output_grid = None # Initialize output

    # 5. Apply transformation rules based on examples
    
    # Rule A (Direct Copy - train_4)
    # Trigger: fill value is 0 and pattern is Q3.
    if fill_value == 0 and pattern_quadrant is q3: 
         output_grid = pattern_quadrant

    # Rule B (Value Combination Tiling - train_1)
    # Trigger: Pattern=Q4 ({5, 6}), Fill=Q3 ({1}).
    elif pattern_quadrant is q4 and fill_quadrant is q3 and \
         pattern_unique_nz == {5, 6} and fill_unique_nz == {1}:
        # Create the 2x2 base tile
        tile = np.array([[6, 5], [5, 6]], dtype=int)
        # Tile to 4x the size of the pattern quadrant (e.g., 4x4 -> 16x16)
        quad_rows, quad_cols = pattern_quadrant.shape
        output_grid = np.tile(tile, (quad_rows * 2, quad_cols * 2)) # Correct tiling factor

    # Rule C (Pattern Application Tiling - train_2)
    # Trigger: Pattern=Q4 ({4}), Fill=Q3 ({1, 5}).
    elif pattern_quadrant is q4 and fill_quadrant is q3 and \
         pattern_unique_nz == {4} and fill_unique_nz == {1, 5}:
        # Create base tile by replacing 0s in pattern with corresponding fill elements
        base_tile = pattern_quadrant.copy()
        mask = (base_tile == 0)
        base_tile[mask] = fill_quadrant[mask]
        # Tile the base tile 4x4
        output_grid = np.tile(base_tile, (4, 4))

    # Rule D (Zero Replacement and Modification - train_3)
    # Trigger: Pattern=Q4 ({6, 8}), Fill=Q3 ({1}).
    elif pattern_quadrant is q4 and fill_quadrant is q3 and \
         pattern_unique_nz == {6, 8} and fill_unique_nz == {1}:
         # Create P_mod by replacing 0s with fill_value
         pattern_mod = pattern_quadrant.copy()
         pattern_mod[pattern_mod == 0] = fill_value # Replace 0s with 1
         # Select specific rows: [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
         selected_rows_indices = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
         selected_rows = pattern_mod[selected_rows_indices, :]
         # Create two columns of the fill value
         num_selected_rows = len(selected_rows_indices)
         append_cols = np.full((num_selected_rows, 2), fill_value, dtype=int)
         # Stack horizontally
         output_grid = np.hstack((selected_rows, append_cols))

    # Rule E (Zero Replacement and Row Selection - train_5)
    # Trigger: Pattern=Q4 ({1}), Fill=Q3 ({6}).
    elif pattern_quadrant is q4 and fill_quadrant is q3 and \
         pattern_unique_nz == {1} and fill_unique_nz == {6}:
         # Create temp grid by replacing 0s with fill_value
         pattern_mod = pattern_quadrant.copy()
         pattern_mod[pattern_mod == 0] = fill_value # Replace 0s with 6
         # Select first 3 rows
         output_grid = pattern_mod[0:3, :]

    # Fallback: If no specific rule matched, raise an error.
    if output_grid is None:
        raise ValueError("Input grid does not match any known transformation pattern.")

    # Convert final NumPy array back to list of lists for the expected output format
    return output_grid.tolist()
```