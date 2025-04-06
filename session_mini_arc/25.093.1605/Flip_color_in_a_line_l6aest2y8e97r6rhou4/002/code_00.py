import numpy as np
from collections import Counter

# --- [Previous code for find_non_zero_cells remains the same] ---

def find_non_zero_cells(grid):
    """Finds all non-zero cells and returns their coordinates and values."""
    non_zero_coords = np.argwhere(grid > 0)
    return [(r, c, grid[r, c]) for r, c in non_zero_coords]

def find_segments(non_zero_cells, grid_shape):
    """
    Identifies the horizontal segment, vertical segment, and isolated cell
    based on their structural properties from the list of non-zero cells.
    Includes debugging prints.
    """
    print(f"DEBUG: Non-zero cells received: {non_zero_cells}")
    rows = Counter(r for r, c, v in non_zero_cells)
    cols = Counter(c for r, c, v in non_zero_cells)
    print(f"DEBUG: Row counts: {rows}")
    print(f"DEBUG: Col counts: {cols}")

    h_segment_coords = set()
    h_segment_values = []
    v_segment_coords = set()
    v_segment_value = None
    isolated_cell_coord = None
    isolated_cell_value = None

    potential_h_row = max(rows, key=rows.get) if rows else -1
    print(f"DEBUG: Potential H row (most frequent): {potential_h_row}")

    potential_v_col = -1
    max_col_count = 0
    # Find potential vertical segment column more carefully, checking value uniformity
    for c, count in cols.items():
         print(f"DEBUG: Checking col {c} with count {count}")
         if count > 1: # A vertical segment must have length > 1 based on examples
            col_cells = [(r_v, c_v, v) for r_v, c_v, v in non_zero_cells if c_v == c]
            col_values = set(v for r_v, c_v, v in col_cells)
            print(f"DEBUG:   Col {c} cells: {col_cells}, Values: {col_values}")
            if len(col_values) == 1: # Check for uniform value
                 rows_in_col = sorted([r_v for r_v, c_v, v in col_cells])
                 is_contiguous = all(rows_in_col[i] == rows_in_col[0] + i for i in range(len(rows_in_col)))
                 print(f"DEBUG:   Col {c} uniform value ({col_values.pop()}), contiguous: {is_contiguous}")
                 if is_contiguous and count > max_col_count:
                     potential_v_col = c
                     max_col_count = count
                     print(f"DEBUG:   Setting potential V col to {c}")


    print(f"DEBUG: Potential V col identified: {potential_v_col}")

    # Build vertical segment first if found
    if potential_v_col != -1:
         col_cells = [(r_v, c_v, v) for r_v, c_v, v in non_zero_cells if c_v == potential_v_col]
         # Verify again it's likely the vertical segment (uniform value, length > 1, contiguity)
         if len(col_cells) > 1 and len(set(v for _, _, v in col_cells)) == 1:
             rows_in_col = sorted([r_v for r_v, _, _ in col_cells])
             is_contiguous = all(rows_in_col[i] == rows_in_col[0] + i for i in range(len(rows_in_col)))
             if is_contiguous:
                v_segment_coords = set((r_v, c_v) for r_v, c_v, v in col_cells)
                v_segment_value = col_cells[0][2] # Get the uniform value
                print(f"DEBUG: Confirmed V Segment: Coords={v_segment_coords}, Value={v_segment_value}")
             else:
                print(f"DEBUG: V Segment candidate (Col {potential_v_col}) failed contiguity check.")
         else:
             print(f"DEBUG: V Segment candidate (Col {potential_v_col}) failed value uniformity or length check.")


    # Build horizontal segment
    if potential_h_row != -1:
        row_cells = [(r_h, c_h, v) for r_h, c_h, v in non_zero_cells if r_h == potential_h_row]
        print(f"DEBUG: Potential H row ({potential_h_row}) cells: {row_cells}")
        # Check for horizontal contiguity
        if row_cells:
            cols_in_row = sorted([c_h for r_h, c_h, v in row_cells])
            is_contiguous = all(cols_in_row[i] == cols_in_row[0] + i for i in range(len(cols_in_row)))
            print(f"DEBUG:   Potential H segment contiguous: {is_contiguous}")
            if is_contiguous:
                 # Ensure these cells are not part of the identified vertical segment
                 potential_h_coords = set((r_h, c_h) for r_h, c_h, v in row_cells)
                 print(f"DEBUG:   Potential H Coords: {potential_h_coords}")
                 print(f"DEBUG:   Overlap with V Coords ({v_segment_coords}): {potential_h_coords & v_segment_coords}")
                 if not (potential_h_coords & v_segment_coords): # Check for overlap
                    h_segment_coords = potential_h_coords
                    h_segment_values = [v for r_h, c_h, v in row_cells]
                    print(f"DEBUG: Confirmed H Segment: Coords={h_segment_coords}, Values={h_segment_values}")
                 else:
                    print(f"DEBUG: Potential H segment overlaps with V segment.")
            else:
                 print(f"DEBUG: Potential H segment failed contiguity check.")
        else:
            print(f"DEBUG: No cells found for potential H row {potential_h_row}")
    else:
        print(f"DEBUG: No potential H row identified.")


    # Find the isolated cell (the one not in H or V segments)
    all_non_zero_coords = set((r, c) for r, c, v in non_zero_cells)
    segment_coords = h_segment_coords.union(v_segment_coords)
    isolated_coords = all_non_zero_coords - segment_coords
    print(f"DEBUG: All non-zero coords: {all_non_zero_coords}")
    print(f"DEBUG: Identified segment coords (H+V): {segment_coords}")
    print(f"DEBUG: Potential isolated coords: {isolated_coords}")


    if len(isolated_coords) == 1:
        iso_r, iso_c = isolated_coords.pop()
        isolated_cell_coord = (iso_r, iso_c)
        # Find the value corresponding to the isolated coordinate
        isolated_cell_value = [v for r, c, v in non_zero_cells if r == iso_r and c == iso_c][0]
        print(f"DEBUG: Confirmed Isolated Cell: Coord={isolated_cell_coord}, Value={isolated_cell_value}")
    elif len(isolated_coords) > 1 and not h_segment_coords and v_segment_coords:
        # Attempt fallback: If V is found, H wasn't (maybe not most frequent row?), 
        # assume remaining cells > 1 are H, and only 1 is isolated.
        print("DEBUG: Fallback attempt: Multiple isolated candidates, H segment likely misidentified.")
        # Check if remaining cells form a contiguous horizontal line
        potential_h_coords = isolated_coords
        rows_in_potential_h = set(r for r, c in potential_h_coords)
        if len(rows_in_potential_h) == 1: # All remaining are in the same row
             potential_h_row = rows_in_potential_h.pop()
             cols_in_potential_h = sorted(c for r, c in potential_h_coords if r == potential_h_row)
             is_contiguous = all(cols_in_potential_h[i] == cols_in_potential_h[0] + i for i in range(len(cols_in_potential_h)))
             if is_contiguous:
                 print(f"DEBUG: Fallback: Found contiguous horizontal segment in row {potential_h_row}")
                 # This doesn't help find the *single* isolated cell yet. Need better logic.
                 # Maybe the isolated cell is the one *not* in the most frequent row *or* potential V col?
                 
    elif len(isolated_coords) > 1 and not v_segment_coords and h_segment_coords:
         print("DEBUG: Fallback attempt: Multiple isolated candidates, V segment likely misidentified.")
         # Similar logic for finding V if H was found but V wasn't.
         
    else:
         print(f"DEBUG: Could not isolate single cell. Found {len(isolated_coords)} candidates: {isolated_coords}")


    # Final check for robustness - ensure segments were found
    if not h_segment_coords or not v_segment_coords or not isolated_cell_coord:
         print(f"DEBUG: Final Check Failed: H={h_segment_coords}, V={v_segment_coords}, Iso={isolated_cell_coord}")
         raise ValueError("Could not definitively identify all three required structures (horizontal, vertical, isolated).")


    return (list(h_segment_coords), h_segment_values,
            list(v_segment_coords), v_segment_value,
            isolated_cell_coord, isolated_cell_value)


