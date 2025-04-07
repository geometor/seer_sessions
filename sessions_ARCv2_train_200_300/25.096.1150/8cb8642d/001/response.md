```python
"""
Transforms an input grid based on connected regions of non-zero numbers.

1. Identifies connected regions of non-zero cells (8-way connectivity).
2. For each region:
   a. Finds the predominant color (C) and the single different 'seed' color (S) and its location (r_s, c_s).
   b. Identifies boundary cells (region cells adjacent to 0s).
   c. Modifies the region in the output grid:
      - The seed cell becomes 0.
      - Boundary cells remain unchanged (keep color C).
      - Interior cells (not seed, not boundary) change based on Manhattan distance 'd' from the seed:
         - If 'd' is odd, the cell becomes 0.
         - If 'd' is even (and > 0), the cell becomes the seed color S.
3. Cells with value 0 remain unchanged.
"""

import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter

def get_neighbors(r, c, rows, cols):
    """Generates coordinates of 8 neighbors for a cell (r, c)."""
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                yield nr, nc

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the transformed 2D output grid.
    """
    # Convert to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # Define the structure for 8-way connectivity
    connectivity_structure = np.ones((3, 3), dtype=bool)

    # Find connected components (regions) of non-zero cells
    labeled_array, num_features = label(input_array > 0, structure=connectivity_structure)

    # Iterate through each found region
    for region_label in range(1, num_features + 1):
        # Get coordinates of cells in the current region
        region_coords = np.argwhere(labeled_array == region_label)
        if len(region_coords) == 0:
            continue # Should not happen with label starting from 1

        # Get the values of cells in the region
        region_values = [input_array[r, c] for r, c in region_coords]

        # Find Component Color (C) and Seed Color (S)
        if not region_values:
             continue # Skip empty regions if any

        value_counts = Counter(region_values)
        if len(value_counts) < 2:
             # Region has only one color type - might be just boundary? Or only seed?
             # Based on examples, seems regions always have C and S.
             # If it's all one color, maybe no transformation needed?
             # Let's assume the problem guarantees distinct C and S.
             # If a region has only one cell, it's both seed and boundary? Let's test.
             # In train_1, the single 1 is seed, it becomes 0. It's not boundary.
             # If the region is just [1], C=None, S=1. Seed becomes 0. Rule works.
             # If the region is [2, 2, 2], C=2, S=None. No seed? This shouldn't happen per problem description.
             # Let's proceed assuming len(value_counts) >= 1. If len==1, that value is S. If len > 1, find C and S.
             if len(value_counts) == 1:
                 seed_color = region_values[0]
                 component_color = None # No component color if only seed exists
             else:
                 # Most common is component color C
                 component_color = value_counts.most_common(1)[0][0]
                 # Find the seed color S (the one that's not C)
                 seed_color = None
                 for val in value_counts:
                     if val != component_color:
                         seed_color = val
                         break
                 if seed_color is None: # Should not happen if len(value_counts) >= 2
                      continue

        # Find Seed Cell location (r_s, c_s)
        seed_coords = None
        for r, c in region_coords:
            if input_array[r, c] == seed_color:
                seed_coords = (r, c)
                break
        
        if seed_coords is None: # Should not happen if seed_color was found
             continue
        r_s, c_s = seed_coords

        # Identify boundary cells for this region
        boundary_cells = set()
        for r, c in region_coords:
            is_boundary = False
            for nr, nc in get_neighbors(r, c, rows, cols):
                # Check if neighbor is outside region (either 0 or belongs to another region)
                if labeled_array[nr, nc] != region_label: # Check against labeled array
                     # Special check for background: ensure the neighbour is truly 0 in input
                     if input_array[nr,nc] == 0:
                          is_boundary = True
                          break # Found a zero neighbor, it's a boundary cell
            if is_boundary:
                boundary_cells.add((r, c))

        # Apply transformation rules to cells in the region
        for r, c in region_coords:
            # Rule 1: Seed cell becomes 0
            if (r, c) == seed_coords:
                output_array[r, c] = 0
            # Rule 2: Boundary cells remain unchanged (already copied)
            elif (r, c) in boundary_cells:
                # output_array[r, c] = component_color # Already holds this value from copy
                pass # No change needed
            # Rule 3: Interior cells change based on Manhattan distance
            else:
                manhattan_distance = abs(r - r_s) + abs(c - c_s)
                if manhattan_distance % 2 == 1: # Odd distance
                    output_array[r, c] = 0
                else: # Even distance (and > 0, since seed case handled)
                    output_array[r, c] = seed_color

    # Convert back to list of lists
    return output_array.tolist()

```