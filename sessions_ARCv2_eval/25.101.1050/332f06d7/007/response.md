```python
"""
Transformation Rule:

The transformation rule depends on the presence or absence of a 3x3 block of red (2) pixels in the input grid.

1.  **Check for 3x3 Red Block:** Scan the input grid to determine if any 3x3 area consists entirely of red (2) pixels.

2.  **Conditional Transformation:**
    *   **If a 3x3 red block exists (Branch 1):**
        a.  Find the top-left coordinate `(Wr, Wc)` of the first occurrence (scanning top-to-bottom, left-to-right) of a 3x3 block of white (0) pixels in the input grid.
        b.  If no 3x3 white block is found, return the input grid unchanged (assumption based on lack of counter-examples).
        c.  If a 3x3 white block is found at `(Wr, Wc)`:
            i.  Initialize the output grid by copying the input grid.
            ii. Change all white (0) pixels in the output grid to blue (1). (Leave red(2), blue(1), green(3) as initially copied).
            iii. Calculate the target top-left coordinate for a new white block: `Tr = Wr - 6`, `Tc = Wc + 6`.
            iv. Check if the target coordinates `(Tr, Tc)` and the resulting 3x3 block area (`Tr` to `Tr+2`, `Tc` to `Tc+2`) are within the grid boundaries.
            v.  If the target block is within bounds, set the 3x3 area in the output grid starting at `(Tr, Tc)` entirely to white (0), overwriting any previous values.
            vi. Return this modified output grid.

    *   **If no 3x3 red block exists (Branch 2):**
        a.  Initialize the output grid by copying the input grid.
        b.  Change all white (0) pixels in the output grid to blue (1).
        c.  Change all red (2) pixels in the output grid to white (0).
        d.  Leave blue (1) and green (3) pixels unchanged (as they were copied initially).
        e.  Return this modified output grid.
        f.  (Note: This rule correctly handles examples 1 and 4. It does not account for the specific blue(1)-to-white(0) 2x2 block transformation observed only in training example 2's expected output, as the trigger for that specific change is not generalizable from the provided examples).
"""

import numpy as np
from typing import List, Optional, Tuple

# --- Helper Functions ---

def find_nxn_block(grid: np.ndarray, n: int, color: int) -> bool:
    """Checks if an n x n block of the specified color exists anywhere in the grid."""
    height, width = grid.shape
    if height < n or width < n:
        return False
    for r in range(height - n + 1):
        for c in range(width - n + 1):
            if np.all(grid[r:r+n, c:c+n] == color):
                return True
    return False

def find_first_nxn_block(grid: np.ndarray, n: int, color: int) -> Optional[Tuple[int, int]]:
    """Finds the top-left coordinates of the first n x n block of the specified color, scanning top-to-bottom, left-to-right."""
    height, width = grid.shape
    if height < n or width < n:
        return None
    for r in range(height - n + 1):
        for c in range(width - n + 1):
            if np.all(grid[r:r+n, c:c+n] == color):
                return (r, c)
    return None

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the presence of a 3x3 red block.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    block_size = 3

    # --- Step 1: Check for 3x3 Red Block ---
    has_red_3x3 = find_nxn_block(input_array, block_size, 2)

    # --- Step 2: Conditional Transformation ---
    if has_red_3x3:
        # --- Branch 1: 3x3 Red Block Exists ---

        # Find the location of the first 3x3 white (0) block in the input
        white_block_loc = find_first_nxn_block(input_array, block_size, 0)

        # If no 3x3 white block is found, return the original grid (assumption)
        if white_block_loc is None:
            return input_array.tolist()

        # If found, proceed with transformation
        Wr, Wc = white_block_loc

        # Initialize the output grid as a copy of the input
        output_array = np.copy(input_array)

        # Perform initial global transformation: white (0) -> blue (1)
        output_array[input_array == 0] = 1

        # Calculate the target location for the output white block
        Tr = Wr - 6
        Tc = Wc + 6

        # Check if the target location and block are within grid bounds
        if 0 <= Tr < height - block_size + 1 and 0 <= Tc < width - block_size + 1:
            # Create the 3x3 white (0) block at the target location, overwriting
            output_array[Tr : Tr + block_size, Tc : Tc + block_size] = 0

    else:
        # --- Branch 2: No 3x3 Red Block Exists ---

        # Initialize the output grid as a copy of the input
        output_array = np.copy(input_array)

        # Change white (0) to blue (1)
        output_array[input_array == 0] = 1

        # Change red (2) to white (0)
        output_array[input_array == 2] = 0

        # Blue(1) and Green(3) remain unchanged because they were copied initially.
        # Note: This branch does not account for the specific blue->white change in Example 2.

    # Convert the final NumPy array back to a list of lists and return
    return output_array.tolist()
```