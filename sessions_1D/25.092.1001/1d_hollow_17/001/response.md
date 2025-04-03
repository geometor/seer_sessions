```python
"""
Modifies a contiguous horizontal block of non-white pixels by keeping only its endpoints and changing the interior pixels to white (0).
If the block has length 1 or 2, it remains unchanged.
Assumes input is a single row (1xN grid).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 1xN grid by hollowing out a contiguous non-white block,
    keeping only the endpoints.

    Args:
        input_grid (np.array): A 1xN numpy array representing the input grid.

    Returns:
        np.array: The transformed 1xN numpy array.
    """
    # Convert input to numpy array if it's not already
    grid = np.array(input_grid)

    # Ensure it's treated as a 1D array for simplicity, assuming 1xN input
    # If it's Nx1, we might need to adjust, but examples are 1xN
    if grid.shape[0] > 1 and grid.shape[1] == 1:
        # Handle Nx1 case by transposing or flattening, let's assume 1xN based on examples
        # For now, we'll assume the input will always be presented as 1xN or effectively 1D
        row = grid.flatten()
    elif grid.shape[0] == 1:
        row = grid[0]
    else:
        # Handle unexpected dimensions or return input if not 1D
        # Based on examples, assume it's always effectively 1D
        # If multiple rows exist, this logic might need refinement
        # For now, let's process the first row if multiple exist, or flatten if shape is weird
        # Safest assumption based *only* on examples: input is always 1xN
        if grid.ndim == 1: # Already a 1D array
             row = grid
        elif grid.shape[0] == 1: # 1xN case
            row = grid[0]
        else:
            # Cannot confidently process non-1D grids with this logic
            print("Warning: Input grid has unexpected dimensions. Processing first row only.")
            row = grid[0]


    # Initialize output_grid as a copy of the input row
    output_row = np.copy(row)

    # Find indices of non-white pixels (value > 0)
    non_white_indices = np.where(row > 0)[0]

    # Check if there are enough non-white pixels to modify (at least 3 for hollowing)
    if len(non_white_indices) >= 3:
        # Determine the start and end indices of the contiguous block
        start_index = np.min(non_white_indices)
        end_index = np.max(non_white_indices)

        # Check if the non-white pixels form a single contiguous block
        # The length of the sequence should match the difference between max and min index + 1
        is_contiguous = len(non_white_indices) == (end_index - start_index + 1)

        if is_contiguous:
            # Change pixels between the start and end indices to white (0)
            # The range is from start_index + 1 up to (but not including) end_index
            for i in range(start_index + 1, end_index):
                output_row[i] = 0
        # If not contiguous, the rule might not apply as interpreted.
        # Based on examples, we assume contiguity. If not, return copy.

    # Reshape the output row back to 1xN grid format to match expected output structure
    # If the original input was 1D, keep it 1D. Check original input ndim.
    if input_grid.ndim == 1:
        return output_row # Return 1D if input was 1D
    else:
        return output_row.reshape(1, -1) # Return 1xN if input was 2D (1xN)
```