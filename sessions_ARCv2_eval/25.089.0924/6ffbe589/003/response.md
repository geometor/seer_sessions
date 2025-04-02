```python
import numpy as np
import itertools

"""
Identify the bounding box corresponding to the primary cluster of non-white pixels 
by analyzing projections. Find the longest contiguous range of rows containing 
at least one non-white pixel, and the longest contiguous range of columns 
containing at least one non-white pixel. The intersection of these ranges defines 
the bounding box. Extract the subgrid from the input corresponding to this 
bounding box.
"""

def find_longest_contiguous_run(counts):
    """
    Finds the start and end indices of the longest contiguous run of non-zero values.
    If multiple runs have the same max length, returns the first one found.

    Args:
        counts (np.array): A 1D array of counts or indicators (e.g., 0 or 1).

    Returns:
        tuple: (start_index, end_index) of the longest run, or (0, -1) if no non-zero elements.
               The end_index is inclusive.
    """
    max_len = 0
    best_start = 0
    best_end = -1 # Use -1 to indicate no run found yet

    current_len = 0
    current_start = 0

    for i, count in enumerate(counts):
        if count > 0:
            if current_len == 0:
                current_start = i
            current_len += 1
        else:
            if current_len > max_len:
                max_len = current_len
                best_start = current_start
                best_end = i - 1 # Run ended at previous index
            current_len = 0 # Reset run

    # Check if the longest run extends to the end of the array
    if current_len > max_len:
        max_len = current_len
        best_start = current_start
        best_end = len(counts) - 1

    return best_start, best_end


def transform(input_grid):
    """
    Extracts the subgrid corresponding to the primary cluster of non-white pixels.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the cropped output grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Handle empty input
    if rows == 0 or cols == 0:
        return [[]]

    # Find non-white pixels
    non_white_pixels = np.argwhere(input_np != 0)

    # Handle case with no non-white pixels
    if non_white_pixels.shape[0] == 0:
        # Return based on expected behavior - maybe empty grid? Or original?
        # Examples imply non-empty output. Let's assume empty grid.
        return [[]] 

    # Project onto rows: count non-white pixels per row
    row_counts = np.zeros(rows, dtype=int)
    unique_rows = np.unique(non_white_pixels[:, 0])
    for r in unique_rows:
        row_counts[r] = 1 # Just need to know if row has > 0 non-white pixels
        
    # Find longest contiguous run of rows with non-white pixels
    min_r, max_r = find_longest_contiguous_run(row_counts)

    # Project onto columns: count non-white pixels per column
    col_counts = np.zeros(cols, dtype=int)
    unique_cols = np.unique(non_white_pixels[:, 1])
    for c in unique_cols:
        col_counts[c] = 1 # Just need to know if col has > 0 non-white pixels

    # Find longest contiguous run of columns with non-white pixels
    min_c, max_c = find_longest_contiguous_run(col_counts)
    
    # Check if valid ranges were found
    if max_r < min_r or max_c < min_c:
        # This shouldn't happen if there are non-white pixels, but as a safeguard
        return [[]] 

    # Crop the input grid using the bounding box coordinates
    # Slicing is [start_row : end_row+1, start_col : end_col+1]
    output_np = input_np[min_r : max_r + 1, min_c : max_c + 1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid
```