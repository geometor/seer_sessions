import numpy as np

"""
Transformation Rule:
1. Scan the input grid to find the unique 3x3 pattern composed of 8 yellow (4) 
   border pixels and one central, non-yellow (4), non-white (0) pixel.
2. Extract the color of the central pixel; this will be the background color 
   for the output grid.
3. Record the coordinates of the 8 yellow border pixels from this 3x3 pattern.
4. Find the coordinates of all yellow (4) pixels in the input grid.
5. Identify the single 'marker' yellow pixel coordinate by finding the yellow 
   pixel coordinate that is *not* among the 8 border pixel coordinates found in step 3.
6. Create a new output grid with the same dimensions as the input grid.
7. Fill the entire output grid with the background color identified in step 2.
8. Place yellow (4) pixels onto the output grid at the 8 border coordinates recorded in step 3.
9. Determine the row (`marker_r`) and column (`marker_c`) from the marker pixel coordinate.
10. Calculate the coordinates of all pixels lying on the two diagonals passing 
    through (`marker_r`, `marker_c`) within the grid boundaries (i.e., where 
    row - col == marker_r - marker_c OR row + col == marker_r + marker_c).
11. Place yellow (4) pixels onto the output grid at these calculated diagonal 
    coordinates. If a pixel is already yellow (from step 8), it remains yellow.
12. Return the completed output grid.
"""

def find_yellow_square_details(grid):
    """
    Scans the grid to find the 3x3 yellow square pattern and its details.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (center_color, border_coords_set) if found, otherwise None.
               center_color is the color of the central pixel.
               border_coords_set is a set of (row, col) tuples for the 8 border pixels.
    """
    rows, cols = grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            subgrid = grid[r:r+3, c:c+3]
            center_color = subgrid[1, 1]

            # Check center pixel validity
            if center_color == 4 or center_color == 0:
                continue

            # Check border pixels and collect coordinates
            is_yellow_border = True
            border_coords = set()
            for i in range(3):
                for j in range(3):
                    if i == 1 and j == 1: # Skip center
                        continue
                    if subgrid[i, j] != 4:
                        is_yellow_border = False
                        break
                    border_coords.add((r + i, c + j))
                if not is_yellow_border:
                    break

            if is_yellow_border and len(border_coords) == 8:
                # Pattern found
                return center_color, border_coords
    return None # Pattern not found

def find_all_pixels_of_color(grid, color):
    """
    Finds all coordinates of pixels with a specific color.

    Args:
        grid (np.array): The input grid.
        color (int): The color to find.

    Returns:
        list: A list of (row, col) tuples for pixels matching the color.
    """
    coords = np.where(grid == color)
    return list(zip(coords[0], coords[1]))

def find_marker_pixel(all_yellow_coords, border_coords_set):
    """
    Identifies the marker yellow pixel (the one not part of the square border).

    Args:
        all_yellow_coords (list): List of (r, c) tuples for all yellow pixels.
        border_coords_set (set): Set of (r, c) tuples for the 8 border pixels.

    Returns:
        tuple: (row, col) of the marker pixel, or None if exactly one is found.
    """
    marker_candidates = []
    for r, c in all_yellow_coords:
        if (r, c) not in border_coords_set:
            marker_candidates.append((r, c))

    # Expect exactly one marker pixel based on examples
    if len(marker_candidates) == 1:
        return marker_candidates[0]
    else:
        print(f"Warning: Found {len(marker_candidates)} non-border yellow pixels. Expected 1.")
        return None


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Find the 3x3 square, get background color and border coordinates
    square_details = find_yellow_square_details(input_grid)
    if square_details is None:
        print("Error: Characteristic 3x3 yellow square pattern not found.")
        return np.copy(input_grid) # Return copy or raise error
    background_color, border_coords_set = square_details

    # 4. Find all yellow pixels
    all_yellow_coords = find_all_pixels_of_color(input_grid, 4) # 4 is yellow

    # 5. Identify the marker pixel
    marker_coord = find_marker_pixel(all_yellow_coords, border_coords_set)
    if marker_coord is None:
        print("Error: Marker yellow pixel not found or ambiguity exists.")
        return np.copy(input_grid) # Return copy or raise error
    marker_row, marker_col = marker_coord

    # 6. Create output grid
    output_grid = np.full_like(input_grid, background_color)
    rows, cols = output_grid.shape

    # 8. Draw the original border pixels
    for r_border, c_border in border_coords_set:
        if 0 <= r_border < rows and 0 <= c_border < cols: # Boundary check
            output_grid[r_border, c_border] = 4 # Yellow

    # 9. Get marker coordinates (already done)
    # 10. Calculate diagonal invariants
    diag1_invariant = marker_row - marker_col # y = x + k => y - x = k
    diag2_invariant = marker_row + marker_col # y = -x + k => y + x = k

    # 11. Draw diagonals
    for r in range(rows):
        for c in range(cols):
            if (r - c == diag1_invariant) or (r + c == diag2_invariant):
                output_grid[r, c] = 4 # Yellow color

    # 12. Return the final grid
    return output_grid