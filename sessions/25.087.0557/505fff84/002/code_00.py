import numpy as np
# from typing import List, Tuple # Use numpy types

def transform_np(input_grid_np: np.ndarray) -> np.ndarray:
    output_rows = []
    # Iterate through each row of the input numpy array
    for row in input_grid_np:
        # Find indices using numpy's where function
        blue_indices = np.where(row == 1)[0] # np.where returns a tuple of arrays, take the first element
        azure_indices = np.where(row == 8)[0]

        # Check if both arrays are non-empty
        if blue_indices.size > 0 and azure_indices.size > 0:
            # Get the first blue and azure index found
            blue_col = blue_indices[0]
            azure_col = azure_indices[0]

            min_col = min(blue_col, azure_col)
            max_col = max(blue_col, azure_col)

            # Extract the segment using numpy slicing
            segment = row[min_col + 1 : max_col]

            # Only add non-empty segments
            if segment.size > 0:
                 # Store segment as a standard list or 1D numpy array?
                 # Let's keep as numpy array for now
                 output_rows.append(segment)

    # Stack the collected segments vertically
    # Handle the case where no segments were found
    if not output_rows:
        # Determine output shape? Maybe 0x0? Or based on input?
        # ARC often expects an empty grid representation.
        # Returning an empty list might be converted to an empty array by the caller.
        # Or return np.empty((0,0), dtype=int) ? Let's try empty list first, simpler.
        # If output_rows contains arrays of different lengths, vstack fails.
        # We need to handle potentially jagged arrays.
        # The original problem description implies segments might have different lengths.
        # Stack these extracted segments vertically... implies they should form a grid.
        # This suggests segments SHOULD have the same length, or padding is needed, or the NL description needs adjustment.

        # Let's re-read the original description: "Stack these extracted segments vertically"
        # This implies the output should be a rectangular grid.
        # Does this mean all extracted segments must have the same length?
        # Let's re-examine the (missing) examples mentally. If segments can have different lengths, how are they stacked?
        # Maybe the task guarantees segments will have the same length? Or maybe the output is *not* a simple stacking, but something else?

        # Let's stick to the original List[List[int]] output format, as requested by the type hints,
        # and assume the comparison error is in the test harness.
        # The original code produced List[List[int]].

        # Revert: Keep the original code structure but ensure it handles NumPy inputs gracefully if needed.
        # The original code *should* work if the input `input_grid` can be iterated row by row,
        # and each `row` supports enumeration and slicing. NumPy arrays support this.
        # The `find_indices` returns lists. The check `if blue_indices and azure_indices:` works on lists.
        # The slicing `row[min_col + 1 : max_col]` works on lists and NumPy arrays.
        # The result `segment` will be a list if `row` is a list, and a NumPy array if `row` is a NumPy array.
        # Appending NumPy arrays to `output_rows` might create a list of arrays.
        # This might be the issue. Let's ensure `segment` is converted to a list before appending.
