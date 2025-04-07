```python
import numpy as np
from scipy.ndimage import label
from collections import Counter

def get_neighbors(r, c, rows, cols):
    """Generates coordinates of 8 neighbors for a cell (r, c) within grid bounds."""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                yield nr, nc

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the grid by identifying non-zero connected regions.
    For regions containing exactly two distinct non-zero colors (a common 'component'
    color C and a unique 'seed' color S), it applies a pattern based on the
    Manhattan distance from the seed cell:
    1. The seed cell becomes 0.
    2. Boundary cells (adjacent to background 0s) remain unchanged (color C).
    3. Interior cells become 0 if their Manhattan distance from the seed is odd.
    4. Interior cells become the seed color S if their Manhattan distance from the
       seed is even and positive.
    Regions with only one distinct non-zero color or only background cells (0)
    remain unchanged.
    """
    # Convert to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # Define the structure for 8-way connectivity (including diagonals)
    connectivity_structure = np.ones((3, 3), dtype=bool)

    # Find connected components (regions) of non-zero cells
    # labeled_array assigns a unique integer label to each connected region
    # num_features is the total number of regions found (including background if not excluded)
    labeled_array, num_features = label(input_array > 0, structure=connectivity_structure)

    # Iterate through each found region (labels start from 1)
    for region_label in range(1, num_features + 1):
        # Get coordinates of all cells belonging to the current region
        region_coords = np.argwhere(labeled_array == region_label)
        if len(region_coords) == 0:
            continue # Skip if region is somehow empty

        # Get the integer values of cells within this region from the original input
        region_values = [input_array[r, c] for r, c in region_coords]

        # Count the frequency of each distinct value in the region
        value_counts = Counter(region_values)

        # Transformation rule only applies if there are exactly two distinct non-zero values
        if len(value_counts) < 2:
            # If only one color, or some error, leave this region unchanged and move to the next
            continue

        # Identify Component Color (C) - the most frequent color
        # Identify Seed Color (S) - the other color (less frequent)
        # Assumes exactly two colors based on problem description and examples
        component_color = value_counts.most_common(1)[0][0]
        seed_color = None
        for val in value_counts:
            if val != component_color:
                seed_color = val
                break
        
        # If for some reason a distinct seed color wasn't found (e.g., >2 colors), skip
        if seed_color is None:
             continue

        # Find the location (coordinates) of the Seed Cell (r_s, c_s)
        seed_coords = None
        for r, c in region_coords:
            if input_array[r, c] == seed_color:
                seed_coords = (r, c)
                break

        # If seed coordinates couldn't be found (shouldn't happen if seed_color exists), skip
        if seed_coords is None:
             continue
        r_s, c_s = seed_coords

        # Identify Boundary Cells for this region
        # Boundary cells are cells within the region adjacent (8-way) to a background cell (0)
        boundary_cells = set()
        for r, c in region_coords:
            is_boundary = False
            # Check all 8 neighbors
            for nr, nc in get_neighbors(r, c, rows, cols):
                # If a neighbor is background (value 0 in the original input), this cell is boundary
                if input_array[nr, nc] == 0:
                    is_boundary = True
                    break # Found a zero neighbor, no need to check others
            if is_boundary:
                boundary_cells.add((r, c))

        # Apply transformation rules to cells within this region
        for r, c in region_coords:
            current_coords = (r, c)

            # Rule 1: Seed cell becomes 0
            if current_coords == seed_coords:
                output_array[r, c] = 0
            # Rule 2: Boundary cells remain unchanged (they keep Component Color C)
            elif current_coords in boundary_cells:
                # No change needed, output_array already has the copied value
                pass
            # Rule 3: Interior cells (not seed, not boundary) change based on Manhattan distance
            else:
                manhattan_distance = abs(r - r_s) + abs(c - c_s)
                # Rule 3a: Odd distance -> become 0
                if manhattan_distance % 2 == 1:
                    output_array[r, c] = 0
                # Rule 3b: Even positive distance -> become Seed Color S
                else: # Distance is even and > 0 (since d=0 is the seed cell case)
                    output_array[r, c] = seed_color

    # Convert the final numpy array back to a list of lists
    return output_array.tolist()
```