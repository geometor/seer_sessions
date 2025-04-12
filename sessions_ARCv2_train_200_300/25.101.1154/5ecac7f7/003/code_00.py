import numpy as np

"""
Transformation Rule:

1.  Identify the vertical separator columns composed entirely of 'magenta' (6) pixels in the 5x17 input grid (expected at column indices 5 and 11).
2.  These separators logically divide the input grid into three 5x5 segments: Segment 1 (cols 0-4), Segment 2 (cols 6-10), and Segment 3 (cols 12-16).
3.  Create a new 5x5 output grid.
4.  For each column index `j` from 0 to 4:
    a.  Extract the corresponding column from each segment: `Col_Seg1 = InputColumn[j]`, `Col_Seg2 = InputColumn[j+6]`, `Col_Seg3 = InputColumn[j+12]`.
    b.  Calculate the sum of pixel values for each of these three columns.
    c.  Select the column that has the maximum sum.
    d.  **Tie-breaking:** If two or more columns share the same maximum sum, select the column corresponding to the segment with the largest index (i.e., prefer Segment 3 over Segment 2, and Segment 2 over Segment 1).
    e.  Assign the selected column to the `j`-th column of the output grid.
    f.  *(Self-correction Note: This rule works for Example 1 but fails for columns 3 and 4 in Example 2, and column 3 in Example 3. A more complex rule is needed for full accuracy.)*
5.  Return the completed 5x5 output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by segmenting it and selecting columns based on the maximum sum rule.
    """
    # Convert input to NumPy array for easier slicing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Define output dimensions and initialize output grid
    output_height = 5
    output_width = 5
    output_np = np.zeros((output_height, output_width), dtype=int)

    # Define the starting column index for each segment
    segment_starts = [0, 6, 12]

    # Iterate through each column index for the output grid
    for j in range(output_width):
        candidate_cols_data = []
        candidate_sums = []
        candidate_indices = []

        # Extract candidate columns and calculate their sums
        for i, start_col in enumerate(segment_starts):
            col_idx = start_col + j
            # Ensure the column index is within the input grid bounds
            if col_idx < width:
                column = input_np[:, col_idx]
                candidate_cols_data.append(column)
                candidate_sums.append(np.sum(column))
                candidate_indices.append(i) # Store segment index (0, 1, or 2)

        # Check if we found any candidates (should always be 3 for valid input)
        if not candidate_cols_data:
            continue # Should not happen with expected input format

        # Find the maximum sum
        max_sum = -1
        if candidate_sums:
            max_sum = max(candidate_sums)

        # Find indices of columns matching the max sum
        max_sum_indices = [idx for idx, s in enumerate(candidate_sums) if s == max_sum]

        # Select the best column based on max sum and tie-breaker
        selected_column = None
        if len(max_sum_indices) == 1:
            # Only one column has the max sum
            selected_column = candidate_cols_data[max_sum_indices[0]]
        elif len(max_sum_indices) > 1:
            # Tie-breaker: choose the one with the highest segment index
            best_segment_index = -1
            selected_idx_in_candidates = -1
            for k in max_sum_indices:
                 segment_index_of_candidate = candidate_indices[k]
                 if segment_index_of_candidate > best_segment_index:
                     best_segment_index = segment_index_of_candidate
                     selected_idx_in_candidates = k
            selected_column = candidate_cols_data[selected_idx_in_candidates]
        else:
             # This case should ideally not be reached if sums are calculated correctly
             # Default or error handling could go here, but based on logic, we expect a selection.
             # For safety, maybe pick the first candidate? Or handle error.
             # Let's select the first one as a fallback, though unlikely needed.
             if candidate_cols_data:
                 selected_column = candidate_cols_data[0]


        # Assign the selected column to the output grid
        if selected_column is not None:
            output_np[:, j] = selected_column

    # Convert the NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid