
Previous Code:
```python
import numpy as np

"""
Transforms the input grid based on the following rules:
1. Identifies a solid rectangular block of color 3.
2. Identifies a 'source' pattern block adjacent (below or left, potentially separated by a zero row/column) to the color 3 block, matching its size along the shared dimension.
3. Copies the source pattern into the area originally occupied by the color 3 block in an intermediate grid.
4. Iterates through the intermediate grid and creates the final output grid.
5. Changes the color of '2' cells to '8' in the final output grid if they form a corner in the intermediate grid. A corner '2' has exactly two neighbors (N, S, E, W) that are also '2', and these two neighbors are adjacent to each other (e.g., N and E, not N and S).
6. All other cells (0s, non-corner 2s) retain their color from the intermediate grid in the final output grid.
"""

def find_color_block(grid_np, color):
    """
    Finds the bounding box (min_row, max_row, min_col, max_col) of the
    first contiguous block of the specified color encountered.
    Assumes the block is rectangular and solid for color 3 based on examples.
    Returns None if the color is not found.
    """
    rows, cols = grid_np.shape
    # Find all coordinates where the grid matches the color
    coords = np.argwhere(grid_np == color)
    if coords.size == 0:
        return None # Color not found

    # Determine the bounding box
    r_min, c_min = coords.min(axis=0)
    r_max, c_max = coords.max(axis=0)

    # For color 3, we assume based on examples it forms a solid rectangle.
    # A simple check verifies if all cells within the bounding box have the target color.
    block = grid_np[r_min:r_max+1, c_min:c_max+1]
    if np.all(block == color):
        return (r_min, r_max, c_min, c_max)
    else:
        # This indicates the found coordinates don't form a solid block within their bounding box.
        # This case is not expected for color 3 based on the provided examples.
        # We might return the bounding box anyway, or handle as an error.
        # Returning the bounding box allows processing even if assumption is slightly violated.
        # print(f"Warning: Color {color} at {r_min, c_min} to {r_max, c_max} does not form a solid block.")
        return (r_min, r_max, c_min, c_max)


def is_corner(grid_np, r, c):
    """
    Checks if a cell at (r, c) with value 2 is a corner in the grid.
    A corner has exactly two neighbors (N, S, E, W) with value 2,
    and those neighbors are adjacent to each other (e.g., North and East,
    or South and West, but not North and South or East and West).
    """
    rows, cols = grid_np.shape
    # Cell itself must be 2
    if grid_np[r, c] != 2:
        return False

    # Define neighbor coordinates relative to (r, c)
    # Indices correspond to: 0:North, 1:South, 2:East, 3:West
    neighbors_coords = [
        (r - 1, c), # N (idx 0)
        (r + 1, c), # S (idx 1)
        (r, c + 1), # E (idx 2)
        (r, c - 1)  # W (idx 3)
    ]

    neighbor_color_2_count = 0
    # Store indices (0=N, 1=S, 2=E, 3=W) of neighbors that have color 2
    neighbor_indices_2 = []

    # Check each neighbor
    for idx, (nr, nc) in enumerate(neighbors_coords):
        # Check if neighbor is within grid bounds
        if 0 <= nr < rows and 0 <= nc < cols:
            # Check if neighbor color is 2
            if grid_np[nr, nc] == 2:
                neighbor_color_2_count += 1
                neighbor_indices_2.append(idx)

    # A corner must have exactly two neighbors with color 2
    if neighbor_color_2_count != 2:
        return False

    # Check if the two neighbors are adjacent (i.e., not opposites)
    # Opposite pairs have indices (0, 1) [N, S] or (2, 3) [E, W]
    idx1, idx2 = sorted(neighbor_indices_2) # Sort for consistent checking

    # If the pair is (0, 1) or (2, 3), they are opposites, so it's not a corner
    if (idx1 == 0 and idx2 == 1) or (idx1 == 2 and idx2 == 3):
        return False

    # If count is 2 and they are not opposites, they must be adjacent neighbors
    return True


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the identified pattern:
    Copies a source pattern block (adjacent to the '3' block) onto the
    location of the '3' block, then converts corner '2's to '8's.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    # Create an intermediate grid based on input to perform the copy operation
    intermediate_np = input_np.copy()

    # --- Step 1: Find the '3' block ---
    coords_3 = find_color_block(intermediate_np, 3)

    # If a '3' block exists, perform the copy operation
    if coords_3 is not None:
        r_min_3, r_max_3, c_min_3, c_max_3 = coords_3
        height_3 = r_max_3 - r_min_3 + 1
        width_3 = c_max_3 - c_min_3 + 1
        # Define the slice representing the target area (where '3' block is)
        target_slice = (slice(r_min_3, r_max_3 + 1), slice(c_min_3, c_max_3 + 1))

        # --- Step 2: Determine orientation and find source block ---
        source_slice = None
        # Heuristic based on examples: if block width matches grid width, it's horizontal.
        is_horizontal = (width_3 == cols)

        if is_horizontal:
            # Block is horizontal, source pattern is below it
            # Search downwards row by row starting from below the '3' block
            r_source_start = -1
            for r in range(r_max_3 + 1, rows):
                # Check if any cell in the relevant columns of this row (in the *original* grid) is non-zero
                if np.any(input_np[r, c_min_3:c_max_3+1] != 0):
                    r_source_start = r
                    break # Found the first row of the source block

            if r_source_start != -1:
                # Source block has the same height as the '3' block
                r_source_end = r_source_start + height_3 - 1
                # Ensure the calculated source block is within grid bounds
                if r_source_end < rows:
                    source_slice = (slice(r_source_start, r_source_end + 1), slice(c_min_3, c_max_3 + 1))

        else: # Block is vertical, source pattern is to the left
            # Search leftwards column by column starting from left of the '3' block
            c_source_end = -1
            for c in range(c_min_3 - 1, -1, -1): # Iterate columns from c_min_3-1 down to 0
                 # Check if any cell in the relevant rows of this column (in the *original* grid) is non-zero
                 if np.any(input_np[r_min_3:r_max_3+1, c] != 0):
                     c_source_end = c
                     break # Found the last column of the source block

            if c_source_end != -1:
                # Source block has the same width as the '3' block
                c_source_start = c_source_end - width_3 + 1
                # Ensure the calculated source block is within grid bounds
                if c_source_start >= 0:
                    source_slice = (slice(r_min_3, r_max_3 + 1), slice(c_source_start, c_source_end + 1))

        # --- Step 3: Copy pattern from source to target in intermediate grid ---
        if source_slice:
            try:
                # Get the data from the source slice in the original input
                source_data = input_np[source_slice]
                # Get the shape of the target area
                target_shape = intermediate_np[target_slice].shape

                # Ensure source and target shapes match before copying
                if source_data.shape == target_shape:
                    intermediate_np[target_slice] = source_data
                else:
                     # Handle unexpected shape mismatch - clear target area
                     # print(f"Shape mismatch error: Target {target_shape}, Source {source_data.shape}")
                     intermediate_np[target_slice] = 0
            except IndexError:
                 # Handle cases where calculated slices might be out of bounds
                 # print(f"IndexError during copy: Target {target_slice}, Source {source_slice}")
                 intermediate_np[target_slice] = 0 # Clear target area on error
        else:
             # If no source block could be identified (e.g., '3' block at edge)
             # Clear the target area (replace '3's with '0's)
             intermediate_np[target_slice] = 0

    # --- Step 4: Apply Corner Transformation ---
    # Create the final output grid, starting as a copy of the intermediate grid
    final_output_np = intermediate_np.copy()
    # Iterate through each cell of the intermediate grid
    for r in range(rows):
        for c in range(cols):
            # Check for corners using the state of the *intermediate* grid
            if intermediate_np[r, c] == 2:
                if is_corner(intermediate_np, r, c):
                    # If it's a corner '2', change it to '8' in the final output
                    final_output_np[r, c] = 8
            # Note: If it was '3', it should have been overwritten by copy or set to 0.
            # If it was '0' or a non-corner '2', it remains as is in final_output_np.

    # Convert final numpy array back to list of lists for the expected output format
    return final_output_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2
0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0
0 0 0 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0
0 0 0 0 0 2 2 0 0 0 2 2 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0
2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 0 0 0 0
2 2 0 0 0 2 2 0 0 0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 8 2 2 0 0 2 8 2 0 0 2 2 8
0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0
0 0 0 0 0 2 2 2 0 0 2 2 2 0 0 2 2 2 0
0 0 0 0 0 2 2 0 0 0 2 2 0 0 0 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 2 2 2 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0
8 2 2 0 0 2 8 2 0 0 2 2 8 0 0 0 0 0 0
2 2 0 0 0 2 2 0 0 0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0
8 2 0 0 0 2 8 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 8 2 2 0 0 8 2 2 0 0 8 2 2
0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0
0 0 0 0 0 8 2 2 0 0 8 2 2 0 0 8 2 2 0
0 0 0 0 0 8 8 0 0 0 8 8 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 2 2 0 0 8 2 2 0 0 8 2 2 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0
8 2 2 0 0 8 2 2 0 0 8 2 2 0 0 0 0 0 0
8 8 0 0 0 8 8 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 2 2 0 0 8 2 2 0 0 8 2 2 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0
8 2 2 0 0 8 2 2 0 0 8 2 2 0 0 0 0 0 0
8 8 0 0 0 8 8 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 2 2 0 0 8 2 2 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
8 2 2 0 0 8 2 2 0 0 0 0 0 0 0 0 0 0 0
8 8 0 0 0 8 8 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 55
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 30.47091412742381

## Example 2:
Input:
```
2 2 0 0 2 2 0 0 3 3 3
2 0 2 0 2 0 2 0 3 3 3
0 2 0 0 0 2 0 0 3 3 3
0 0 0 0 0 0 0 0 3 3 3
2 2 0 0 0 0 0 0 3 3 3
2 0 2 0 0 0 0 0 3 3 3
0 2 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 2 2 0 0 3 3 3
0 0 0 0 2 0 2 0 3 3 3
0 0 0 0 0 2 0 0 3 3 3
```
Expected Output:
```
8 2 0 0 2 8 0 0 0 0 0
2 0 2 0 2 0 2 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 2 2 0
8 0 2 0 0 0 0 0 2 0 8
0 2 0 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
```
Transformed Output:
```
8 2 0 0 8 2 0 0 8 2 0
2 0 2 0 2 0 2 0 2 0 2
0 2 0 0 0 2 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0 0
8 2 0 0 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 2 0 0 8 2 0
0 0 0 0 2 0 2 0 2 0 2
0 0 0 0 0 2 0 0 0 2 0
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 34.71074380165288

