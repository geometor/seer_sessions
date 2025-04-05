
## train_1

**input:**
```
0 0 0 6 0
0 0 0 6 0
0 0 0 6 0
4 4 4 4 3
0 0 0 5 0
```


**output:**
```
0 0 0 5 0
0 0 0 5 0
0 0 0 5 0
3 3 3 3 4
0 0 0 6 0
```


## train_2

**input:**
```
0 0 3 0 0
6 6 7 7 7
0 0 4 0 0
0 0 4 0 0
0 0 4 0 0
```


**output:**
```
0 0 4 0 0
7 7 6 6 6
0 0 3 0 0
0 0 3 0 0
0 0 3 0 0
```


## train_3

**input:**
```
0 0 6 0 0
0 0 6 0 0
0 0 6 0 0
8 8 8 8 8
0 0 7 0 0
```


**output:**
```
0 0 7 0 0
0 0 7 0 0
0 0 7 0 0
8 8 8 8 8
0 0 6 0 0
```

Okay, let's analyze the provided examples to understand the transformation logic.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are consistently 5x5 grids containing non-negative integers. The majority of cells are 0 (background).
2.  **Non-Zero Structures:** The non-zero values form distinct shapes or structures within the grid:
    *   A contiguous vertical line segment (all cells have the same non-zero value).
    *   A contiguous horizontal line segment (cells can have one or two distinct non-zero values).
    *   A single isolated non-zero cell.
3.  **Value Transformation:** The core transformation involves changing the *values* within these identified structures, while the *positions* of the structures themselves remain largely unchanged.
4.  **Interaction between Structures:** The transformation rules for the values within each structure seem dependent on the values present in the *other* structures. Specifically:
    *   The new value(s) for the horizontal segment depend on the original values within that segment.
    *   The new value for the vertical segment depends on the original value of the isolated cell.
    *   The new value for the isolated cell depends on the original value of the vertical segment.

**YAML Facts:**


```yaml
task_description: Processes a 2D grid to modify values within specific non-zero structures based on interactions between those structures.

grid_properties:
  type: 2D array of integers
  size: 5x5 (based on examples)
  background_value: 0

identified_objects:
  - object: horizontal_segment
    description: A contiguous sequence of non-zero cells along a single row.
    properties:
      - coordinates: Set of (row, col) tuples defining the segment.
      - values: List or set of non-zero integer values present in the segment cells.
      - unique_values: Set of distinct non-zero values.
    actions:
      - value_swap: If exactly two unique non-zero values (A, B) exist, all cells with A change to B, and all cells with B change to A. If only one unique value exists, values remain unchanged.
  - object: vertical_segment
    description: A contiguous sequence of non-zero cells along a single column, all having the same value.
    properties:
      - coordinates: Set of (row, col) tuples defining the segment.
      - value: The single non-zero integer value present in all segment cells.
    actions:
      - value_assignment: The value of all cells in this segment changes to the original value of the 'isolated_cell'.
  - object: isolated_cell
    description: A single non-zero cell that is not part of the horizontal or vertical segments.
    properties:
      - coordinates: The (row, col) tuple of the cell.
      - value: The non-zero integer value of the cell.
    actions:
      - value_assignment: The value of this cell changes to the original value of the 'vertical_segment'.

relationships:
  - The transformation rule for 'vertical_segment' depends on the initial state of 'isolated_cell'.
  - The transformation rule for 'isolated_cell' depends on the initial state of 'vertical_segment'.
  - The transformation rule for 'horizontal_segment' depends only on its own initial state (its unique values).

assumptions:
  - There is exactly one horizontal segment, one vertical segment, and one isolated cell in each input grid.
  - Segments are defined by contiguous non-zero values along a row or column.
  - The vertical segment always consists of cells with a single, uniform non-zero value.
  - The three structures (horizontal segment, vertical segment, isolated cell) do not spatially overlap in the input grid.
  - Zero cells remain zero in the output.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, or as a grid of zeros with the same dimensions.
2.  Identify the coordinates and values of the horizontal segment (contiguous non-zero cells in a single row). Store its unique non-zero values.
3.  Identify the coordinates and the single non-zero value (`V_val`) of the vertical segment (contiguous non-zero cells in a single column with the same value).
4.  Identify the coordinate and the non-zero value (`I_val`) of the isolated cell (the single non-zero cell not belonging to the horizontal or vertical segments).
5.  Determine the value transformation map for the horizontal segment:
    *   If the horizontal segment has exactly two unique non-zero values, `A` and `B`, create a mapping: `{A: B, B: A}`.
    *   If the horizontal segment has only one unique non-zero value, `A`, create a mapping: `{A: A}`.
6.  Iterate through the coordinates of the horizontal segment in the input grid. For each coordinate `(r, c)`, set the corresponding output grid cell `output[r][c]` to the mapped value based on the input value `input[r][c]` and the mapping created in step 5.
7.  Iterate through the coordinates of the vertical segment. For each coordinate `(r, c)`, set the corresponding output grid cell `output[r][c]` to the original value of the isolated cell (`I_val`).
8.  Retrieve the coordinate `(r_i, c_i)` of the isolated cell. Set the output grid cell `output[r_i][c_i]` to the original value of the vertical segment (`V_val`).
9.  Ensure all cells that were originally 0 in the input remain 0 in the output (this is handled if starting with a zero grid and only filling non-zero values, or by skipping zero cells if modifying a copy).
10. Return the completed output grid.
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
```python
import numpy as np
from collections import Counter

