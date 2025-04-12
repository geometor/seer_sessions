import copy
import numpy as np
from collections import deque

"""
Transforms a 2D grid based on the number of distinct contiguous shapes formed by 
the value 0 in the input grid. The grid also contains a background value (6) 
and a single vertical marker line (5).

Transformation Rules:

Case A: Exactly 2 Shapes of 0s Found
    1. Replace all input 0s with 6s in the output grid. Preserve other values.
    2. Find the two shapes (Shape 1 and Shape 2) and their bounding boxes (Bbox).
       Shape 1 is the one with the smaller minimum row index (r_min).
       Bbox = (r_min, c_min, r_max, c_max).
    3. Calculate the coordinates for a single output rectangle of 2s:
        - rect_height = (Bbox2.r_max - Bbox2.r_min + 1)
        - top = Bbox1.r_max - rect_height + 1
        - bottom = Bbox1.r_max
        - left = Bbox2.r_min + 1
        - right = Bbox2.r_max + 1
    4. Fill this calculated rectangle in the output grid with the value 2.

Case B: Number of 0-Shapes is Not 2
    1. Perform a block shift: Replace original 0 locations with 6, then draw the 
       0s shifted one column to the right in the output grid.
    2. Find the marker column index `marker_col`.
    3. Check if any row in the *input* grid contains a "long" pattern 
       (0, 6, 6+, 0) - i.e., a 0, followed by two or more 6s, followed by a 0.
    
    Subcase B1 (Long pattern exists):
        - Find all rows `r` in the *input* grid that contain *any* (0, 6+, 0) pattern.
        - For each such row `r`: Fill the output grid row `r` from column 
          `marker_col + 1` to `width - 1` with 2s.

    Subcase B2 (Only short (0, 6, 0) patterns exist):
        - Find all rows `r` in the *input* grid that contain the (0, 6, 0) pattern 
          starting at column `c > 0`.
        - For each such row `r`: Check if any 0 involved in such a pattern instance 
          belongs to the same shape as any 0 in row `r+1`.
        - If vertically connected: Fill the output grid row `r` from column 
          `marker_col + 1` to `width - 1` with 2s.
"""

# === Helper Functions ===

def find_marker_col(grid: list[list[int]], marker_value: int = 5) -> int:
    """Finds the column index of the first occurrence of the marker value."""
    height = len(grid)
    if height == 0: return -1
    width = len(grid[0])
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
    width = len(grid[0])
    
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
    width = len(grid[0])
    grid_np = np.array(grid)

    for r in range(height):
        row = grid_np[r, :]
        for i in range(width):
            if row[i] == 0:
                # Search for the next 0 at least 3 positions away
                for j in range(i + 3, width): 
                    if row[j] == 0:
                        # Check if all elements between i and j are 6
                        if np.all(row[i + 1 : j] == 6):
                            return True
    return False
    
def pattern_06plus0_rows(grid: list[list[int]]) -> list[int]:
    """Finds rows containing the pattern (0, 6+, 0)."""
    pattern_rows = []
    height = len(grid)
    if height == 0: return []
    width = len(grid[0])
    grid_np = np.array(grid)
    
    for r in range(height):
        row = grid_np[r,:]
        found_in_row = False
        for i in range(width):
            if row[i] == 0:
                for j in range(i + 2, width): 
                    if row[j] == 0:
                        if i + 1 < j and np.all(row[i + 1 : j] == 6):
                             pattern_rows.append(r)
                             found_in_row = True
                             break # Found a pattern in this row, move to next row
                if found_in_row: break # Optimization
    return sorted(list(set(pattern_rows))) # Unique rows

