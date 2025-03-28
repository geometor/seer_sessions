```python
import numpy as np
from scipy.ndimage import label, generate_binary_structure

"""
Identifies contiguous non-white objects (8-way connectivity) and their enclosed white regions (holes, 4-way connectivity). Fills holes based on the number and size:
- If an object encloses exactly one hole:
  - Fill with gray (5) if the hole size is 1 pixel.
  - Fill with orange (7) if the hole size is greater than 1 pixel.
- If an object encloses exactly two holes:
  - Fill both holes with orange (7).
White regions touching the grid border are considered background and are not filled.
"""

def find_neighbors(grid_shape, coords, connectivity=8):
    """
    Finds valid neighbor coordinates for a set of coordinates within the grid boundaries.

    Args:
        grid_shape (tuple): The (rows, cols) shape of the grid.
        coords (set): A set of (row, col) tuples representing the coordinates of interest.
        connectivity (int): 8 for 8-way (including diagonals), 4 for 4-way.

    Returns:
        set: A set of (row, col) tuples representing neighbor coordinates.
    """
    neighbors = set()
    rows, cols = grid_shape
    if connectivity == 4:
        offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        offsets = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for r, c in coords:
        for dr, dc in offsets:
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within the grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.add((nr, nc))
    return neighbors

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Fills enclosed white regions (holes) within colored shapes based on the number and size of holes.
    - 1 hole, size 1: fill with gray (5)
    - 1 hole, size > 1: fill with orange (7)
    - 2 holes: fill with orange (7)
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Define connectivity structures
    struct_obj = generate_binary_structure(2, 2)  # 8-way connectivity for objects
    struct_hole = generate_binary_structure(2, 1) # 4-way connectivity for holes

    # 1. Identify all colored objects (non-zero pixels) using 8-way connectivity
    colored_mask = input_grid != 0
    obj_labels, num_objs = label(colored_mask, structure=struct_obj)

    # 2. Identify all white regions (zero pixels) using 4-way connectivity
    white_mask = input_grid == 0
    hole_labels, num_holes_total = label(white_mask, structure=struct_hole)

    # 3. Determine the labels of the background white region(s)
    # Any white region touching the border is considered background.
    border_labels = set()
    if rows > 0 and cols > 0: # Ensure grid is not empty
        border_labels.update(hole_labels[0, :])      # Top row
        border_labels.update(hole_labels[-1, :])     # Bottom row
        border_labels.update(hole_labels[:, 0])      # Left column
        border_labels.update(hole_labels[:, -1])     # Right column
    # Filter out 0 (which represents non-white areas in hole_labels)
    background_label_set = {lbl for lbl in border_labels if lbl != 0}

    # 4. Iterate through each unique colored object
    obj_indices = np.unique(obj_labels)
    obj_indices = obj_indices[obj_indices != 0] # Exclude background label 0

    for obj_id in obj_indices:
        # Get coordinates of the current object
        obj_coords_tuple = np.where(obj_labels == obj_id)
        obj_coords_set = set(zip(obj_coords_tuple[0], obj_coords_tuple[1]))

        # Find all 8-way neighbors of the object's pixels
        neighbor_coords = find_neighbors((rows, cols), obj_coords_set, connectivity=8)

        # Identify adjacent white region labels that are *not* part of the object itself
        adjacent_hole_labels = set()
        for r, c in neighbor_coords:
            if (r, c) not in obj_coords_set: # Ensure neighbor is not part of the object
                 hole_label_at_coord = hole_labels[r, c]
                 # Check if it's a valid labeled white region (label > 0)
                 if hole_label_at_coord != 0:
                     adjacent_hole_labels.add(hole_label_at_coord)

        # Filter out the background labels to get only enclosed holes
        enclosed_hole_labels = adjacent_hole_labels - background_label_set
        num_enclosed_holes = len(enclosed_hole_labels)

        # 5. Apply fill logic based on the number and size of enclosed holes
        if num_enclosed_holes == 1:
            hole_id = list(enclosed_hole_labels)[0]
            hole_coords = np.where(hole_labels == hole_id)
            hole_size = len(hole_coords[0]) # Count number of pixels in the hole

            fill_color = -1 # Default: no fill
            if hole_size == 1:
                fill_color = 5 # Gray for size 1
            elif hole_size > 1:
                fill_color = 7 # Orange for size > 1

            if fill_color != -1:
                output_grid[hole_coords] = fill_color

        elif num_enclosed_holes == 2:
            fill_color = 7 # Orange for two holes
            for hole_id in enclosed_hole_labels:
                hole_coords = np.where(hole_labels == hole_id)
                output_grid[hole_coords] = fill_color
        
        # Implicit: If num_enclosed_holes is 0 or > 2, do nothing.

    return output_grid
```