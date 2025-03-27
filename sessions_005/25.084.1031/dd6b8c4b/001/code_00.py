"""
Identify a 3x3 block containing green (3) and red (2) pixels.
Determine if this block has a magenta (6) border.
Check if any maroon (9) pixel is adjacent (including diagonals) to the block or its border.

Rule 1: If a magenta border exists AND a maroon pixel is adjacent:
  - Change all green (3) and red (2) pixels within the 3x3 block to maroon (9).

Rule 2: If a magenta border exists AND NO maroon pixel is adjacent:
  - Find the location (r, c) of the original red (2) pixel.
  - Change the green (3) pixels at (r-1, c-1) and (r-1, c) to maroon (9).
  - Additionally, find any magenta (6) pixel that is NOT part of the immediate border but IS adjacent to any maroon (9) pixel in the input, and change its color to orange (7).

Rule 3: If NO magenta border exists:
  - Find the location (r, c) of the original red (2) pixel.
  - Within the 3x3 block:
    - Change green (3) pixels to maroon (9) if their row is above 'r'.
    - Change green (3) pixels to maroon (9) if their row is 'r' and their column is left of 'c'.
  - Change the original red (2) pixel at (r, c) to green (3).
  - Additionally, find all maroon (9) pixels in the input grid. If a maroon pixel has NO adjacent (including diagonal) maroon neighbors in the input grid, change its color to orange (7).

All other pixels remain unchanged.
"""

import numpy as np

def find_central_block(grid):
    """
    Finds the 3x3 block containing green (3) and red (2) pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (top_left_r, top_left_c, red_r, red_c) or (None, None, None, None) if not found.
               Returns the coordinates of the top-left corner of the 3x3 block
               and the coordinates of the red (2) pixel within the grid.
    """
    rows, cols = grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            block = grid[r:r+3, c:c+3]
            red_pixels = np.where(block == 2)
            green_pixels = np.where(block == 3)

            if len(red_pixels[0]) == 1 and len(green_pixels[0]) > 0:
                # Found the block
                red_r_local, red_c_local = red_pixels[0][0], red_pixels[1][0]
                red_r, red_c = r + red_r_local, c + red_c_local
                return r, c, red_r, red_c
    return None, None, None, None

def get_neighbors(grid_shape, r, c, include_diagonal=True):
    """
    Gets the coordinates of valid neighbors for a pixel.

    Args:
        grid_shape (tuple): The shape (rows, cols) of the grid.
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.
        include_diagonal (bool): Whether to include diagonal neighbors.

    Returns:
        list: A list of neighbor coordinates (nr, nc).
    """
    rows, cols = grid_shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            if not include_diagonal and abs(dr) + abs(dc) == 2:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def check_magenta_border(grid, br, bc):
    """
    Checks if the 3x3 block starting at (br, bc) has a solid magenta (6) border.

    Args:
        grid (np.array): The input grid.
        br (int): Top row index of the block.
        bc (int): Left column index of the block.

    Returns:
        bool: True if a complete magenta border exists, False otherwise.
        set: Coordinates of the border pixels.
    """
    rows, cols = grid.shape
    border_coords = set()
    has_border = True

    # Define potential border coordinates relative to br, bc
    potential_border_indices = [
        (-1, -1), (-1, 0), (-1, 1), (-1, 2), (-1, 3),
        (0, -1),                          (0, 3),
        (1, -1),                          (1, 3),
        (2, -1),                          (2, 3),
        (3, -1), (3, 0), (3, 1), (3, 2), (3, 3),
    ]

    for dr, dc in potential_border_indices:
        r, c = br + dr, bc + dc
        if 0 <= r < rows and 0 <= c < cols:
            border_coords.add((r, c))
            if grid[r, c] != 6:
                has_border = False
                # Don't break early, collect all potential border coords
        else:
            # If a border pixel would be off-grid, it can't be a complete border
             # Update: The examples imply borders can be incomplete at edges.
             # Let's assume the rule applies if *all existing* border cells are magenta.
             # However, for simplicity and based on examples, let's require the full 5x5 area
             # to be checkable within bounds for a border to be 'present'.
             # A strict interpretation: if br=0 or bc=0 or br+3>=rows or bc+3>=cols, border cannot be complete.
             if br == 0 or bc == 0 or br + 3 >= rows or bc + 3 >= cols:
                 # If the block touches the edge, we consider the border check to fail
                 # unless the problem statement implies otherwise. Example 1/2 block is not at edge.
                 # Let's assume full border means the 5x5 area is within bounds.
                 return False, set() # Cannot have a full border if block is too close to edge

    # If we got here, the 5x5 area is within bounds. Now check colors.
    for r, c in border_coords:
        if grid[r, c] != 6:
            return False, border_coords # Found a non-magenta cell in the border area

    # If all checks passed
    return True, border_coords


