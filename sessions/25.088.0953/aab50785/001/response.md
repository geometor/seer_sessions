```python
import numpy as np
from typing import List, Tuple

"""
The transformation identifies rows in the input grid that contain exactly two non-overlapping pairs of horizontally adjacent azure pixels (8 8). 
For each such identified row, it extracts the segment of the row located strictly between the inner azure pixels of the two pairs. 
The final output grid consists of these extracted segments stacked vertically in the order they were found in the input grid.

For example, if a row looks like `... A B 8 8 C D E 8 8 F G ...`, the extracted segment will be `C D E`.
The start index of the segment is the column index of the second '8' of the first pair, plus one.
The end index of the segment is the column index of the first '8' of the second pair.
"""

def find_horizontal_pairs(row: np.ndarray, color: int) -> List[int]:
    """Finds the starting column indices of horizontal pairs of a given color."""
    pair_indices = []
    for c in range(len(row) - 1):
        if row[c] == color and row[c+1] == color:
            pair_indices.append(c)
    return pair_indices

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Extracts segments from rows containing exactly two '8 8' pairs.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the output grid, formed by stacking the
        extracted segments.
    """
    output_rows = []
    delimiter_color = 8 # Azure

    # Iterate through each row of the input grid
    for r in range(input_grid.shape[0]):
        row = input_grid[r, :]
        
        # Find the starting indices of all horizontal '8 8' pairs in the current row
        pair_start_indices = find_horizontal_pairs(row, delimiter_color)

        # Check if exactly two pairs were found
        if len(pair_start_indices) == 2:
            # Get the starting index of the first pair
            first_pair_start_col = pair_start_indices[0]
            # Get the starting index of the second pair
            second_pair_start_col = pair_start_indices[1]

            # Determine the column indices for extraction
            # Start column is after the second '8' of the first pair
            start_extract_col = first_pair_start_col + 2
            # End column is before the first '8' of the second pair
            end_extract_col = second_pair_start_col

            # Extract the segment if the indices are valid (start < end)
            if start_extract_col < end_extract_col:
                extracted_segment = row[start_extract_col:end_extract_col]
                output_rows.append(extracted_segment)

    # If no matching rows were found, return an empty grid or handle as appropriate
    # Based on examples, if output_rows is not empty, stack them
    if not output_rows:
        # Returning an empty array shape (0,0) might be problematic depending on framework.
        # Let's return a 1x1 grid with 0 if nothing found, although examples suggest 
        # something is always found. If test cases show empty output possibility, adjust this.
        # Based on ARC viewer, empty is usually represented as 0x0 or 1x1 black (0)
         return np.array([[]], dtype=int) # Represents 0 height grid

    # Convert the list of extracted rows into a numpy array
    # Ensure all rows have the same length if stacking; examples suggest they do.
    output_grid = np.array(output_rows, dtype=int)

    return output_grid

```