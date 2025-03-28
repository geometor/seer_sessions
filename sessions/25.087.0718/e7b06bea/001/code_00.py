import numpy as np

"""
Transformation Rule:

1. Initialize the output grid as a copy of the input grid, filled entirely with the background color (white, 0).
2. Identify the gray vertical line in the input grid (assumed to be at column 0). Copy this gray line to column 0 of the output grid.
3. Identify all columns in the input grid, starting from column 1, that contain any colors other than white (0) or gray (5). These are the 'data lines'.
4. Find the minimum column index (`first_data_col`) among these data lines. If no such columns exist, return the output grid with only the gray line copied.
5. Calculate the target starting column (`target_start_col`) for the shifted data lines in the output grid as `first_data_col - 1`.
6. Iterate through the identified data line columns from the input grid, maintaining their relative order. For each data line column found at input index `input_col_idx`, copy its contents (the vertical line of color) to the corresponding output column index `target_start_col + (input_col_idx - first_data_col)`.
7. The final output grid contains the gray line at column 0 and the shifted data lines starting at `target_start_col`. All other cells remain white (0).
"""

def find_data_columns(input_np):
    """
    Identifies columns containing colors other than white (0) or gray (5),
    starting from column index 1.
    Returns the index of the first such column found, and a list of all such column indices.
    """
    height, width = input_np.shape
    data_col_indices = []
    first_data_col = -1

    for c in range(1, width):
        column = input_np[:, c]
        # Check if the column contains any color other than white (0) or gray (5)
        if np.any((column != 0) & (column != 5)):
            data_col_indices.append(c)
            if first_data_col == -1:
                first_data_col = c
                
    return first_data_col, data_col_indices

def transform(input_grid):
    """
    Shifts the block of non-white, non-gray vertical lines (data lines)
    one column to the left, maintaining the gray line at column 0.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with white (0)
    output_np = np.zeros_like(input_np)

    # Copy the gray reference line (column 0) if it exists
    if width > 0:
         # Assuming the gray line is always at column 0 based on examples
         # A more robust check could be added here if needed
         output_np[:, 0] = input_np[:, 0]

    # Find the data line columns and the index of the first one
    first_data_col, data_col_indices = find_data_columns(input_np)

    # If data lines were found, shift them
    if first_data_col != -1:
        # Calculate the target starting column for the shifted block
        target_start_col = first_data_col - 1
        
        # Check if target column is valid (should be >= 1 as first_data_col >= 1)
        if target_start_col >= 0: # Actually >= 1 if we want to avoid overwriting column 0, but the examples show it can be adjacent. Let's use >= 0. If target_start_col == 0, it overwrites the initial white fill, which is fine.
             # Iterate through the identified data columns and copy them to the new position
            for i, input_col_idx in enumerate(data_col_indices):
                output_col_idx = target_start_col + i
                # Ensure we don't write out of bounds (though logic implies this shouldn't happen if input is valid)
                if output_col_idx < width:
                     output_np[:, output_col_idx] = input_np[:, input_col_idx]
        else:
             # This case (first_data_col = 0) shouldn't happen based on find_data_columns starting search at 1.
             # If it could, add specific handling here.
             pass

    # Convert back to list of lists if required by the environment, otherwise return numpy array
    return output_np.tolist()