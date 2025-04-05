import numpy as np
from scipy.ndimage import label

"""
Identifies the largest connected region of non-zero colored cells (LFO) in the 
input grid using 4-connectivity. Then, identifies all connected regions of 
background cells (color 0). Any background region that does not touch the 
grid's boundary is considered an internal hole. 
An internal hole is checked to see if it contains any "thin" cells. A cell is 
"thin" if it is a background cell (0) and has background neighbors both above 
and below it, OR background neighbors both to its left and right.
Only internal holes that contain NO "thin" cells are filled with the color 
of the LFO.
"""

def find_largest_foreground_region_color(input_grid, structure):
    """
    Finds the color of the largest connected foreground region.

    Args:
        input_grid (np.array): The input grid.
        structure (np.array): Connectivity structure.

    Returns:
        int: The color of the largest foreground region, or 0 if no foreground.
    """
    foreground_mask = input_grid > 0
    labeled_fg, num_fg_labels = label(foreground_mask, structure=structure)

    if num_fg_labels == 0:
        return 0 # No foreground objects

    # Count the size of each labeled foreground region (excluding label 0 - background)
    component_sizes = np.bincount(labeled_fg.ravel())
    # Index 0 corresponds to the background (or areas not part of any foreground component)
    # Find the label with the maximum size among foreground components (indices > 0)
    if len(component_sizes) > 1:
        largest_fg_label = np.argmax(component_sizes[1:]) + 1
        # Find the coordinates of the first pixel belonging to the largest component
        # Use np.where which is generally safer than np.argwhere for this
        coords_r, coords_c = np.where(labeled_fg == largest_fg_label)
        if coords_r.size > 0:
            # Get the color from the original grid at these coordinates
            return input_grid[coords_r[0], coords_c[0]]
        else:
             return 0 # Should not happen if largest_fg_label exists
    else:
        return 0 # Only background found

def is_thin(r, c, grid):
    """
    Checks if a background cell at (r, c) is 'thin'.
    A cell is thin if it's background (0) and has background neighbors
    in opposite directions (N/S or E/W).

    Args:
        r (int): Row index.
        c (int): Column index.
        grid (np.array): The input grid.

    Returns:
        bool: True if the cell is thin, False otherwise.
    """
    rows, cols = grid.shape
    if grid[r, c] != 0: # Must be a background cell
        return False

    # Check North-South neighbors
    has_north = r > 0 and grid[r - 1, c] == 0
    has_south = r < rows - 1 and grid[r + 1, c] == 0
    if has_north and has_south:
        return True

    # Check East-West neighbors
    has_west = c > 0 and grid[r, c - 1] == 0
    has_east = c < cols - 1 and grid[r, c + 1] == 0
    if has_west and has_east:
        return True

    return False

def transform(input_grid):
    """
    Fills internal, non-thin holes in the grid with the color of the largest 
    foreground object.

    Args:
        input_grid (list of lists): The input grid representation.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()
    rows, cols = grid_np.shape

    # Define 4-connectivity structure
    structure = np.array([[0, 1, 0],
                          [1, 1, 1],
                          [0, 1, 0]], dtype=bool)

    # --- Step 1: Find the color of the largest foreground region ---
    fill_color = find_largest_foreground_region_color(grid_np, structure)

    # If there's no foreground region or the only color is 0, no filling needed
    if fill_color == 0:
        return output_grid.tolist()

    # --- Step 2: Identify background regions (potential holes) ---
    background_mask = (grid_np == 0)
    labeled_bg, num_bg_labels = label(background_mask, structure=structure)

    # --- Step 3: Identify which background regions touch the boundary ---
    boundary_labels = set()
    if rows > 0:
        boundary_labels.update(labeled_bg[0, :])
        boundary_labels.update(labeled_bg[rows - 1, :])
    if cols > 0:
        boundary_labels.update(labeled_bg[:, 0])
        boundary_labels.update(labeled_bg[:, cols - 1])
    boundary_labels.discard(0) # Remove 0 if present

    # --- Step 4: Check internal holes for thinness and fill if not thin ---
    for label_idx in range(1, num_bg_labels + 1):
        # Check if it's an internal hole (not touching boundary)
        if label_idx not in boundary_labels:
            # Find coordinates of all cells in this background region
            hole_coords_r, hole_coords_c = np.where(labeled_bg == label_idx)

            # Check if any cell in this hole is "thin"
            hole_is_thin = False
            for r, c in zip(hole_coords_r, hole_coords_c):
                if is_thin(r, c, grid_np):
                    hole_is_thin = True
                    break # Found a thin cell, no need to check others in this hole

            # If the hole is NOT thin, fill it
            if not hole_is_thin:
                output_grid[labeled_bg == label_idx] = fill_color

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()