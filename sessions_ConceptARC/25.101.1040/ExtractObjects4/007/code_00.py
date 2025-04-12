"""
Transforms an input grid based on the following rules:
1. Identify the single dominant non-white color (C) in the input grid.
2. Identify the rows containing at least one pixel of color C ('relevant rows').
3. Identify columns that contain *only* color C for all pixels intersecting with the relevant rows ('pure columns').
4. Find the largest number of consecutively indexed pure columns (the 'largest contiguous pure column block size', N).
5. Generate an N x N square output grid filled entirely with the dominant color C.
"""

import numpy as np
from typing import List, Optional, Set

def find_dominant_color(grid_np: np.ndarray) -> Optional[int]:
    """Finds the single non-white color in the grid, assuming one exists."""
    unique_colors = np.unique(grid_np)
    non_white_colors = unique_colors[unique_colors != 0]
    if len(non_white_colors) >= 1:
        # Based on examples, assume the first non-white color is dominant.
        return int(non_white_colors[0])
    else:
        # No non-white color found
        return None

def find_relevant_rows(grid_np: np.ndarray, dominant_color: int) -> np.ndarray:
    """Finds the indices of rows containing the dominant color."""
    if dominant_color is None:
        return np.array([], dtype=int)
    rows_with_color = np.any(grid_np == dominant_color, axis=1)
    relevant_indices = np.where(rows_with_color)[0]
    return relevant_indices

def find_pure_column_indices(grid_np: np.ndarray, dominant_color: int, relevant_row_indices: np.ndarray) -> List[int]:
    """Finds indices of columns that are pure within relevant rows."""
    pure_indices = []
    if dominant_color is None or relevant_row_indices.size == 0:
        return pure_indices

    num_cols = grid_np.shape[1]
    for j in range(num_cols):
        column_slice = grid_np[relevant_row_indices, j]
        if np.all(column_slice == dominant_color):
            pure_indices.append(j)
    return pure_indices

def find_largest_contiguous_block_size(indices: List[int]) -> int:
    """Calculates the maximum length of consecutive numbers in a sorted list."""
    if not indices:
        return 0

    indices.sort() # Ensure indices are sorted
    max_len = 0
    current_len = 0
    last_idx = -2 # Initialize to ensure the first index starts a new block

    for idx in indices:
        if idx == last_idx + 1:
            # Index is contiguous with the previous one
            current_len += 1
        else:
            # Non-contiguous index, end the previous block
            max_len = max(max_len, current_len)
            # Start a new block of length 1
            current_len = 1
        last_idx = idx

    # Check the length of the last block after the loop finishes
    max_len = max(max_len, current_len)
    return max_len

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation logic to the input grid.
    """
    # Convert input to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Handle empty input grid
    if input_grid_np.size == 0:
        return []

    # Step 1: Identify the Dominant Color
    dominant_color = find_dominant_color(input_grid_np)
    if dominant_color is None:
         # If no dominant color, output is empty (or handle as needed)
        return []

    # Step 2: Identify Relevant Rows
    relevant_row_indices = find_relevant_rows(input_grid_np, dominant_color)
    if relevant_row_indices.size == 0:
        # If no relevant rows, output is empty (size 0)
        return []

    # Step 3: Identify Pure Columns
    pure_column_indices = find_pure_column_indices(input_grid_np, dominant_color, relevant_row_indices)

    # Step 4: Find Largest Contiguous Block Size of Pure Columns
    output_size = find_largest_contiguous_block_size(pure_column_indices)

    # Step 5: Create Output Grid
    output_grid_np = np.full((output_size, output_size), dominant_color, dtype=int)

    # Convert output numpy array back to list of lists
    output_grid = output_grid_np.tolist()

    return output_grid