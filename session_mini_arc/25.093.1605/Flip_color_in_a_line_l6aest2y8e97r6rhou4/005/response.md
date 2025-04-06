```python
import numpy as np
from collections import Counter

"""
Processes a 2D grid containing non-zero integers forming specific structures. 
It identifies a unique vertical segment (contiguous, uniform value, length>1), 
a unique horizontal segment (contiguous, length>1, values can vary), 
which do not overlap spatially, and a unique isolated non-zero cell 
(not part of either identified segment). It then swaps/assigns values:
- Horizontal Segment: If it originally had exactly two unique non-zero values (A, B), 
  they are swapped (A->B, B->A) in the output. Otherwise, values remain unchanged.
- Vertical Segment: Its cells in the output take the original value of the isolated cell.
- Isolated Cell: Its cell in the output takes the original value of the vertical segment.
- Zero cells remain zero.
The identification relies on finding the unique non-overlapping pair of 
potential vertical and horizontal segments.
"""

def find_non_zero_cells(grid):
    """Finds all non-zero cells and returns their coordinates and values."""
    non_zero_coords = np.argwhere(grid > 0)
    return [(r, c, grid[r, c]) for r, c in non_zero_coords]

def find_potential_vertical_segments(grid, non_zero_cells):
    """
    Finds all potential vertical segments (contiguous, uniform value, length > 1).
    Returns a list of dictionaries, each with 'coords' (set) and 'value'.
    """
    non_zero_coords_set = set((r, c) for r, c, v in non_zero_cells)
    potential_segments = []
    processed_coords = set()

    # Sort cells primarily by column, then row to help processing
    sorted_cells = sorted(non_zero_cells, key=lambda x: (x[1], x[0]))

    for r_start, c_start, v_start in sorted_cells:
        if (r_start, c_start) in processed_coords:
            continue

        # Check downwards for contiguous cells with the same value
        current_segment_coords = [(r_start, c_start)]
        current_r = r_start + 1
        while (current_r, c_start) in non_zero_coords_set and grid[current_r, c_start] == v_start:
            current_segment_coords.append((current_r, c_start))
            current_r += 1

        # Store if it's a valid segment (length > 1)
        if len(current_segment_coords) > 1:
            segment_set = set(current_segment_coords)
            potential_segments.append({"coords": segment_set, "value": v_start})
            processed_coords.update(segment_set) # Mark all segment cells as processed
        else:
             processed_coords.add((r_start, c_start)) # Mark single cell as processed

    return potential_segments

def find_potential_horizontal_segments(grid, non_zero_cells):
    """
    Finds all potential horizontal segments (contiguous, length > 1). Values can vary.
    Returns a list of dictionaries, each with 'coords' (set) and 'values' (list).
    """
    non_zero_coords_set = set((r, c) for r, c, v in non_zero_cells)
    potential_segments = []
    processed_coords = set()

    # Sort cells primarily by row, then column
    sorted_cells = sorted(non_zero_cells, key=lambda x: (x[0], x[1]))

    for r_start, c_start, v_start in sorted_cells:
        if (r_start, c_start) in processed_coords:
            continue

        # Check rightwards for contiguous cells
        current_segment_coords = [(r_start, c_start)]
        current_c = c_start + 1
        while (r_start, current_c) in non_zero_coords_set:
            current_segment_coords.append((r_start, current_c))
            current_c += 1

        # Store if it's a valid segment (length > 1)
        if len(current_segment_coords) > 1:
            segment_set = set(current_segment_coords)
            # Ensure coords are sorted by column for consistent 'values' list
            sorted_coords_list = sorted(list(segment_set), key=lambda x: x[1])
            values = [grid[r, c] for r, c in sorted_coords_list]
            potential_segments.append({"coords": segment_set, "values": values})
            processed_coords.update(segment_set)
        else:
            processed_coords.add((r_start, c_start))

    return potential_segments

def find_correct_segments(potential_v, potential_h):
    """
    Finds the unique non-overlapping pair of vertical and horizontal segments.
    Returns (v_segment, h_segment) or (None, None) if not found or ambiguous.
    """
    non_overlapping_pairs = []
    for v_seg in potential_v:
        for h_seg in potential_h:
            # Check for disjoint sets of coordinates
            if not (v_seg['coords'] & h_seg['coords']):
                non_overlapping_pairs.append((v_seg, h_seg))

    # Expect exactly one non-overlapping pair based on problem constraints
    if len(non_overlapping_pairs) == 1:
        return non_overlapping_pairs[0]
    else:
        # Log error or warning if 0 or >1 pairs found
        # print(f"Warning/Error: Found {len(non_overlapping_pairs)} non-overlapping segment pairs.")
        return None, None # Indicate failure

def find_isolated_cell(grid, all_nz_coords_set, v_coords, h_coords):
    """
    Finds the single non-zero cell not belonging to the identified segments.
    Returns {'coord': (r, c), 'value': val} or None if not found/ambiguous.
    """
    segment_coords = v_coords.union(h_coords)
    isolated_coords_set = all_nz_coords_set - segment_coords

    if len(isolated_coords_set) == 1:
        iso_coord = isolated_coords_set.pop()
        iso_value = grid[iso_coord[0], iso_coord[1]]
        return {"coord": iso_coord, "value": iso_value}
    else:
        # Log error or warning
        # print(f"Warning/Error: Found {len(isolated_coords_set)} isolated cell candidates.")
        return None # Indicate failure


def transform(input_grid):
    """
    Applies the transformation rules after identifying the unique non-overlapping
    vertical segment, horizontal segment, and isolated cell.
    """
    # Initialize grid using numpy for convenience
    grid = np.array(input_grid)
    output_grid = np.copy(grid)

    # --- Identification Phase ---
    non_zero_cells = find_non_zero_cells(grid)
    if not non_zero_cells:
        return output_grid.tolist() # Return original if empty

    all_nz_coords_set = set((r, c) for r, c, v in non_zero_cells)

    # Find all potential segments
    potential_v = find_potential_vertical_segments(grid, non_zero_cells)
    potential_h = find_potential_horizontal_segments(grid, non_zero_cells)

    # Find the correct, non-overlapping pair
    true_v_segment, true_h_segment = find_correct_segments(potential_v, potential_h)

    # If the correct pair wasn't found, return original (robustness)
    if not true_v_segment or not true_h_segment:
        # print("Failed to identify unique non-overlapping segments. Returning original grid.")
        return grid.tolist()

    # Find the isolated cell using the coordinates of the true segments
    isolated_cell = find_isolated_cell(grid, all_nz_coords_set, true_v_segment['coords'], true_h_segment['coords'])

    # If isolated cell wasn't found uniquely, return original
    if not isolated_cell:
        # print("Failed to identify unique isolated cell. Returning original grid.")
        return grid.tolist()

    # Extract original values needed for transformation
    v_val_orig = true_v_segment['value']
    h_vals_orig = true_h_segment['values']
    i_val_orig = isolated_cell['value']
    v_coords = true_v_segment['coords']
    h_coords = true_h_segment['coords']
    iso_coord = isolated_cell['coord']

    # --- Transformation Phase ---

    # 1. Determine Horizontal Segment transformation map
    unique_h_values = sorted(list(set(h_vals_orig)))
    h_value_map = {}
    if len(unique_h_values) == 2:
        val_a, val_b = unique_h_values
        h_value_map[val_a] = val_b
        h_value_map[val_b] = val_a
    else:
        # Only one unique value, or more than two -> map to self (no change)
        for val in unique_h_values:
            h_value_map[val] = val

    # 2. Apply transformations to output_grid

    # Apply Horizontal transformation
    for r, c in h_coords:
        original_val = grid[r, c]
        if original_val in h_value_map: # Should always be true if logic is correct
            output_grid[r, c] = h_value_map[original_val]

    # Apply Vertical transformation
    for r, c in v_coords:
        output_grid[r, c] = i_val_orig

    # Apply Isolated Cell transformation
    iso_r, iso_c = iso_coord
    output_grid[iso_r, iso_c] = v_val_orig

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```