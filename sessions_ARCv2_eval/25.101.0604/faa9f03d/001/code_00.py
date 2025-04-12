import copy

"""
Transforms an input grid based on two primary rules applied sequentially:

1.  **Red Boundary Transformation:** Identifies horizontal segments defined by pairs of '2's (red) on the same row in the original input. 
    - The boundary '2's are changed to '3's (green).
    - The cells between the boundaries are filled with '3's.
    - A single '1' (blue) is placed within the segment. Its position depends on whether a '0' (black) was originally present between the boundaries:
        - If a '0' was present, the '1' is placed at column `c1 + 2` (where `c1` is the left boundary column).
        - If no '0' was present, the '1' is placed at column `c2 - 1` (where `c2` is the right boundary column).
    This transformation uses the original input grid to determine the segments and the presence of '0's, but applies changes to a working copy.

2.  **Blue Propagation:** Iteratively fills horizontal gaps between '1's. 
    - If a cell is not '1', but its immediate left and right neighbors in the same row are '1', the cell is changed to '1'.
    - This process repeats for each row until no more cells can be changed in that row.
    This transformation operates on the grid resulting from the Red Boundary Transformation pass.
"""

def find_red_boundaries(row_data: list[int]) -> list[tuple[int, int]]:
    """Finds pairs of indices corresponding to the color 2 in a row."""
    indices = [i for i, color in enumerate(row_data) if color == 2]
    pairs = []
    # Simple pairing assuming non-overlapping boundaries as seen in examples
    for i in range(0, len(indices), 2):
        if i + 1 < len(indices):
            pairs.append((indices[i], indices[i+1]))
    return pairs

def check_zero_in_segment(row_data: list[int], c1: int, c2: int) -> bool:
    """Checks if the color 0 exists in the row segment between c1+1 and c2-1."""
    if c1 + 1 >= c2: # Check if segment is empty or just boundaries
        return False
    return 0 in row_data[c1 + 1 : c2]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the red boundary transformation and blue propagation rules to the input grid.
    """
    # Initialize output_grid as a deep copy of the input to modify
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # --- 1. Red Boundary Transformation Pass ---
    # This pass uses the original input_grid for checks but modifies output_grid
    for r in range(height):
        original_row = input_grid[r]
        # Find pairs of '2's in the original row
        boundary_pairs = find_red_boundaries(original_row)

        for c1, c2 in boundary_pairs:
            # Check for '0' within the segment in the original row
            found_zero = check_zero_in_segment(original_row, c1, c2)

            # Modify the output_grid
            # Change boundaries to 3
            if 0 <= r < height and 0 <= c1 < width:
                 output_grid[r][c1] = 3
            if 0 <= r < height and 0 <= c2 < width:
                 output_grid[r][c2] = 3

            # Fill segment between boundaries with 3
            for c in range(c1 + 1, c2):
                 if 0 <= r < height and 0 <= c < width:
                     output_grid[r][c] = 3

            # Place '1' based on zero check
            if found_zero:
                marker_pos = c1 + 2
            else:
                marker_pos = c2 - 1

            if 0 <= r < height and 0 <= marker_pos < width:
                # Ensure marker is within the segment bounds before placing
                if c1 < marker_pos < c2:
                    output_grid[r][marker_pos] = 1
                # Handle edge case where segment is too small for marker placement logic (e.g., c1+2 >= c2)
                # The logic derived seems to assume segments are wide enough. If not, the original fill remains.


    # --- 2. Blue Propagation Pass ---
    # This pass operates entirely on the (potentially modified) output_grid
    for r in range(height):
        while True: # Keep iterating on the row until no changes are made
            change_made_in_scan = False
            # Create a temporary row copy to avoid propagation within the same scan
            row_copy = list(output_grid[r])
            for c in range(1, width - 1):
                # Check if cell is not blue, but neighbors are blue
                if row_copy[c] != 1 and row_copy[c-1] == 1 and row_copy[c+1] == 1:
                    # Check if the cell in the actual grid is still not blue before changing
                    # This handles cases where a cell might have been changed by the red boundary pass
                    if output_grid[r][c] != 1:
                        output_grid[r][c] = 1
                        change_made_in_scan = True
            
            if not change_made_in_scan:
                break # No changes in this scan, move to the next row

    return output_grid