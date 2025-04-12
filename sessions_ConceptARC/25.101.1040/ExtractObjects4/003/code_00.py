"""
Identifies the single dominant non-white color in the input grid.
Determines the set of rows that contain at least one instance of this dominant color ('relevant rows').
Counts the number of columns where all cells intersecting with the relevant rows contain only the dominant color ('pure columns').
Generates a square output grid whose side length equals the count of pure columns, filled entirely with the dominant color.
"""

import numpy as np
from typing import List, Tuple, Optional

# Helper function to find the dominant non-white color
def find_dominant_color(grid_np: np.ndarray) -> Optional[int]:
    """Finds the single non-white color in the grid."""
    unique_colors = np.unique(grid_np)
    non_white_colors = unique_colors[unique_colors != 0]
    if len(non_white_colors) == 1:
        return int(non_white_colors[0])
    elif len(non_white_colors) == 0:
        # Handle case with no non-white colors (e.g., all white grid)
        return None
    else:
        # Handle case with multiple non-white colors if needed,
        # based on examples, only one is expected.
        # For now, return the first one found, though this might need adjustment
        # if future tasks show ambiguity.
        # print(f"Warning: Found multiple non-white colors: {non_white_colors}. Using {non_white_colors[0]}")
        return int(non_white_colors[0]) # Or raise an error

# Helper function to find relevant row indices
def find_relevant_rows(grid_np: np.ndarray, dominant_color: int) -> np.ndarray:
    """Finds the indices of rows containing the dominant color."""
    if dominant_color is None:
        return np.array([], dtype=int)
    rows_with_color = np.any(grid_np == dominant_color, axis=1)
    relevant_indices = np.where(rows_with_color)[0]
    return relevant_indices

# Helper function to count pure columns
def count_pure_columns(grid_np: np.ndarray, dominant_color: int, relevant_row_indices: np.ndarray) -> int:
    """Counts columns that are 'pure' with respect to the dominant color in relevant rows."""
    # If no dominant color or no relevant rows found, no columns can be pure by definition.
    if dominant_color is None or relevant_row_indices.size == 0:
        return 0

    num_cols = grid_np.shape[1]
    pure_column_count = 0

    for j in range(num_cols):
        # Extract the column slice corresponding to the relevant rows
        column_slice = grid_np[relevant_row_indices, j]
        # Check if all elements in this slice are the dominant color
        if np.all(column_slice == dominant_color):
            pure_column_count += 1

    return pure_column_count

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on identifying pure columns relative to the dominant color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    # Convert input to numpy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Handle empty input grid case
    if input_grid_np.size == 0:
        return []

    # 1. Identify the Dominant Color
    dominant_color = find_dominant_color(input_grid_np)

    # Handle case where no dominant color is found (e.g., all white)
    if dominant_color is None:
        # Return empty grid or handle as per specific task requirements if this occurs
        return []

    # 2. Identify Relevant Rows (rows containing the dominant color)
    relevant_row_indices = find_relevant_rows(input_grid_np, dominant_color)

    # 3. Count Pure Columns
    # A column is pure if, for all relevant rows, the cell in that column contains the dominant color.
    pure_column_count = count_pure_columns(input_grid_np, dominant_color, relevant_row_indices)

    # 4. Determine Output Size
    output_size = pure_column_count

    # 5. Create Output Grid
    # Generate an N x N grid filled with the dominant color, where N is the pure column count.
    output_grid_np = np.full((output_size, output_size), dominant_color, dtype=int)

    # Convert numpy array back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid