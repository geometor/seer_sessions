"""
Transforms the input grid by:
1. Identifying the single dominant non-white color (C).
2. Identifying the rows that contain at least one pixel of color C ('relevant rows').
3. Identifying columns that contain any pixel *not* equal to C within the relevant rows ('impure columns').
4. Counting the number of impure columns.
5. Calculating the output grid size N as the input grid's width minus the count of impure columns.
6. Generating an N x N square grid filled entirely with the dominant color C.
"""

import numpy as np
from typing import List, Tuple, Optional

# Helper function to find the dominant non-white color
def find_dominant_color(grid_np: np.ndarray) -> Optional[int]:
    """Finds the single non-white color in the grid."""
    unique_colors = np.unique(grid_np)
    non_white_colors = unique_colors[unique_colors != 0]
    if len(non_white_colors) >= 1:
        # In case of multiple non-white, task examples imply only one matters.
        # We can assume the lowest numbered one, or most frequent,
        # but based on examples, taking the first (often only) one works.
        return int(non_white_colors[0])
    else:
        # Handle case with no non-white colors (e.g., all white grid)
        return None

# Helper function to find relevant row indices
def find_relevant_rows(grid_np: np.ndarray, dominant_color: int) -> np.ndarray:
    """Finds the indices of rows containing the dominant color."""
    if dominant_color is None:
        return np.array([], dtype=int)
    rows_with_color = np.any(grid_np == dominant_color, axis=1)
    relevant_indices = np.where(rows_with_color)[0]
    return relevant_indices

# Helper function to count impure columns
def count_impure_columns(grid_np: np.ndarray, dominant_color: int, relevant_row_indices: np.ndarray) -> int:
    """Counts columns that contain any non-dominant color within relevant rows."""
    # If no dominant color or no relevant rows found, define all columns as 'not impure' based on this criteria.
    if dominant_color is None or relevant_row_indices.size == 0:
        return 0

    num_cols = grid_np.shape[1]
    impure_column_count = 0

    for j in range(num_cols):
        # Extract the column slice corresponding to the relevant rows
        column_slice = grid_np[relevant_row_indices, j]
        # Check if *any* element in this slice is *not* the dominant color
        if np.any(column_slice != dominant_color):
            impure_column_count += 1

    return impure_column_count

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on identifying impure columns relative to the dominant color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Handle empty input grid case
    if input_grid_np.size == 0:
        return []

    # 1. Identify the Dominant Color
    dominant_color = find_dominant_color(input_grid_np)

    # Handle case where no dominant color is found (e.g., all white)
    if dominant_color is None:
        # Based on examples, this shouldn't happen, but returning empty seems reasonable.
        return []

    # 2. Identify Relevant Rows (rows containing the dominant color)
    relevant_row_indices = find_relevant_rows(input_grid_np, dominant_color)

    # 3. Count Impure Columns
    # A column is impure if, within any relevant row, it contains a color other than the dominant one.
    impure_column_count = count_impure_columns(input_grid_np, dominant_color, relevant_row_indices)

    # 4. Determine Output Size
    input_width = input_grid_np.shape[1]
    output_size = input_width - impure_column_count

    # Ensure output size is not negative (though unlikely given the logic)
    output_size = max(0, output_size)

    # 5. Create Output Grid
    # Generate an N x N grid filled with the dominant color, where N is the calculated size.
    output_grid_np = np.full((output_size, output_size), dominant_color, dtype=int)

    # Convert numpy array back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid