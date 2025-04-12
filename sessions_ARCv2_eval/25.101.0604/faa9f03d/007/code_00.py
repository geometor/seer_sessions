import copy

"""
Transforms an input grid based on a sequence of rules applied using both the
original input grid for context and modifying a working copy (`output_grid`).

Rule Order:
1.  Red Boundary Transformation: Finds '2' pairs in input, fills with '3' and places '1' marker in output.
2.  4-7 Transformation: Finds '4' followed by '7' in input. Copies segment from row below (input) into output, fills 4 positions with '3' in output. Marks '4'.
3.  4-Alone Transformation: Finds '4' in input (not marked in Rule 2). Changes '4' to '6' in output, fills column below with '6's in output.
4.  Vertical Propagation: Finds 'X-0-X' vertical patterns (X=1, 3, or 7) in input. Changes '0' to 'X' in output.
5.  Horizontal Propagation: Iteratively fills gaps in output. If cell Y is between two X's (X=1, 3, or 6) and Y != X, changes Y to X.
"""

# --- Helper Functions ---

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
    # Ensure slice indices are within bounds
    start = max(0, c1 + 1)
    end = min(len(row_data), c2)
    return 0 in row_data[start : end]

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Initialize output_grid as a deep copy of the input to modify
    output_grid = copy.deepcopy(input_grid)
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    processed_fours = set() # Keep track of (r, c) of '4's processed by Rule 2

    # --- 1. Apply Red Boundary Transformation (Rule 1) ---
    # Reads input grid, modifies output_grid
    for r in range(height):
        original_row = input_grid[r]
        boundary_pairs = find_red_boundaries(original_row)

        for c1, c2 in boundary_pairs:
            found_zero = check_zero_in_segment(original_row, c1, c2)

            # Modify output_grid: Change boundaries to 3
            if 0 <= c1 < width: output_grid[r][c1] = 3
            if 0 <= c2 < width: output_grid[r][c2] = 3

            # Modify output_grid: Fill segment between boundaries with 3
            for c in range(c1 + 1, c2):
                 if 0 <= c < width: output_grid[r][c] = 3

            # Modify output_grid: Place '1' based on zero check
            if found_zero:
                marker_pos = c1 + 2
            else:
                marker_pos = c2 - 1

            # Place marker only if it's strictly within the original bounds
            if 0 <= marker_pos < width and c1 < marker_pos < c2:
                output_grid[r][marker_pos] = 1

    # --- 2. Apply 4-7 Transformation (Rule 2) ---
    # Reads input grid, modifies output_grid
    for r in range(height):
        for c in range(width - 1):
            if input_grid[r][c] == 4 and input_grid[r][c+1] == 7:
                # Copy segment from row below (if exists)
                if r + 1 < height:
                    for copy_c in range(c): # Copy columns 0 to c-1
                         if copy_c < width: # Ensure target index is valid
                             output_grid[r][copy_c] = input_grid[r+1][copy_c]

                # Replace 4, 7 and potentially next two cells with 3
                for offset in range(4):
                    target_c = c + offset
                    if target_c < width:
                        output_grid[r][target_c] = 3
                    else:
                        break # Stop if we go past the grid width

                processed_fours.add((r, c)) # Mark this '4' as processed

    # --- 3. Apply 4-Alone Transformation (Rule 3) ---
    # Reads input grid, modifies output_grid
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == 4 and (r, c) not in processed_fours:
                # Change the '4' itself to '6' in the output grid
                if 0 <= r < height and 0 <= c < width: # Bounds check
                    output_grid[r][c] = 6
                # Fill column below with 6s in the output grid
                for fill_r in range(r + 1, height):
                    if 0 <= c < width: # Ensure column index is valid
                         output_grid[fill_r][c] = 6

    # --- 4. Apply Vertical Propagation (Rule 4) ---
    # Reads input grid, modifies output_grid
    for r in range(1, height - 1):
        for c in range(width):
             # Check original input for the X-0-X vertical pattern
             # Check bounds before accessing neighbors
            if 0 <= r-1 < height and 0 <= r+1 < height and 0 <= c < width:
                color_above = input_grid[r-1][c]
                color_below = input_grid[r+1][c]
                color_current_input = input_grid[r][c]

                # Check only if the current cell in input is 0
                if color_current_input == 0:
                    # Propagate 1
                    if color_above == 1 and color_below == 1:
                        output_grid[r][c] = 1
                    # Propagate 3
                    elif color_above == 3 and color_below == 3:
                        output_grid[r][c] = 3
                    # Propagate 7
                    elif color_above == 7 and color_below == 7:
                         output_grid[r][c] = 7


    # --- 5. Apply Horizontal Propagation (Rule 5) ---
    # Operates iteratively on the output_grid, overwriting non-matching colors
    for r in range(height):
        while True: # Keep iterating on the row until no changes are made
            change_made_in_scan = False
            # Create a temporary row copy to check neighbors based on state at start of scan
            row_copy = list(output_grid[r])
            for c in range(1, width - 1):
                # Check bounds before accessing neighbors
                if 0 <= c-1 < width and 0 <= c+1 < width:
                    left_color = row_copy[c-1]
                    right_color = row_copy[c+1]
                    current_color = output_grid[r][c] # Check the *actual* grid value

                    # Check if neighbors are identical, non-zero, and different from current cell
                    if left_color == right_color and left_color != 0 and current_color != left_color:
                        # Propagate only specific colors (1, 3, 6)
                        if left_color in [1, 3, 6]:
                            output_grid[r][c] = left_color
                            change_made_in_scan = True

            if not change_made_in_scan:
                break # No changes in this scan, move to the next row

    # Rule 6 (Cleanup) was removed as it was incorrect based on example 3.

    return output_grid