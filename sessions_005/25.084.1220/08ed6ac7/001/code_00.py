import numpy as np
from typing import List, Tuple, Dict

"""
Processes a grid by identifying columns containing gray pixels (5).
These columns are ranked based first on the count of gray pixels (ascending)
and secondarily by their column index (descending).
The gray pixels in each ranked column are then replaced with a specific color
based on their rank: Rank 1 -> Yellow (4), Rank 2 -> Blue (1),
Rank 3 -> Green (3), Rank 4 -> Red (2). All other pixels remain unchanged.
Assumes exactly four such columns exist.
"""

def _find_and_count_gray_columns(input_grid: np.ndarray) -> List[Dict]:
    """
    Identifies columns containing gray pixels and counts them.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, each containing 'index' (column index)
        and 'count' (number of gray pixels) for relevant columns.
    """
    gray_columns_info = []
    height, width = input_grid.shape
    gray_color = 5

    for col_idx in range(width):
        column = input_grid[:, col_idx]
        gray_count = np.sum(column == gray_color)
        if gray_count > 0:
            gray_columns_info.append({'index': col_idx, 'count': gray_count})

    return gray_columns_info

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
    height, width = input_np.shape
    gray_color = 5

    # 1. Identify columns with gray pixels and count them
    gray_columns_data = _find_and_count_gray_columns(input_np)

    # 2. Sort the columns: primary key = count (ascending), secondary key = index (descending)
    #    The lambda function returns a tuple for sorting: (count, -index)
    #    Using -index achieves descending order for the index tie-breaker.
    sorted_columns = sorted(gray_columns_data, key=lambda x: (x['count'], -x['index']))

    # 3. Define the rank-to-color mapping (using 0-based index from sorted list)
    #    Rank 1 (index 0) -> Yellow (4)
    #    Rank 2 (index 1) -> Blue (1)
    #    Rank 3 (index 2) -> Green (3)
    #    Rank 4 (index 3) -> Red (2)
    #    We assume there will always be exactly 4 columns based on examples.
    rank_to_color = {
        0: 4, # Rank 1 -> Yellow
        1: 1, # Rank 2 -> Blue
        2: 3, # Rank 3 -> Green
        3: 2  # Rank 4 -> Red
    }

    # 4. Iterate through sorted columns, determine replacement color, and update output grid
    for rank_idx, col_info in enumerate(sorted_columns):
        col_index = col_info['index']
        replacement_color = rank_to_color.get(rank_idx)

        if replacement_color is not None:
            # Iterate through rows of this specific column
            for row_idx in range(height):
                # Check if the original pixel was gray
                if input_np[row_idx, col_index] == gray_color:
                    # Replace the gray pixel with the determined color in the output grid
                    output_grid[row_idx, col_index] = replacement_color
        # else: handle cases where rank_idx might be outside 0-3 if assumption is wrong (optional)

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()