def check_maroon_adjacency(grid, br, bc, border_coords, has_border):
    """
    Checks if any maroon (9) pixel is adjacent (incl. diagonal) to the block or its border.

    Args:
        grid (np.array): The input grid.
        br (int): Top row index of the block.
        bc (int): Left column index of the block.
        border_coords (set): Coordinates of the border pixels (if has_border is True).
        has_border (bool): Whether a magenta border exists.

    Returns:
        bool: True if an adjacent maroon pixel is found, False otherwise.
    """
    rows, cols = grid.shape
    block_coords = set((r, c) for r in range(br, br + 3) for c in range(bc, bc + 3))
    target_coords = block_coords
    if has_border:
        target_coords.update(border_coords)

    maroon_locations = np.argwhere(grid == 9)

    for mr, mc in maroon_locations:
        neighbors = get_neighbors(grid.shape, mr, mc, include_diagonal=True)
        for nr, nc in neighbors:
            if (nr, nc) in target_coords:
                return True
    return False


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    input_grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the central block and red pixel
    br, bc, r_red, c_red = find_central_block(input_grid)

    if br is None:
        # No block found, return the original grid
        return output_grid.tolist()

    # 2. Determine if a magenta border exists
    has_magenta_border, border_coords = check_magenta_border(input_grid, br, bc)

    # 3. Check for maroon adjacency
    is_maroon_adjacent = check_maroon_adjacency(input_grid, br, bc, border_coords, has_magenta_border)

    # 4. Apply rules based on border and adjacency
    if has_magenta_border:
        if is_maroon_adjacent:
            # Rule 1: Change block green/red to maroon
            for r in range(br, br + 3):
                for c in range(bc, bc + 3):
                    if input_grid[r, c] == 3 or input_grid[r, c] == 2:
                        output_grid[r, c] = 9
        else:
            # Rule 2: Change specific greens to maroon, modify stray magentas
            # Ensure target pixels are within bounds before changing
            if 0 <= r_red - 1 < rows and 0 <= c_red - 1 < cols:
                 if output_grid[r_red - 1, c_red - 1] == 3: # Check if it's green before changing
                     output_grid[r_red - 1, c_red - 1] = 9
            if 0 <= r_red - 1 < rows and 0 <= c_red < cols:
                 if output_grid[r_red - 1, c_red] == 3: # Check if it's green before changing
                      output_grid[r_red - 1, c_red] = 9

            # Modify stray magentas adjacent to maroons
            magenta_locations = np.argwhere(input_grid == 6)
            maroon_locations = np.argwhere(input_grid == 9) # Find maroon locations once

            for mag_r, mag_c in magenta_locations:
                if (mag_r, mag_c) not in border_coords: # Check if it's NOT part of the border
                    is_adj_to_maroon = False
                    neighbors = get_neighbors(input_grid.shape, mag_r, mag_c, include_diagonal=True)
                    for nr, nc in neighbors:
                        if input_grid[nr, nc] == 9:
                            is_adj_to_maroon = True
                            break
                    if is_adj_to_maroon:
                        output_grid[mag_r, mag_c] = 7 # Change to orange

    else: # No magenta border
        # Rule 3: Change specific greens, change red to green, modify isolated maroons
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if input_grid[r, c] == 3:
                    if r < r_red:
                        output_grid[r, c] = 9
                    elif r == r_red and c < c_red:
                        output_grid[r, c] = 9
        # Change original red to green
        output_grid[r_red, c_red] = 3

        # Modify isolated maroons
        maroon_locations = np.argwhere(input_grid == 9)
        for mr, mc in maroon_locations:
            is_isolated = True
            neighbors = get_neighbors(input_grid.shape, mr, mc, include_diagonal=True)
            for nr, nc in neighbors:
                if input_grid[nr, nc] == 9:
                    is_isolated = False
                    break
            if is_isolated:
                # Check if this maroon pixel was changed in the block modification step above
                # This check is important if a green turned into maroon and is isolated
                # We only want to change *original* isolated maroons to orange
                if input_grid[mr, mc] == 9: # Only change if it was maroon in the input
                   output_grid[mr, mc] = 7 # Change to orange


    return output_grid.tolist()