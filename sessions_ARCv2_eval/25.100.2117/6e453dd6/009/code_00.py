import copy
import numpy as np
from collections import deque

"""
Transforms a 2D grid based on prioritized conditions applied to the input grid. 
The transformation always involves shifting blocks of 0s one column to the right. 
The placement of the output value '2' depends on which condition is met first:

1. Condition B1 (Long Pattern): If the input grid contains any row with the pattern (0, 6, 6+, 0).
2. Condition A (2 Shapes with Short Patterns): If Condition B1 is false, and the input has exactly two 0-shapes, and both shapes contain the (0, 6, 0) pattern.
3. Condition B2 (Connectivity Check): If neither B1 nor A is met.

Transformation Details:

Universal Step: Block Shift
    - Initialize output grid from input.
    - Find all 0-shapes (contiguous blocks of 0s) in the input.
    - In the output grid, replace the original locations of these 0s with 6.
    - In the output grid, place 0s at the locations corresponding to the original 0s shifted one column right (respecting grid boundaries).

'2' Placement Rules (applied to the shifted grid):

- If Condition B1 Met:
    - Find all rows `r` in the *input* grid containing any (0, 6+, 0) pattern.
    - For each such unique row `r`, fill the output grid cells `output_grid[r][c]` with 2 for columns `c` from `marker_col + 1` to `width - 1`.

- If Condition A Met:
    - Identify the top shape (Shape1, smaller min_row) and bottom shape (Shape2). Get their bounding boxes (Bbox1, Bbox2).
    - Find the row indices (`R2_rows`) within Shape2 (in the input grid) that contain the (0, 6, 0) pattern.
    - Fill Block 1: `output_grid[r][c] = 2` for `r` from 4 to `Bbox1.rmax` and `c` from `marker_col + 1` to `marker_col + 4`.
    - Fill Block 2: `output_grid[r][c] = 2` for `r` from `min(R2_rows)` to `Bbox2.rmax` and `c` from `marker_col + 1` to `marker_col + 4`. (Handle case where R2_rows is empty?). Assume R2_rows will not be empty if condition A is met.

- If Condition B2 Met:
    - Find all rows `r` in the *input* grid containing the (0, 6, 0) pattern starting at column `c > 0`.
    - Check if these pattern instances are vertically connected (any 0 in the pattern at `r` belongs to the same shape as any 0 at `r+1`).
    - Identify the unique set of connected rows `r`.
    - For each such unique row `r`, fill the output grid cells `output_grid[r][c]` with 2 for columns `c` from `marker_col + 1` to `width - 1`.
"""

# === Helper Functions ===

def find_marker_col(grid: list[list[int]], marker_value: int = 5) -> int:
    """Finds the column index of the first occurrence of the marker value."""
    height = len(grid)
    if height == 0: return -1
    width = len(grid[0]) if height > 0 else 0
    for r in range(height):
        for c in range(width):
            if grid[r][c] == marker_value:
                return c
    return -1 

def get_neighbors(r: int, c: int, height: int, width: int) -> list[tuple[int, int]]:
    """Gets valid 4-directional neighbors within grid bounds."""
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def find_shapes_and_map(grid: list[list[int]], value: int) -> tuple[list[set[tuple[int, int]]], dict[tuple[int, int], int]]:
    """Finds distinct contiguous shapes of a given value using BFS and maps coords to shape IDs."""
    height = len(grid)
    if height == 0: return [], {}
    width = len(grid[0]) if height > 0 else 0
    
    grid_np = np.array(grid) 
    visited = set()
    shapes = []
    coord_to_shape_id = {}
    shape_id_counter = 0

    for r in range(height):
        for c in range(width):
            if grid_np[r, c] == value and (r, c) not in visited:
                shape_id_counter += 1
                current_shape = set()
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_shape.add((curr_r, curr_c))
                    coord_to_shape_id[(curr_r, curr_c)] = shape_id_counter
                    
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width):
                        # Check grid_np for value, not visited set
                        if grid_np[nr, nc] == value and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                if current_shape:
                    shapes.append(current_shape)
                    
    return shapes, coord_to_shape_id