def pattern_060_rows_and_indices_c_gt_0(grid: list[list[int]]) -> dict[int, list[int]]:
    """Finds rows containing (0, 6, 0) starting at c > 0, returns {row: [indices]}."""
    pattern_data = {}
    height = len(grid)
    if height == 0: return {}
    width = len(grid[0])
    
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
                    if coord_below in coord_to_shape_id and coord_to_shape_id[coord_below] == shape_id:
                        connected = True
                        break # Found connection for this pattern instance's 0
            if connected: break # Stop checking 0s within this pattern instance if connected
        if connected: break # Stop checking pattern instances in row r if connected
        
    return connected

def shift_blocks_right(grid: list[list[int]], shapes: list[set[tuple[int, int]]]):
    """Modifies the grid by shifting 0-shapes right by one column."""
    height = len(grid)
    width = len(grid[0])
    
    # Step 1: Collect all original 0 coordinates
    original_zero_coords = set().union(*shapes)
    
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
    width = len(input_grid[0])
    
    shapes, coord_to_shape_id = find_shapes_and_map(input_grid, 0)
    num_shapes = len(shapes)
    marker_col = find_marker_col(input_grid, 5)
    
    # --- Initialize Output Grid ---
    output_grid = copy.deepcopy(input_grid)

    # --- Case A: Exactly 2 Shapes ---
    if num_shapes == 2:
        # Replace all original 0s with 6
        for r in range(height):
            for c in range(width):
                if output_grid[r][c] == 0:
                    output_grid[r][c] = 6
                    
        # Calculate bounding boxes
        bboxes = [get_bounding_box(s) for s in shapes]
        
        # Sort shapes by min_row to identify Shape 1 and Shape 2
        if bboxes[0][0] <= bboxes[1][0]:
            bbox1 = bboxes[0] # r1_min, c1_min, r1_max, c1_max
            bbox2 = bboxes[1] # r2_min, c2_min, r2_max, c2_max
        else:
            bbox1 = bboxes[1]
            bbox2 = bboxes[0]
            
        r1_min, c1_min, r1_max, c1_max = bbox1
        r2_min, c2_min, r2_max, c2_max = bbox2

        # Check if bboxes are valid before calculating dims
        if r1_min != -1 and r2_min != -1:
            # Calculate output rectangle coordinates based on refined rule
            rect_height = (r2_max - r2_min + 1)
            top_row = r1_max - rect_height + 1
            bottom_row = r1_max
            left_col = r2_min + 1
            right_col = r2_max + 1
            
            # Fill the output rectangle with 2s
            for r in range(top_row, bottom_row + 1):
                for c in range(left_col, right_col + 1):
                    if 0 <= r < height and 0 <= c < width: # Check bounds
                        output_grid[r][c] = 2

    # --- Case B: Not Exactly 2 Shapes ---
    else:
        # Perform the block shift (modifies output_grid)
        shift_blocks_right(output_grid, shapes)
        
        # Determine subcase: long pattern exists in *input*?
        has_long = pattern_long_exists(input_grid)

        if has_long:
            # Subcase B1: Long pattern exists
            rows_to_fill = pattern_06plus0_rows(input_grid)
            for r in rows_to_fill:
                # Fill row r from marker_col + 1 to end
                for c in range(marker_col + 1, width):
                     if 0 <= r < height and 0 <= c < width: # Bounds check (r,c already in bounds)
                         output_grid[r][c] = 2
        else:
            # Subcase B2: Only short (0, 6, 0) patterns potentially relevant
            # Find rows with (0,6,0) starting at c > 0 in the *input* grid
            pattern_060_data = pattern_060_rows_and_indices_c_gt_0(input_grid)
            rows_to_fill = []
            for r, c_indices in pattern_060_data.items():
                # Check vertical connectivity for this row using input grid shapes/map
                is_connected = check_vertical_connectivity(r, c_indices, height, width, coord_to_shape_id)
                if is_connected:
                    rows_to_fill.append(r)
            
            # Fill eligible rows
            for r in rows_to_fill:
                 # Fill row r from marker_col + 1 to end
                for c in range(marker_col + 1, width):
                     if 0 <= r < height and 0 <= c < width: # Bounds check
                         output_grid[r][c] = 2

    return output_grid