## Example 3:
Input:
```
2 0 2 0 0 0 0 0 3 3 3
0 2 0 0 0 0 0 0 3 3 3
2 2 0 0 0 0 0 0 3 3 3
0 0 0 0 0 0 0 0 3 3 3
0 0 0 0 2 0 2 0 3 3 3
0 0 0 0 0 2 0 0 3 3 3
0 0 0 0 2 2 0 0 3 3 3
0 0 0 0 0 0 0 0 3 3 3
2 0 2 0 2 0 2 0 3 3 3
0 2 0 0 0 2 0 0 3 3 3
2 2 0 0 2 2 0 0 3 3 3
```
Expected Output:
```
8 0 2 0 0 0 0 0 2 0 8
0 2 0 0 0 0 0 0 0 2 0
2 2 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 0 0 0
0 2 0 0 0 2 0 0 0 0 0
8 2 0 0 2 8 0 0 0 0 0
```
Transformed Output:
```
2 0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 2 0 2 0 2
0 0 0 0 0 2 0 0 0 2 0
0 0 0 0 2 8 0 0 2 8 0
0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0 2
0 2 0 0 0 2 0 0 0 2 0
2 8 0 0 2 8 0 0 2 8 0
```
Match: False
Pixels Off: 21
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 34.71074380165288
