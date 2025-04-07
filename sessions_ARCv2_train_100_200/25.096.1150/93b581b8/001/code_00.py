import numpy as np

"""
Transformation Rule Description:

1.  **Identify Input Block:** Locate the 2x2 block of non-zero integers within the input 6x6 grid. Let the top-left corner of this block be at coordinates (r, c). Let the values in the block be:
    A = input_grid[r][c]
    B = input_grid[r][c+1]
    C = input_grid[r+1][c]
    D = input_grid[r+1][c+1]

2.  **Initialize Output:** Create an output grid, initially identical to the input grid.

3.  **Generate Corner Patterns:** Modify the output grid by adding patterns in the corners. The shape, location, and value of these patterns depend on the coordinates (r, c) of the input block.

    *   **Case 1: Input block at (1, 1)** (i.e., r=1, c=1)
        *   Top-Left: Place value D at (0, 0).
        *   Top-Right: Place value C in cells (0, 3) and (0, 4).
        *   Bottom-Left: Place value B in cells (3, 0) and (4, 0).
        *   Bottom-Right: Place value A in a 2x2 block starting at (3, 3).

    *   **Case 2: Input block at (2, 2)** (i.e., r=2, c=2)
        *   Top-Left: Place value D in a 2x2 block starting at (0, 0).
        *   Top-Right: Place value C in a 2x2 block starting at (0, 4).
        *   Bottom-Left: Place value B in a 2x2 block starting at (4, 0).
        *   Bottom-Right: Place value A in a 2x2 block starting at (4, 4).

4.  **Return Result:** The modified grid is the final output.
"""

def find_block_location(grid_np: np.ndarray) -> tuple[int, int] | None:
    """Finds the top-left corner (r, c) of the 2x2 non-zero block."""
    h, w = grid_np.shape
    for r in range(h - 1):
        for c in range(w - 1):
            # Check if the top-left element is non-zero
            # and if the sum of the 2x2 block is non-zero (handles blocks with some zeros)
            # More robustly, check if at least one element in the 2x2 block is non-zero
            # And crucially, check if the surrounding area (if applicable) is zero
            # to ensure we find the *only* non-zero block.
            # For this specific problem, simply finding the first non-zero element
            # that can be a top-left of a non-zero block seems sufficient.
            if grid_np[r, c] != 0:
                 # Check if the whole 2x2 block contains non-zeros (as per examples)
                 # Or simply assume if top-left is non-zero, it's our block start
                 # Let's assume finding the first non-zero top-left is enough based on examples
                 block = grid_np[r:r+2, c:c+2]
                 # Check if block is within bounds and contains non-zeros
                 if block.shape == (2, 2) and np.any(block != 0):
                     # Verify it's the specific block by checking a value other than top-left, e.g. bottom-right
                     if grid_np[r+1, c+1] != 0 : # or check sum > 0, or any non-zero
                        return r, c
            # A simpler check might be: find first non-zero cell, assume it's top-left
            # if grid_np[r,c] != 0:
            #    return r,c # This works for the examples given

    # A more explicit check looking for the 2x2 area
    for r in range(h - 1):
        for c in range(w - 1):
            block = grid_np[r:r+2, c:c+2]
            if np.all(block != 0): # Check if all elements are non-zero, might be too strict
                 return r, c
            # Let's use the property that the block is the *only* non-zero area
            if np.sum(grid_np) > 0 and np.sum(block) == np.sum(grid_np):
                 return r, c


    return None # Should not happen based on problem description

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by copying the central 2x2 non-zero block
    and adding corner patterns based on the block's values and location.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    h, w = input_grid_np.shape # Should be 6x6

    # Find the location (r, c) of the top-left corner of the 2x2 non-zero block
    location = find_block_location(input_grid_np)
    if location is None:
        # Handle error: No block found (or return input grid?)
        print("Warning: No 2x2 non-zero block found.")
        return input_grid # Or raise error
    r, c = location

    # Extract the values from the 2x2 block
    A = input_grid_np[r, c]
    B = input_grid_np[r, c+1]
    C = input_grid_np[r+1, c]
    D = input_grid_np[r+1, c+1]

    # Initialize the output grid as a copy of the input
    # This preserves the original 2x2 block
    output_grid_np = np.copy(input_grid_np)

    # Apply transformations based on the block's location (r, c)
    if r == 1 and c == 1:
        # Case 1: Block at (1, 1)
        output_grid_np[0, 0] = D          # Top-Left: D at (0,0)
        output_grid_np[0, 3:5] = C      # Top-Right: C at (0,3), (0,4)
        output_grid_np[3:5, 0] = B      # Bottom-Left: B at (3,0), (4,0)
        output_grid_np[3:5, 3:5] = A    # Bottom-Right: A in 2x2 block at (3,3)

    elif r == 2 and c == 2:
        # Case 2: Block at (2, 2)
        output_grid_np[0:2, 0:2] = D    # Top-Left: D in 2x2 block at (0,0)
        output_grid_np[0:2, 4:6] = C    # Top-Right: C in 2x2 block at (0,4)
        output_grid_np[4:6, 0:2] = B    # Bottom-Left: B in 2x2 block at (4,0)
        output_grid_np[4:6, 4:6] = A    # Bottom-Right: A in 2x2 block at (4,4)

    else:
        # Handle unexpected block locations if necessary
        print(f"Warning: Unexpected block location at ({r}, {c}). No corner patterns applied.")
        # Or potentially raise an error
        # raise ValueError(f"Unsupported block location: ({r}, {c})")

    # Convert the result back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid