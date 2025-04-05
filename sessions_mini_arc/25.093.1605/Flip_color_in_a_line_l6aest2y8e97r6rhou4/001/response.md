```python
import numpy as np
from collections import Counter

"""
Processes a 2D grid (5x5 based on examples) containing three distinct non-zero structures:
1. A horizontal segment: Contiguous non-zero cells in a single row.
2. A vertical segment: Contiguous non-zero cells in a single column, all with the same value.
3. An isolated cell: A single non-zero cell not part of the other two segments.

The transformation rules are:
- Horizontal Segment: If it contains exactly two unique non-zero values (A, B), swap them (A becomes B, B becomes A). Otherwise, values remain unchanged.
- Vertical Segment: All cells in this segment take the original value of the isolated cell.
- Isolated Cell: This cell takes the original value of the vertical segment.
- Zero cells remain zero.
"""

def find_non_zero_cells(grid):
    """Finds all non-zero cells and returns their coordinates and values."""
    non_zero_coords = np.argwhere(grid > 0)
    return [(r, c, grid[r, c]) for r, c in non_zero_coords]

def find_segments(non_zero_cells):
    """
    Identifies the horizontal segment, vertical segment, and isolated cell
    based on their structural properties from the list of non-zero cells.
    """
    rows = Counter(r for r, c, v in non_zero_cells)
    cols = Counter(c for r, c, v in non_zero_cells)

    h_segment_coords = set()
    h_segment_values = []
    v_segment_coords = set()
    v_segment_value = None
    isolated_cell_coord = None
    isolated_cell_value = None

    # Identify potential horizontal segment row (most frequent row)
    # Identify potential vertical segment column (most frequent col with uniform value potential)
    
    potential_h_row = max(rows, key=rows.get) if rows else -1
    potential_v_col = -1
    max_col_count = 0
    
    # Find potential vertical segment column more carefully, checking value uniformity
    for c, count in cols.items():
        if count > 1: # A vertical segment must have length > 1 based on examples
            col_cells = [(r_v, c_v, v) for r_v, c_v, v in non_zero_cells if c_v == c]
            if len(set(v for r_v, c_v, v in col_cells)) == 1: # Check for uniform value
                 # Check for vertical contiguity
                 rows_in_col = sorted([r_v for r_v, c_v, v in col_cells])
                 is_contiguous = all(rows_in_col[i] == rows_in_col[0] + i for i in range(len(rows_in_col)))
                 if is_contiguous and count > max_col_count:
                     potential_v_col = c
                     max_col_count = count

    # Refine segment identification based on properties
    temp_h_coords = set()
    temp_v_coords = set()

    # Build vertical segment first if found
    if potential_v_col != -1:
         col_cells = [(r_v, c_v, v) for r_v, c_v, v in non_zero_cells if c_v == potential_v_col]
         # Verify again it's likely the vertical segment (uniform value, length > 1)
         if len(col_cells) > 1 and len(set(v for _, _, v in col_cells)) == 1:
             v_segment_coords = set((r_v, c_v) for r_v, c_v, v in col_cells)
             v_segment_value = col_cells[0][2] # Get the uniform value

    # Build horizontal segment
    row_cells = [(r_h, c_h, v) for r_h, c_h, v in non_zero_cells if r_h == potential_h_row]
     # Check for horizontal contiguity
    if row_cells:
        cols_in_row = sorted([c_h for r_h, c_h, v in row_cells])
        is_contiguous = all(cols_in_row[i] == cols_in_row[0] + i for i in range(len(cols_in_row)))
        if is_contiguous:
             # Ensure these cells are not part of the identified vertical segment
             potential_h_coords = set((r_h, c_h) for r_h, c_h, v in row_cells)
             if not (potential_h_coords & v_segment_coords): # Check for overlap
                h_segment_coords = potential_h_coords
                h_segment_values = [v for r_h, c_h, v in row_cells]


    # Find the isolated cell (the one not in H or V segments)
    all_non_zero_coords = set((r, c) for r, c, v in non_zero_cells)
    segment_coords = h_segment_coords.union(v_segment_coords)
    isolated_coords = all_non_zero_coords - segment_coords

    if len(isolated_coords) == 1:
        iso_r, iso_c = isolated_coords.pop()
        isolated_cell_coord = (iso_r, iso_c)
        isolated_cell_value = [v for r, c, v in non_zero_cells if r == iso_r and c == iso_c][0]
    else:
        # This case shouldn't happen based on assumptions, but handle defensively
        # Or raise an error if assumptions must hold strictly
        print(f"Warning: Expected 1 isolated cell, found {len(isolated_coords)}. Grid analysis might be incorrect.")
        # Attempt to find a single cell if others failed
        if not h_segment_coords or not v_segment_coords:
             potential_isolated = [ (r,c,v) for r,c,v in non_zero_cells if (r,c) not in h_segment_coords and (r,c) not in v_segment_coords]
             if len(potential_isolated) == 1:
                 iso_r, iso_c, iso_v = potential_isolated[0]
                 isolated_cell_coord = (iso_r, iso_c)
                 isolated_cell_value = iso_v
                 # Need to re-evaluate h/v segments if they weren't fully ID'd before
                 if not h_segment_coords:
                    # Find the remaining group likely being horizontal
                     remaining_coords = all_non_zero_coords - v_segment_coords - set([isolated_cell_coord])
                     if remaining_coords:
                         h_segment_coords = remaining_coords
                         h_segment_values = [v for r, c, v in non_zero_cells if (r,c) in h_segment_coords]
                 if not v_segment_coords:
                    # Find the remaining group likely being vertical
                     remaining_coords = all_non_zero_coords - h_segment_coords - set([isolated_cell_coord])
                     if remaining_coords:
                         vals = [v for r, c, v in non_zero_cells if (r,c) in remaining_coords]
                         if len(set(vals)) == 1:
                             v_segment_coords = remaining_coords
                             v_segment_value = vals[0]


    # Final check for robustness - ensure segments were found
    if not h_segment_coords or not v_segment_coords or not isolated_cell_coord:
         raise ValueError("Could not definitively identify all three required structures (horizontal, vertical, isolated).")


    return (list(h_segment_coords), h_segment_values,
            list(v_segment_coords), v_segment_value,
            isolated_cell_coord, isolated_cell_value)


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    Identifies horizontal segment, vertical segment, and isolated cell.
    Swaps values in horizontal segment if two unique values exist.
    Sets vertical segment cells to the original isolated cell value.
    Sets the isolated cell to the original vertical segment value.
    """
    # Convert input to numpy array for easier handling
    grid = np.array(input_grid)
    output_grid = np.copy(grid) # Start with a copy

    # Find all non-zero cells
    non_zero_cells = find_non_zero_cells(grid)
    if not non_zero_cells:
        return output_grid # Return original if grid is empty or all zeros

    # Identify the three structures and their properties
    try:
        h_coords, h_values, v_coords, v_value_orig, iso_coord, iso_value_orig = find_segments(non_zero_cells)
    except ValueError as e:
        print(f"Error during segment identification: {e}")
        # Decide how to handle error: return original, return empty, etc.
        # For now, returning original grid seems safest if structure isn't as expected.
        return grid # Or output_grid if you prefer the copy

    # --- Apply transformations ---

    # 1. Horizontal Segment Transformation
    unique_h_values = sorted(list(set(h_values)))
    h_value_map = {}
    if len(unique_h_values) == 2:
        # Swap values if exactly two unique values
        val_a, val_b = unique_h_values
        h_value_map[val_a] = val_b
        h_value_map[val_b] = val_a
    else:
        # Otherwise, map values to themselves (no change)
        for val in unique_h_values:
            h_value_map[val] = val

    # Apply map to horizontal segment cells in output grid
    for r, c in h_coords:
        original_val = grid[r, c]
        if original_val in h_value_map: # Ensure value exists in map
             output_grid[r, c] = h_value_map[original_val]
        # else: # Should not happen if h_values are derived correctly
        #    print(f"Warning: Value {original_val} at {r,c} not in h_value_map")


    # 2. Vertical Segment Transformation
    # Set all vertical segment cells to the original value of the isolated cell
    for r, c in v_coords:
        output_grid[r, c] = iso_value_orig

    # 3. Isolated Cell Transformation
    # Set the isolated cell to the original value of the vertical segment
    iso_r, iso_c = iso_coord
    output_grid[iso_r, iso_c] = v_value_orig

    # 4. Zero cells remain zero (handled by starting with a copy)

    # Convert back to list of lists if necessary, otherwise return numpy array
    # return output_grid.tolist()
    return output_grid
```