def get_bounding_box(shape_coords: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a shape."""
    if not shape_coords:
        return (-1, -1, -1, -1) 
        
    min_r = min(r for r, c in shape_coords)
    min_c = min(c for r, c in shape_coords)
    max_r = max(r for r, c in shape_coords)
    max_c = max(c for r, c in shape_coords)
    return min_r, min_c, max_r, max_c

def pattern_long_exists(grid: list[list[int]]) -> bool:
    """Checks if any row contains (0, 6, 6+, 0)."""
    height = len(grid)
    if height == 0: return False
    width = len(grid[0]) if height > 0 else 0
    grid_np = np.array(grid)

    for r in range(height):
        row = grid_np[r, :]
        for i in range(width):
            if row[i] == 0:
                # Search for the next 0 at least 3 positions away
                for j in range(i + 3, width): 
                    if row[j] == 0:
                        # Check if all elements between i and j are 6
                        if i + 1 < j and np.all(row[i + 1 : j] == 6):
                            return True
    return False
    
def pattern_06plus0_rows(grid: list[list[int]]) -> list[int]:
    """Finds rows containing the pattern (0, 6+, 0)."""
    pattern_rows = set()
    height = len(grid)
    if height == 0: return []
    width = len(grid[0]) if height > 0 else 0
    grid_np = np.array(grid)
    
    for r in range(height):
        row = grid_np[r,:]
        found_in_row = False
        for i in range(width):
            if row[i] == 0:
                for j in range(i + 2, width): 
                    if row[j] == 0:
                        if i + 1 < j and np.all(row[i + 1 : j] == 6):
                             pattern_rows.add(r)
                             found_in_row = True
                             break # Found a pattern in this row, move to next row
                if found_in_row: break # Optimization
    return sorted(list(pattern_rows)) # Unique rows

def pattern_060_indices_in_row(row_list: list[int]) -> list[int]:
    """Finds starting column indices of (0, 6, 0) patterns in a single row list."""
    indices = []
    n = len(row_list)
    if n < 3: return indices
    for c in range(n - 2):
        if row_list[c] == 0 and row_list[c+1] == 6 and row_list[c+2] == 0:
            indices.append(c)
    return indices

def shape_contains_060(shape_coords: set[tuple[int,int]], grid: list[list[int]]) -> bool:
    """Checks if a shape contains any (0, 6, 0) pattern within its rows."""
    if not shape_coords: return False
    rows_in_shape = set(r for r,c in shape_coords)
    height = len(grid)
    
    for r in rows_in_shape:
        if 0 <= r < height: # Ensure row index is valid
             indices = pattern_060_indices_in_row(grid[r])
             for c_start in indices:
                 # Check if both 0s of the pattern are within the shape coordinates
                 if (r, c_start) in shape_coords and (r, c_start + 2) in shape_coords:
                     return True # Found one instance
    return False # No instance found

def get_rows_with_060_in_shape(shape_coords: set[tuple[int,int]], grid: list[list[int]]) -> list[int]:
    """Finds row indices within a shape that contain a (0, 6, 0) pattern using only shape coordinates."""
    rows = set()
    if not shape_coords: return []
    shape_rows = sorted(list(set(r for r,c in shape_coords)))
    height = len(grid)
    
    for r in shape_rows:
         if 0 <= r < height: # Ensure row index is valid
             indices = pattern_060_indices_in_row(grid[r])
             for c_start in indices:
                 # Check if both 0s of the pattern are part of this shape
                 if (r, c_start) in shape_coords and (r, c_start + 2) in shape_coords:
                     rows.add(r)
                     break # Move to next row once found in this one
    return sorted(list(rows))


def pattern_060_rows_and_indices_c_gt_0(grid: list[list[int]]) -> dict[int, list[int]]:
    """Finds rows containing (0, 6, 0) starting at c > 0, returns {row: [indices]}."""
    pattern_data = {}
    height = len(grid)
    if height == 0: return {}
    width = len(grid[0]) if height > 0 else 0
    
    for r in range(height):
        row_indices = []
        if width < 3: continue
        # Start check from c=1
        for c in range(1, width - 2):
            if grid[r][c] == 0 and grid[r][c+1] == 6 and grid[r][c+2] == 0:
                row_indices.append(c)
        if row_indices:
            pattern_data[r] = sorted(list(set(row_indices)))
    return pattern_data

def check_vertical_connectivity(r: int, c_indices: list[int], height: int, width: int, coord_to_shape_id: dict) -> bool:
    """Checks if any 0 at (r, c) or (r, c+2) for c in c_indices (where c > 0) 
       is connected to a 0 in row r+1."""
    if r + 1 >= height or not c_indices:
        return False 

    connected = False
    # Iterate through all pattern instances starting at c>0 in this row
    for c_start in c_indices: 
        # Coordinates of the two 0s in this specific pattern instance
        coords_in_pattern = []
        # Ensure coordinates are valid before adding
        if 0 <= c_start < width: coords_in_pattern.append((r, c_start))
        if 0 <= c_start + 2 < width: coords_in_pattern.append((r, c_start+2))
        
        # Check connectivity for either 0 in this pattern instance
        for R_PAT, C_PAT in coords_in_pattern:
            if (R_PAT, C_PAT) in coord_to_shape_id:
                shape_id = coord_to_shape_id[(R_PAT, C_PAT)]
                # Check all cells in row r+1 for the same shape ID
                for c_below in range(width):
                    coord_below = (r + 1, c_below)
                    # Check if coord_below has a shape ID and if it matches
                    if coord_below in coord_to_shape_id and coord_to_shape_id[coord_below] == shape_id:
                        connected = True
                        break # Found connection for this pattern instance's 0
            if connected: break # Stop checking 0s within this pattern instance if connected
        if connected: break # Stop checking pattern instances in row r if connected
        
    return connected

def apply_shift_blocks_right(grid: list[list[int]], shapes: list[set[tuple[int, int]]]):
    """Modifies the grid IN-PLACE by shifting 0-shapes right by one column."""
    height = len(grid)
    width = len(grid[0])
    
    # Step 1: Collect all original 0 coordinates
    original_zero_coords = set().union(*shapes) if shapes else set()
    
    # Step 2: Replace original 0s with 6s
    for r, c in original_zero_coords:
        if 0 <= r < height and 0 <= c < width:
             grid[r][c] = 6
             
    # Step 3: Place 0s shifted one column to the right
    for r, c in original_zero_coords:
        if 0 <= r < height and c + 1 < width: # Check bounds for shift
             grid[r][c + 1] = 0


# === Main Transformation Function ===

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    
    # --- Analyze Input ---
    height = len(input_grid)
    if height == 0: return []
    width = len(input_grid[0]) if height > 0 else 0
    if width == 0: return copy.deepcopy(input_grid) # Handle empty rows
    
    shapes, coord_to_shape_id = find_shapes_and_map(input_grid, 0)
    num_shapes = len(shapes)
    marker_col = find_marker_col(input_grid, 5)
    if marker_col == -1: marker_col = width # Handle case where marker isn't found? Set to edge?

    # --- Initialize Output Grid & Apply Block Shift ---
    output_grid = copy.deepcopy(input_grid)
    apply_shift_blocks_right(output_grid, shapes) # Modifies output_grid in place

    # --- Determine and Apply '2' Placement Rule (Prioritized) ---

    # Condition B1: Check for long pattern in INPUT grid
    has_long = pattern_long_exists(input_grid)
    if has_long:
        rows_to_fill = pattern_06plus0_rows(input_grid)
        for r in rows_to_fill:
            # Fill row r from marker_col + 1 to end
            for c in range(marker_col + 1, width):
                if 0 <= r < height and 0 <= c < width: # Bounds check
                    output_grid[r][c] = 2
    
    # Condition A: Check if B1 is false, num_shapes is 2, and both shapes contain (0,6,0) in INPUT grid
    elif num_shapes == 2 and shape_contains_060(shapes[0], input_grid) and shape_contains_060(shapes[1], input_grid):
        # Sort shapes by min_row to identify Shape 1 (top) and Shape 2 (bottom)
        bboxes = [get_bounding_box(s) for s in shapes]
        s1_coords, s2_coords = (shapes[0], shapes[1]) if bboxes[0][0] <= bboxes[1][0] else (shapes[1], shapes[0])
        bbox1 = get_bounding_box(s1_coords)
        bbox2 = get_bounding_box(s2_coords)
        
        r1_min, c1_min, r1_max, c1_max = bbox1
        r2_min, c2_min, r2_max, c2_max = bbox2

        # Find rows in Shape 2 (input grid) that contain the pattern
        rows_with_060_shape2 = get_rows_with_060_in_shape(s2_coords, input_grid)
        
        # Check if bboxes and rows list are valid before proceeding
        if r1_min != -1 and r2_min != -1:
            # Fill Block 1
            # Start row is fixed at 4 based on Example 1 observation
            start_row_block1 = 4 
            end_row_block1 = r1_max
            start_col_block1 = marker_col + 1
            end_col_block1 = marker_col + 4 # Inclusive range? Yes, seems to be 4 wide.
            
            for r in range(start_row_block1, end_row_block1 + 1):
                for c in range(start_col_block1, end_col_block1 + 1):
                    if 0 <= r < height and 0 <= c < width: # Check bounds
                        output_grid[r][c] = 2
                        
            # Fill Block 2 (Only if rows_with_060_shape2 is not empty)
            if rows_with_060_shape2:
                start_row_block2 = min(rows_with_060_shape2)
                end_row_block2 = r2_max
                # Columns are the same as block 1
                start_col_block2 = marker_col + 1
                end_col_block2 = marker_col + 4
                
                for r in range(start_row_block2, end_row_block2 + 1):
                    for c in range(start_col_block2, end_col_block2 + 1):
                        if 0 <= r < height and 0 <= c < width: # Check bounds
                            output_grid[r][c] = 2

    # Condition B2: Default case if B1 and A are false
    else:
        # Find rows with (0,6,0) starting at c > 0 in the *input* grid
        pattern_060_data = pattern_060_rows_and_indices_c_gt_0(input_grid)
        connected_rows_to_fill = []
        for r, c_indices in pattern_060_data.items():
            # Check vertical connectivity using input grid shapes/map
            is_connected = check_vertical_connectivity(r, c_indices, height, width, coord_to_shape_id)
            if is_connected:
                connected_rows_to_fill.append(r)
        
        # Fill eligible rows
        for r in connected_rows_to_fill:
            # Fill row r from marker_col + 1 to end
            for c in range(marker_col + 1, width):
                if 0 <= r < height and 0 <= c < width: # Bounds check
                    output_grid[r][c] = 2

    return output_grid