def transform(input_grid):
    """
    Applies the transformation rules to the input grid. Includes debug prints.
    """
    grid = np.array(input_grid)
    output_grid = np.copy(grid) 
    print(f"\n--- Processing Input Grid ---")
    print(grid)

    non_zero_cells = find_non_zero_cells(grid)
    if not non_zero_cells:
        print("DEBUG: Grid is empty or all zeros. Returning copy.")
        return output_grid.tolist() 

    try:
        print("DEBUG: Calling find_segments...")
        h_coords, h_values, v_coords, v_value_orig, iso_coord, iso_value_orig = find_segments(non_zero_cells, grid.shape)
        print("DEBUG: find_segments successful.")
        print(f"DEBUG: H Coords: {h_coords}, H Values: {h_values}")
        print(f"DEBUG: V Coords: {v_coords}, V Value Orig: {v_value_orig}")
        print(f"DEBUG: Iso Coord: {iso_coord}, Iso Value Orig: {iso_value_orig}")

    except ValueError as e:
        print(f"DEBUG: Error during segment identification: {e}")
        print("DEBUG: Returning original grid due to error.")
        # Return as list of lists matching expected format
        return grid.tolist() 

    # --- Apply transformations ---
    print("DEBUG: Applying transformations...")

    # 1. Horizontal Segment Transformation
    unique_h_values = sorted(list(set(h_values)))
    h_value_map = {}
    if len(unique_h_values) == 2:
        val_a, val_b = unique_h_values
        h_value_map[val_a] = val_b
        h_value_map[val_b] = val_a
        print(f"DEBUG: H Swap Map: {h_value_map}")
    else:
        for val in unique_h_values:
            h_value_map[val] = val
        print(f"DEBUG: H No-Swap Map: {h_value_map}")

    for r, c in h_coords:
        original_val = grid[r, c]
        if original_val in h_value_map: 
             output_grid[r, c] = h_value_map[original_val]
             print(f"DEBUG: Applied H map: ({r},{c}) = {h_value_map[original_val]}")
        else: 
           print(f"Warning: Value {original_val} at {r,c} not in h_value_map")


    # 2. Vertical Segment Transformation
    print(f"DEBUG: Applying V transformation: Setting V cells to {iso_value_orig}")
    for r, c in v_coords:
        output_grid[r, c] = iso_value_orig
        print(f"DEBUG: Applied V map: ({r},{c}) = {iso_value_orig}")

    # 3. Isolated Cell Transformation
    iso_r, iso_c = iso_coord
    print(f"DEBUG: Applying Iso transformation: Setting Iso cell ({iso_r},{iso_c}) to {v_value_orig}")
    output_grid[iso_r, iso_c] = v_value_orig

    print("DEBUG: Transformations complete.")
    print("Final Output Grid:")
    print(output_grid)
    # Convert back to list of lists 
    return output_grid.tolist()

# Example Inputs
train_1_input = [
    [0, 0, 0, 6, 0],
    [0, 0, 0, 6, 0],
    [0, 0, 0, 6, 0],
    [4, 4, 4, 4, 3],
    [0, 0, 0, 5, 0]
]

train_2_input = [
    [0, 0, 3, 0, 0],
    [6, 6, 7, 7, 7],
    [0, 0, 4, 0, 0],
    [0, 0, 4, 0, 0],
    [0, 0, 4, 0, 0]
]

train_3_input = [
    [0, 0, 6, 0, 0],
    [0, 0, 6, 0, 0],
    [0, 0, 6, 0, 0],
    [8, 8, 8, 8, 8],
    [0, 0, 7, 0, 0]
]

# Test Execution
print("--- Running Train Example 1 ---")
output_1 = transform(train_1_input)
# print(f"Output 1:\n{np.array(output_1)}") # Print numpy array for better formatting

print("\n--- Running Train Example 2 ---")
output_2 = transform(train_2_input)
# print(f"Output 2:\n{np.array(output_2)}")

print("\n--- Running Train Example 3 ---")
output_3 = transform(train_3_input)
# print(f"Output 3:\n{np.array(output_3)}")
