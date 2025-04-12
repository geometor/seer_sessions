```python
import numpy as np
import copy

"""
Transformation Rule based on "Bridging" Hypothesis:

1. Create a working copy of the input grid.
2. Initialize an empty set `columns_to_remove`.
3. Find all gray pixels (color 5) in the input grid.
4. For each gray pixel (GP) at position (r, c):
    a. Find its 8 direct neighbors.
    b. Identify the distinct non-white (0), non-gray (5) colors among these direct neighbors.
    c. Determine the 'unique_neighbor_color' (C): This is the color if exactly one such distinct color exists among neighbors; otherwise, it's considered undefined.
    d. Determine the color the gray pixel will become ('new_color'): It becomes color C if C is defined, otherwise it becomes white (0). Store this change.
    e. Check the Bridging Condition: The GP is considered "bridging" if it is adjacent (8-connectivity) to any neighbor pixel P whose color Cp is non-white, non-gray, AND (C is undefined OR Cp is different from C).
    f. If the GP is bridging, add its column index `c` to the `columns_to_remove` set.
5. Apply all stored color changes to the working grid.
6. Construct the final output grid by selecting only the columns from the modified working grid whose indices are *not* in the `columns_to_remove` set, preserving the original relative order.
"""

def get_neighbors(grid: np.ndarray, r: int, c: int, connectivity=8) -> list[tuple[int, int, int]]:
    """
    Gets neighbours (value, row, col) of a pixel at (r, c), handling grid boundaries.
    Supports 8-way (default) or 4-way connectivity.
    """
    neighbours = []
    rows, cols = grid.shape
    if connectivity == 8:
        deltas = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    elif connectivity == 4:
        deltas = [(-1,0), (0,-1), (0,1), (1,0)]
    else:
        deltas = [] # Should not happen with current usage

    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        # Check grid boundaries
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbours.append((grid[nr, nc], nr, nc))
    return neighbours

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the "Bridging" hypothesis for gray pixels.
    """
    # Convert input list of lists to a numpy array
    input_array = np.array(input_grid, dtype=int)

    # Handle empty input grid case
    if input_array.size == 0:
        return []

    # Create a working copy to store modifications
    working_grid = np.copy(input_array)
    rows, cols = input_array.shape

    # Initialize set to store indices of columns to be removed
    columns_to_remove = set()
    # Initialize list to store color modifications
    modifications = [] # Store as (r, c, new_color)

    # Find coordinates of all gray pixels first
    gray_pixels_coords = []
    for r in range(rows):
        for c in range(cols):
            if input_array[r, c] == 5:
                gray_pixels_coords.append((r, c))

    # Process each identified gray pixel
    for r, c in gray_pixels_coords:
        # Step 4a: Find neighbors
        direct_neighbors = get_neighbors(input_array, r, c, connectivity=8)

        # Step 4b: Identify distinct non-white/non-gray direct neighbor colors
        colored_direct_neighbors = [n for n in direct_neighbors if n[0] != 0 and n[0] != 5]
        distinct_direct_colors = set(n[0] for n in colored_direct_neighbors)

        # Step 4c: Determine unique_neighbor_color (C)
        unique_neighbor_color = -1 # Sentinel for undefined C
        if len(distinct_direct_colors) == 1:
            unique_neighbor_color = list(distinct_direct_colors)[0]
        # Note: Case len > 1 was not observed, but is handled implicitly (C remains -1)

        # Step 4d: Determine new_color and store modification
        new_color = 0 # Default to white
        if unique_neighbor_color != -1:
            new_color = unique_neighbor_color
        modifications.append((r, c, new_color))

        # Step 4e: Check the Bridging Condition
        is_bridging = False
        for neighbor_val, _, _ in direct_neighbors:
            # Check if neighbor P has color Cp != 0, != 5
            if neighbor_val != 0 and neighbor_val != 5:
                 # Check if C is undefined OR Cp is different from C
                 if unique_neighbor_color == -1 or neighbor_val != unique_neighbor_color:
                     is_bridging = True
                     break # Found a bridging neighbor, no need to check others

        # Step 4f: Mark column for removal if bridging
        if is_bridging:
            columns_to_remove.add(c)

    # Step 5: Apply all collected color modifications to the working grid
    for mod_r, mod_c, mod_color in modifications:
        working_grid[mod_r, mod_c] = mod_color

    # Step 6: Construct the final output grid by removing marked columns
    # Create a list of column indices to keep
    output_cols_indices = [c_idx for c_idx in range(cols) if c_idx not in columns_to_remove]

    # Create the output array
    if not output_cols_indices:
         # If all columns are removed or no columns existed initially
        output_grid_array = np.empty((rows, 0), dtype=int)
    else:
        # Select only the columns that are not marked for removal
        output_grid_array = working_grid[:, output_cols_indices]

    # Convert final numpy array back to list of lists for the return value
    return output_grid_array.tolist()
```