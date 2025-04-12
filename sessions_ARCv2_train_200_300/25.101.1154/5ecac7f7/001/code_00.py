import numpy as np
from collections import Counter

"""
The transformation operates on a 5x17 input grid and produces a 5x5 output grid.

1.  **Segmentation**: The input grid is divided into three 5x5 segments using vertical magenta (6) separators at columns 5 and 11.
    - Segment 1: Columns 0-4
    - Segment 2: Columns 6-10
    - Segment 3: Columns 12-16

2.  **Column Selection**: The output grid is constructed column by column (index j from 0 to 4). For each output column `j`, the corresponding columns from the three input segments (input columns `j`, `j+6`, and `j+12`) are compared.

3.  **Selection Rule**: The column with the maximum sum of pixel values is selected.
    - **Tie-breaking**: If two or more columns share the same maximum sum, the column from the segment with the highest index (Segment 3 > Segment 2 > Segment 1) is chosen.

4.  **Output Construction**: The selected column becomes the `j`-th column of the 5x5 output grid.
"""

def calculate_sum(column: list[int]) -> int:
    """Calculates the sum of values in a list (column)."""
    return sum(column)

def select_column(cols: list[tuple[int, list[int]]]) -> list[int]:
    """
    Selects one column from a list of candidate columns based on the max sum rule.

    Args:
        cols: A list of tuples, where each tuple is (segment_index, column_data).
              Example: [(0, [col1_data]), (1, [col2_data]), (2, [col3_data])]

    Returns:
        The selected column data (list of ints).
    """
    max_sum = -1
    best_col_data = None
    best_segment_index = -1

    # Calculate sums for each column
    col_sums = [(idx, calculate_sum(data)) for idx, data in cols]

    # Find the maximum sum
    max_sum = max(s for idx, s in col_sums)

    # Find candidate columns with the maximum sum
    candidates = [(idx, data) for (idx, data), (_, s) in zip(cols, col_sums) if s == max_sum]

    # Apply tie-breaker (highest segment index)
    if len(candidates) == 1:
        best_col_data = candidates[0][1]
    else:
        # Find the candidate with the maximum segment index
        max_idx = -1
        for idx, data in candidates:
            if idx > max_idx:
                max_idx = idx
                best_col_data = data

    return best_col_data


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on segmenting and selecting columns by max sum.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_height = 5
    output_width = 5

    # Initialize the output grid (e.g., with zeros)
    output_np = np.zeros((output_height, output_width), dtype=int)

    # Define segment column start indices
    segment_starts = [0, 6, 12]

    # Iterate through each column index of the output grid
    for j in range(output_width):
        # Extract corresponding columns from each segment
        candidate_cols = []
        for i, start_col in enumerate(segment_starts):
            col_idx = start_col + j
            # Ensure column index is within bounds (should be for 5x17 -> 5x5)
            if col_idx < width:
                 # Get column data as a list
                column_data = input_np[:, col_idx].tolist()
                candidate_cols.append((i, column_data)) # Store segment index (0, 1, or 2) and data

        # Select the best column based on the defined rule
        if candidate_cols:
            selected_col = select_column(candidate_cols)
            # Assign the selected column to the output grid
            output_np[:, j] = selected_col
        else:
             # Handle cases where columns might not exist (defensive programming)
             pass


    # Convert the result back to a list of lists
    output_grid = output_np.tolist()

    return output_grid