"""
Processes a 2D grid containing three distinct non-zero structures:
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
    # Use numpy's argwhere to efficiently find coordinates of non-zero elements
    non_zero_coords = np.argwhere(grid > 0)
    # Return a list of tuples: (row, column, value)
    return [(r, c, grid[r, c]) for r, c in non_zero_coords]

def find_segments(non_zero_cells):
    """
    Identifies the horizontal segment, vertical segment, and isolated cell
    based on their structural properties from the list of non-zero cells.
    This version uses frequency analysis and structural checks.
    """
    # Count occurrences of each row and column index among non-zero cells
    rows = Counter(r for r, c, v in non_zero_cells)
    cols = Counter(c for r, c, v in non_zero_cells)

    h_segment_coords = set()
    h_segment_values = []
    v_segment_coords = set()
    v_segment_value = None
    isolated_cell_coord = None
    isolated_cell_value = None

    # --- Identify Vertical Segment ---
    # A vertical segment should have multiple cells in the same column with the same value.
    potential_v_cols = {} # Store potential vertical columns: col_index -> (coords, value)
    for c, count in cols.items():
        if count > 1: # Segments usually have more than one cell
            col_cells = [(r_v, c_v, v) for r_v, c_v, v in non_zero_cells if c_v == c]
            col_values = set(v for _, _, v in col_cells)
            # Check for uniform value
            if len(col_values) == 1:
                rows_in_col = sorted([r_v for r_v, _, _ in col_cells])
                # Check for vertical contiguity
                is_contiguous = all(rows_in_col[i] == rows_in_col[0] + i for i in range(len(rows_in_col)))
                if is_contiguous:
                    potential_v_cols[c] = (set((r_v, c_v) for r_v, c_v, v in col_cells), col_cells[0][2])

    # Assume only one such structure exists per the problem description
    if len(potential_v_cols) == 1:
        v_col_index = list(potential_v_cols.keys())[0]
        v_segment_coords, v_segment_value = potential_v_cols[v_col_index]
    # Add handling if zero or multiple potential V segments found, maybe raise error or use longest?
    elif len(potential_v_cols) > 1:
         # If multiple, pick the longest one as the most likely candidate
         longest_v_col = -1
         max_len = 0
         for c, (coords, val) in potential_v_cols.items():
             if len(coords) > max_len:
                 max_len = len(coords)
                 longest_v_col = c
         if longest_v_col != -1:
             v_segment_coords, v_segment_value = potential_v_cols[longest_v_col]


    # --- Identify Horizontal Segment ---
    # A horizontal segment should have multiple cells in the same row.
    potential_h_rows = {} # Store potential horizontal rows: row_index -> (coords, values)
    for r, count in rows.items():
         if count > 1:
             row_cells = [(r_h, c_h, v) for r_h, c_h, v in non_zero_cells if r_h == r]
             cols_in_row = sorted([c_h for _, c_h, _ in row_cells])
             # Check for horizontal contiguity
             is_contiguous = all(cols_in_row[i] == cols_in_row[0] + i for i in range(len(cols_in_row)))
             if is_contiguous:
                  potential_h_rows[r] = (set((r_h, c_h) for r_h, c_h, v in row_cells), [v for _, _, v in row_cells])

    # Filter out any potential H segment that overlaps with the identified V segment
    valid_h_rows = {}
    for r, (coords, values) in potential_h_rows.items():
        if not (coords & v_segment_coords): # Check for intersection
             valid_h_rows[r] = (coords, values)

    # Assume only one valid H segment remains
    if len(valid_h_rows) == 1:
         h_row_index = list(valid_h_rows.keys())[0]
         h_segment_coords, h_segment_values = valid_h_rows[h_row_index]
    # Add handling if zero or multiple potential H segments found
    elif len(valid_h_rows) > 1:
         # If multiple valid ones, maybe pick based on row frequency or length?
         # Picking the one corresponding to the most frequent row index might be robust
         most_frequent_r = max(rows, key=rows.get)
         if most_frequent_r in valid_h_rows:
              h_segment_coords, h_segment_values = valid_h_rows[most_frequent_r]
         else: # Fallback: pick the longest non-overlapping one
             longest_h_row = -1
             max_len = 0
             for r, (coords, vals) in valid_h_rows.items():
                 if len(coords) > max_len:
                     max_len = len(coords)
                     longest_h_row = r
             if longest_h_row != -1:
                 h_segment_coords, h_segment_values = valid_h_rows[longest_h_row]


    # --- Identify Isolated Cell ---
    # The isolated cell is the non-zero cell not belonging to H or V segments.
    all_non_zero_coords = set((r, c) for r, c, v in non_zero_cells)
    segment_coords = h_segment_coords.union(v_segment_coords)
    isolated_coords_set = all_non_zero_coords - segment_coords

    if len(isolated_coords_set) == 1:
        iso_r, iso_c = isolated_coords_set.pop()
        isolated_cell_coord = (iso_r, iso_c)
        # Find the value corresponding to the isolated coordinate
        isolated_cell_value = [v for r, c, v in non_zero_cells if r == iso_r and c == iso_c][0]
    # Add handling if zero or multiple isolated cells are found


    # Final check: Ensure all three components were successfully identified
    if not h_segment_coords or not v_segment_coords or not isolated_cell_coord:
        # This indicates the input structure didn't match assumptions
        # Log detailed info for debugging
        # print(f"DEBUG: Failed Identification! H={h_segment_coords}, V={v_segment_coords}, Iso={isolated_cell_coord}")
        # print(f"Potential V Segments: {potential_v_cols}")
        # print(f"Potential H Segments: {potential_h_rows}")
        # print(f"Valid H Segments (no V overlap): {valid_h_rows}")
        # print(f"Isolated Candidates: {isolated_coords_set}")
        raise ValueError("Could not definitively identify all three required structures (horizontal, vertical, isolated).")

    # Return identified structures' details
    return (list(h_segment_coords), h_segment_values,
            list(v_segment_coords), v_segment_value,
            isolated_cell_coord, isolated_cell_value)


def transform(input_grid):
    """
    Applies the transformation rules to the input grid by identifying
    horizontal/vertical segments and an isolated cell, then swapping/assigning
    values based on the rules.
    """
    # Convert input to a NumPy array for efficient element access and manipulation
    grid = np.array(input_grid)
    # Create a copy to modify, preserving the original input grid
    output_grid = np.copy(grid)

    # Find all non-zero cells in the grid
    non_zero_cells = find_non_zero_cells(grid)

    # If there are no non-zero cells, return the grid as is
    if not non_zero_cells:
        return output_grid.tolist() # Return as list of lists

    try:
        # Identify the coordinates and original values of the three structures
        h_coords, h_values_orig, v_coords, v_value_orig, iso_coord, iso_value_orig = find_segments(non_zero_cells)
    except ValueError as e:
        # If segments can't be identified according to assumptions, return the original grid
        # This might happen if the input doesn't contain the expected three structures.
        print(f"Error during segment identification: {e}. Returning original grid.")
        return grid.tolist() # Return original as list of lists

    # --- Apply transformations to the output grid ---

    # 1. Horizontal Segment Transformation:
    # Find the unique values present in the horizontal segment
    unique_h_values = sorted(list(set(h_values_orig)))
    h_value_map = {}
    # If exactly two unique values exist, create a map to swap them
    if len(unique_h_values) == 2:
        val_a, val_b = unique_h_values
        h_value_map[val_a] = val_b
        h_value_map[val_b] = val_a
    # Otherwise (one unique value), create a map where values map to themselves (no change)
    else:
        for val in unique_h_values:
            h_value_map[val] = val

    # Iterate through the coordinates of the horizontal segment
    for r, c in h_coords:
        original_val = grid[r, c] # Get the original value from the input grid
        if original_val in h_value_map:
            # Apply the transformation using the map
            output_grid[r, c] = h_value_map[original_val]

    # 2. Vertical Segment Transformation:
    # Set all cells in the vertical segment to the original value of the isolated cell
    for r, c in v_coords:
        output_grid[r, c] = iso_value_orig

    # 3. Isolated Cell Transformation:
    # Set the isolated cell to the original value of the vertical segment
    iso_r, iso_c = iso_coord
    output_grid[iso_r, iso_c] = v_value_orig

    # 4. Zero cells remain zero (this is implicitly handled by starting with a copy
    #    and only modifying the non-zero cells identified in the segments)

    # Convert the final NumPy array back to a list of lists format
    return output_grid.tolist()
```
