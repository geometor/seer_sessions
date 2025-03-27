import numpy as np
from typing import List, Dict, Tuple

"""
Processes a grid by identifying columns containing gray pixels (5).
These columns are ranked based first on the count of gray pixels (ascending)
and secondarily by their column index (ascending).
The gray pixels in each ranked column are then replaced with a specific color
based on their rank: Rank 1 -> Yellow (4), Rank 2 -> Green (3),
Rank 3 -> Red (2), Rank 4 -> Blue (1). All other pixels remain unchanged.
Assumes exactly four such columns exist.
"""

def _find_and_rank_gray_columns(input_grid: np.ndarray) -> List[Dict]:
    """
    Identifies columns containing gray pixels, counts them, and ranks the columns.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A sorted list of dictionaries, each containing 'index' (column index)
        and 'count' (number of gray pixels) for relevant columns. The list is
        sorted by count (ascending) and then index (ascending).
    """
    gray_columns_info = []
    height, width = input_grid.shape
    gray_color = 5

    # 1. Identify Target Columns: Find columns with gray pixels and count them.
    for col_idx in range(width):
        column = input_grid[:, col_idx]
        gray_count = np.sum(column == gray_color)
        if gray_count > 0:
            gray_columns_info.append({'index': col_idx, 'count': gray_count})

    # 2. Rank Columns: Sort by count (asc) then index (asc).
    #    The lambda function returns a tuple for sorting: (count, index)
    sorted_columns = sorted(gray_columns_info, key=lambda x: (x['count'], x['index']))

    return sorted_columns

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    height = input_np.shape[0]
    gray_color = 5

    # Steps 1 & 2: Identify and Rank gray columns
    ranked_columns = _find_and_rank_gray_columns(input_np)

    # 3. Determine Replacement Colors based on rank (0-based index from sorted list)
    #    Rank 1 (index 0) -> Yellow (4)
    #    Rank 2 (index 1) -> Green (3)
    #    Rank 3 (index 2) -> Red (2)
    #    Rank 4 (index 3) -> Blue (1)
    #    We assume there will always be exactly 4 columns based on examples.
    rank_to_color = {
        0: 4, # Rank 1 -> Yellow
        1: 3, # Rank 2 -> Green
        2: 2, # Rank 3 -> Red
        3: 1  # Rank 4 -> Blue
    }

    # 4. Apply Transformation: Iterate through ranked columns and replace gray pixels
    for rank_idx, col_info in enumerate(ranked_columns):
        col_index = col_info['index']
        # Get the replacement color for the current rank
        replacement_color = rank_to_color.get(rank_idx)

        if replacement_color is not None:
            # Iterate through rows of this specific column
            for row_idx in range(height):
                # Check if the pixel in the *original* input grid was gray
                if input_np[row_idx, col_index] == gray_color:
                    # Replace the gray pixel with the determined color in the output grid
                    output_grid[row_idx, col_index] = replacement_color
        # else: handle cases where rank_idx might be outside 0-3 if assumption is wrong (optional, not needed based on examples)

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()