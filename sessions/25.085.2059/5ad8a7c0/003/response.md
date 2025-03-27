```python
import numpy as np

"""
Transformation Rule:

1.  **Global Check:** Examine the entire input grid. If any row contains two red pixels (value 2) immediately adjacent horizontally (`[..., 2, 2, ...]`), stop and output the input grid unchanged.
2.  **Identify Candidates:** If the global check passes, proceed to analyze each row independently:
    *   Find all rows containing exactly two red pixels.
    *   For each such row, check if the pixels strictly between the two red pixels are all white (value 0).
    *   Rows satisfying both conditions are "candidate rows". Ensure the red pixels are not adjacent (i.e., the segment between them exists).
3.  **Classify Candidates:** Categorize the candidate rows identified in step 2:
    *   If a candidate row's red pixels are in the first column (index 0) AND the last column (index `width-1`), it is a "boundary candidate".
    *   Otherwise (if at least one red pixel is not on the edge column), it is an "internal candidate".
4.  **Apply Filling Logic:**
    *   Determine if any "internal candidates" were found in step 3.
    *   **If internal candidates exist:** Modify the grid by filling the segment (between the two red pixels) with red (value 2) *only* for the "internal candidates". Do not modify "boundary candidates".
    *   **If no internal candidates exist:** Modify the grid by filling the segment (between the two red pixels) with red (value 2) for *all* "boundary candidates" (if any exist).
5.  **Output:** Output the modified grid. Rows that were not identified as candidates to be filled remain unchanged from the input.
"""

def has_adjacent_reds(grid: np.ndarray) -> bool:
    """Checks if any row in the grid contains adjacent red pixels."""
    height, width = grid.shape
    for r in range(height):
        for c in range(width - 1):
            if grid[r, c] == 2 and grid[r, c + 1] == 2:
                return True
    return False

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    Fills horizontal segments between pairs of red pixels in a row with red,
    subject to conditions involving adjacent reds and whether pairs are internal or boundary.
    """
    # 1. Global Check for adjacent red pixels
    if has_adjacent_reds(input_grid):
        return input_grid.copy() # If inhibitor found, return the input grid unchanged

    # Initialize output_grid as a copy of the input
    output_grid = input_grid.copy()
    height, width = output_grid.shape

    internal_candidates = [] # Stores (row_index, col1, col2)
    boundary_candidates = [] # Stores (row_index, col1, col2)

    # 2. Identify and 3. Classify Candidates
    for r in range(height):
        row = output_grid[r, :]
        red_indices = np.where(row == 2)[0]

        # Check if the row contains exactly two red pixels
        if len(red_indices) == 2:
            c1, c2 = red_indices[0], red_indices[1] # c1 < c2 guaranteed by np.where

            # Check if the segment between c1 and c2 exists and is non-empty
            if c1 + 1 < c2:
                # Extract the segment strictly between the two red pixels
                segment = row[c1 + 1 : c2]

                # Check if all pixels in the segment are white (0)
                if np.all(segment == 0):
                    # This is a candidate row
                    # Classify as boundary or internal
                    if c1 == 0 and c2 == width - 1:
                        boundary_candidates.append((r, c1, c2))
                    else:
                        internal_candidates.append((r, c1, c2))

    # 4. Apply Filling Logic
    if internal_candidates: # If internal candidates exist
        # Fill segments only for internal candidates
        for r, c1, c2 in internal_candidates:
            output_grid[r, c1 + 1 : c2] = 2
    elif boundary_candidates: # Else if only boundary candidates exist (or no candidates)
        # Fill segments for boundary candidates
        for r, c1, c2 in boundary_candidates:
             output_grid[r, c1 + 1 : c2] = 2
    # If neither list has candidates, the grid remains unchanged (as initialized)

    # 5. Output
    return output_grid
```