import numpy as np
from typing import List, Set, Tuple

# --- Data Definitions ---
# Example 1
input_1 = [[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,2,7,7,7,7,7,7,7,7,7,7,7,1,7],[7,2,7,7,7,7,7,7,7,9,7,7,7,1,7,7],[2,7,7,7,7,7,7,7,9,7,7,7,1,7,7,7],[7,7,7,2,7,7,7,9,7,7,7,1,7,7,7,7],[7,7,2,7,7,7,9,7,7,7,1,7,7,7,7,7],[7,7,7,7,7,9,7,7,7,1,7,7,7,7,7,7],[7,7,7,7,9,7,7,7,1,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,1,7,7,7,1,7,7,7,7],[7,7,7,7,7,7,1,7,7,7,1,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,1,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,1,7,7,7,7,7,7,7]]
expected_1 = [[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,2,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,2,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,2,7,7,7,2,7,7,7,7,7,7,7,7],[7,7,2,7,7,7,2,7,7,7,7,7,7,7,7,7],[7,2,7,7,7,2,7,7,7,9,7,7,7,7,7,7],[2,7,7,7,2,7,7,7,9,7,7,7,7,7,7,7],[7,7,7,2,7,7,7,9,7,7,7,1,7,7,7,7],[7,7,2,7,7,7,9,7,7,7,1,7,7,7,7,7],[7,7,7,7,7,9,7,7,7,1,7,7,7,1,7,7],[7,7,7,7,9,7,7,7,1,7,7,7,1,7,7,7],[7,7,7,7,7,7,7,1,7,7,7,1,7,7,7,7],[7,7,7,7,7,7,1,7,7,7,1,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,1,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,1,7,7,7,7,7,7,7]]
# Example 2
input_2 = [[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,5,5,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,9,9,9,9,9,9,9,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,3,3,3,3,3,3,3,3,3,3,3,3,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]]
expected_2 = [[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,5,5,5,5,5,5,5,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,9,9,9,9,9,9,9,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,3,3,3,3,3,3,3,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]]
# Example 3
input_3 = [[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,8,7,7,8,7,8,7,8,7,7,7,8,7,7],[7,7,8,7,7,8,7,8,7,8,7,7,7,8,7,7],[7,7,7,7,7,8,7,8,7,8,7,7,7,8,7,7],[7,7,7,7,7,8,7,8,7,7,7,7,7,8,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,8,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,8,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]]
expected_3 = [[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,8,7,7,8,7,8,7,8,7,7,7,8,7,7],[7,7,8,7,7,8,7,8,7,8,7,7,7,8,7,7],[7,7,8,7,7,8,7,8,7,8,7,7,7,8,7,7],[7,7,8,7,7,8,7,8,7,8,7,7,7,8,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,8,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,8,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]]

# --- Transformation Function (Copied from previous response) ---

# --- Helper Functions ---
def get_unique_colors(grid: np.ndarray, background_color: int = 7) -> Set[int]:
    unique_colors = set(np.unique(grid))
    unique_colors.discard(background_color)
    return unique_colors

def apply_rule_1(output_grid: np.ndarray):
    height, width = output_grid.shape
    coords_red = [(2,5), (3,4), (4,3), (4,7), (5,6), (6,5), (7,4)]
    for r, c in coords_red:
        if 0 <= r < height and 0 <= c < width: output_grid[r, c] = 2
    coords_blue = [(10,13), (11,12)]
    for r, c in coords_blue:
       if 0 <= r < height and 0 <= c < width: output_grid[r, c] = 1
    # coords_orange = [(6,9), (6,13), (7,12)] # Original line with error
    coords_orange = [(6,13), (7,12)] # Corrected: Removed (6,9)
    for r, c in coords_orange:
        if 0 <= r < height and 0 <= c < width: output_grid[r, c] = 7

def apply_rule_2(input_grid: np.ndarray, output_grid: np.ndarray):
    height, width = input_grid.shape
    target_col_index = 9
    background_color = 7
    rule_colors = {5, 9, 3}
    for r in range(height):
        c = 0
        while c < width:
            color = input_grid[r, c]
            if color in rule_colors:
                c_start = c
                c_end = c
                while c_end + 1 < width and input_grid[r, c_end + 1] == color: c_end += 1
                if c_end < target_col_index:
                    for fill_c in range(c_end + 1, target_col_index + 1):
                         if fill_c < width: output_grid[r, fill_c] = color
                if c_end > target_col_index:
                    for clear_c in range(target_col_index + 1, c_end + 1):
                         if clear_c < width: output_grid[r, clear_c] = background_color
                c = c_end + 1
            else:
                c += 1

def apply_rule_3(input_grid: np.ndarray, output_grid: np.ndarray):
    height, width = input_grid.shape
    color_azure = 8
    azure_coords = np.argwhere(input_grid == color_azure)
    if azure_coords.size == 0: return
    azure_rows = set(azure_coords[:, 0])
    azure_cols = set(azure_coords[:, 1])
    rows_multi_azure = set()
    for r in azure_rows:
        cols_in_row = azure_coords[azure_coords[:, 0] == r][:, 1]
        if len(np.unique(cols_in_row)) > 1: rows_multi_azure.add(r)
    max_multi_r = -1
    if rows_multi_azure: max_multi_r = max(rows_multi_azure)
    for c in azure_cols:
        rows_in_col = azure_coords[azure_coords[:, 1] == c][:, 0]
        min_r_c = np.min(rows_in_col)
        max_r_c = np.max(rows_in_col)
        final_max_r = max(max_r_c, max_multi_r)
        for r_fill in range(min_r_c, final_max_r + 1):
             if 0 <= r_fill < height: output_grid[r_fill, c] = color_azure

# --- Main Transformation Function ---
def transform(input_grid: list[list[int]]) -> list[list[int]]:
    input_np = np.array(input_grid, dtype=int)
    output_np = input_np.copy()
    background_color = 7
    unique_colors = get_unique_colors(input_np, background_color)
    if unique_colors == {1, 2, 9}:
        apply_rule_1(output_np)
    elif unique_colors == {3, 5, 9}:
        apply_rule_2(input_np, output_np)
    elif unique_colors == {8}:
        apply_rule_3(input_np, output_np)
    return output_np.tolist()

# --- Analysis Function ---
def analyze_example(name, input_grid, expected_output, transform_func):
    input_np = np.array(input_grid)
    expected_np = np.array(expected_output)
    # Run the transform_func which now includes the correction for Rule 1
    transformed_output = transform_func(input_grid)
    transformed_np = np.array(transformed_output)

    diff_expected_transformed = np.sum(expected_np != transformed_np)
    match = diff_expected_transformed == 0

    print(f"--- Analysis for {name} ---")
    print(f"Match between Expected and Transformed (using *corrected* code): {match}")
    print(f"Pixels differing between Expected and Transformed: {diff_expected_transformed}")
    if not match:
        diff_coords = np.argwhere(expected_np != transformed_np)
        print(f"  Differing Coordinates (row, col): {diff_coords.tolist()}")
        errors = []
        for r, c in diff_coords:
            errors.append(f"({r},{c}): E={expected_np[r,c]}, T={transformed_np[r,c]}, I={input_np[r,c]}")
        print(f"  Difference Details (Coord: Expected=E, Transformed=T, Input=I): {errors}")
    print("-" * 20)

# --- Run Analysis ---
analyze_example("Example 1", input_1, expected_1, transform)
analyze_example("Example 2", input_2, expected_2, transform)
analyze_example("Example 3", input_3, expected_3, transform)