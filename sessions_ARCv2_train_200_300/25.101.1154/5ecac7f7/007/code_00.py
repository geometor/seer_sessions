import numpy as np

"""
Transformation Rule:

1.  **Identify Separators:** Locate the two vertical columns in the 5x17 input grid composed entirely of 'magenta' (6) pixels (expected at indices 5 and 11).
2.  **Segment Input:** Divide the input grid using these separators into three distinct 5x5 pixel segments: Segment 0 (columns 0-4), Segment 1 (columns 6-10), and Segment 2 (columns 12-16).
3.  **Initialize Output:** Create a new, empty 5x5 output grid.
4.  **Process Columns:** Iterate through each column index `j` from 0 to 4 to construct the output grid:
    a.  **Extract Candidates:** Identify the three corresponding columns from the input: `Col_0 = InputColumn[j]`, `Col_1 = InputColumn[j+6]`, `Col_2 = InputColumn[j+12]`.
    b.  **Apply Selection Rule (Hypothesized):**
        i.  Calculate the sum of pixel values for `Col_0`, `Col_1`, and `Col_2`.
        ii. Identify the column(s) with the maximum sum.
        iii. If only one column has the maximum sum, select that column.
        iv. If multiple columns share the maximum sum, select the one from the segment with the highest index (i.e., prefer `Col_2` over `Col_1`, and `Col_1` over `Col_0`).
    c.  **Assign Output Column:** Place the selected column's data into the `j`-th column of the output grid.
5.  **Return Output:** Return the fully constructed 5x5 output grid.

**(Caveat):** The selection rule (4b) described above is the best simple hypothesis derived but is known to produce incorrect results for specific columns in the training examples (column 3 and 4 in Example 2; column 3 in Example 3). The actual rule required for a complete solution is likely more complex or conditional than this hypothesized rule.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by segmenting it and selecting columns based on the hypothesized maximum sum rule with max segment index tie-breaking.
    """
    # Convert input to NumPy array for easier slicing and calculations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape # Expected height=5, width=17

    # Define output dimensions and initialize output grid with zeros
    output_height = 5
    output_width = 5
    output_np = np.zeros((output_height, output_width), dtype=int)

    # Define the starting column index for each logical segment (0-based)
    # Segment 0 starts at col 0, Segment 1 at col 6, Segment 2 at col 12
    segment_starts = [0, 6, 12]

    # Iterate through each column index (j) for the 5x5 output grid
    for j in range(output_width):
        candidate_cols_data = [] # To store the actual column data (NumPy arrays)
        candidate_sums = []      # To store the sum of each candidate column
        candidate_indices = []   # To store the segment index (0, 1, or 2) of each candidate

        # Step 4a: Extract Candidates and calculate sums from each segment
        for i, start_col in enumerate(segment_starts):
            col_idx = start_col + j # Calculate the corresponding column index in the input grid
            # Ensure the column index is within the input grid bounds
            if col_idx < width:
                column = input_np[:, col_idx] # Extract the column using numpy slicing
                candidate_cols_data.append(column)
                candidate_sums.append(np.sum(column)) # Calculate sum using numpy
                candidate_indices.append(i) # Store original segment index (0, 1, or 2)

        # Ensure we actually found candidates (should always be 3 for valid 5x17 input)
        if not candidate_cols_data:
            # This case should not happen with the expected input format.
            # If it did, the output column would remain zeros.
            continue # Move to the next output column index j

        # Step 4b: Apply Selection Rule (Hypothesized)
        selected_column = None # Initialize variable to hold the chosen column data

        # Find the maximum sum among the candidates
        max_sum = -1 # Initialize to a value lower than any possible sum
        if candidate_sums:
            max_sum = max(candidate_sums)

        # Find the indices (in the candidate_*** lists) of columns that match the max sum
        max_sum_indices_in_candidates = [idx for idx, s in enumerate(candidate_sums) if s == max_sum]

        # Determine the selected column based on max sum and tie-breaker
        if len(max_sum_indices_in_candidates) == 1:
            # Step 4b.iii: Only one column has the maximum sum - select it
            selected_idx = max_sum_indices_in_candidates[0]
            selected_column = candidate_cols_data[selected_idx]
        elif len(max_sum_indices_in_candidates) > 1:
            # Step 4b.iv: Tie-breaker needed: choose the one with the highest original segment index
            best_segment_index = -1 # Track the highest segment index found so far among tied candidates
            selected_idx_in_candidates = -1 # Track the index in candidate lists corresponding to the best choice

            # Iterate through the indices of the tied candidates
            for k in max_sum_indices_in_candidates:
                 # Get the original segment index (0, 1, or 2) for this candidate
                 segment_index_of_candidate = candidate_indices[k]
                 # If this segment index is higher than the current best, update best
                 if segment_index_of_candidate > best_segment_index:
                     best_segment_index = segment_index_of_candidate
                     selected_idx_in_candidates = k # Store the index of this best candidate

            # Select the column data corresponding to the tie-breaker winner
            if selected_idx_in_candidates != -1:
                 selected_column = candidate_cols_data[selected_idx_in_candidates]
            else:
                 # Fallback: Should not happen if tie-breaking logic is sound,
                 # but select the first tied candidate just in case.
                 selected_column = candidate_cols_data[max_sum_indices_in_candidates[0]]

        else:
             # This case (no candidates matching max_sum) should not be logically reachable
             # if max_sum was derived from non-empty candidate_sums.
             # If it somehow occurs (e.g., empty input?), select the first candidate as a fallback.
             if candidate_cols_data:
                 selected_column = candidate_cols_data[0]


        # Step 4c: Assign Output Column
        # Place the selected column's data into the j-th column of the output grid
        if selected_column is not None:
            output_np[:, j] = selected_column

    # Step 5: Return Output
    # Convert the final NumPy array output grid back to a standard list of lists format
    output_grid = output_np.tolist()

    return output_grid