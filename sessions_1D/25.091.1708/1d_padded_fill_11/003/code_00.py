import numpy as np
from collections import defaultdict
from typing import List, Tuple, Optional

"""
Processes the input grid row by row.
For each row:
1. Identifies all non-white pixels and groups their column indices by color.
2. Counts how many distinct colors appear exactly twice in the row.
3. If exactly one color (C) appears exactly twice:
    a. Finds the column indices (col1, col2, where col1 < col2) of these two pixels.
    b. Fills the segment of the row strictly between col1 and col2 (columns col1 + 1 to col2 - 1) with color C.
4. Otherwise (if no color appears exactly twice, or multiple colors do), the row remains unchanged.
The output grid is initially a copy of the input grid, and modifications are applied directly to the output grid's rows.
"""

def analyze_row(row: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Analyzes a single row to find if there is exactly one color
    that appears exactly twice.

    Args:
        row (np.ndarray): A 1D numpy array representing a row of the grid.

    Returns:
        Optional[Tuple[int, int, int]]: A tuple (color, col1, col2) if the
                                         condition is met, otherwise None.
                                         col1 and col2 are the sorted indices.
    """
    non_white_pixels = defaultdict(list)
    for c, pixel_color in enumerate(row):
        if pixel_color != 0:  # 0 is white/background
            non_white_pixels[pixel_color].append(c)

    # Find colors that appear exactly twice
    colors_with_two_pixels = []
    for color, indices in non_white_pixels.items():
        if len(indices) == 2:
            colors_with_two_pixels.append((color, sorted(indices))) # Store color and sorted indices

    # Check if exactly one such color exists
    if len(colors_with_two_pixels) == 1:
        color, indices = colors_with_two_pixels[0]
        return color, indices[0], indices[1]
    else:
        return None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on filling between pairs of identical
    non-white pixels in each row, if that pair is unique for its color count.

    Args:
        input_grid (List[List[int]]): The input grid.

    Returns:
        List[List[int]]: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    rows, cols = input_grid_np.shape

    # Iterate through each row of the input grid
    for r in range(rows):
        current_row = input_grid_np[r, :]

        # Analyze the row to find if the specific pair condition is met
        analysis_result = analyze_row(current_row)

        # If a unique pair satisfying the condition is found
        if analysis_result is not None:
            fill_color, col1, col2 = analysis_result

            # Fill the segment in the output grid row
            # range(col1 + 1, col2) covers indices strictly between col1 and col2
            if col1 + 1 < col2: # Ensure there's actually space to fill
                 output_grid[r, col1 + 1 : col2] = fill_color
            # If col1 + 1 == col2, there are no pixels between them, so nothing to fill.

        # Else (no unique pair condition met), the row in output_grid
        # remains unchanged (as it was initially copied).

    # Convert the result back to list of lists
    return output_grid.tolist()