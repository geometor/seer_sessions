```python
import copy
import numpy as np
from collections import deque

"""
Transforms a 2D grid based on the number of distinct contiguous shapes formed by 
the value 0 in the input grid. The grid also contains a background value (6) 
and a single vertical marker line (5).

Transformation Rules:

Case A: Exactly 2 Shapes of 0s Found (e.g., train_1)
    1. Replace all input 0s with 6s in the output grid. Preserve other values.
    2. Find the two shapes (Shape 1 and Shape 2) and their bounding boxes (Bbox).
       Shape 1 is the one with the smaller minimum row index (r_min).
       Bbox = (r_min, c_min, r_max, c_max).
    3. Calculate the coordinates for a single output rectangle of 2s:
        - height = (Bbox2.r_max - Bbox2.r_min + 1)
        - top = Bbox1.r_max - height + 1
        - bottom = Bbox1.r_max
        - left = Bbox2.r_min + 1
        - right = Bbox2.r_max + 1
    4. Fill this calculated rectangle in the output grid with the value 2.

Case B: Number of 0-Shapes is Not 2 (e.g., train_2, train_3)
    1. Create the base output grid by replacing all input 0s with 6s. Preserve others.
    2. Find the original coordinates of all input 0s.
    3. Shift these 0s one column to the right, placing 0s in the output grid 
       at the new coordinates (r, c+1), checking bounds.
    4. Find the marker column index `marker_col`.
    5. Check if any row in the *input* grid contains a "long" pattern 
       (0, 6, 6+, 0) - i.e., a 0, followed by two or more 6s, followed by a 0.
    
    Subcase B1 (Long pattern exists - e.g., train_3):
        - Find all rows `r` in the *input* grid that contain *any* (0, 6+, 0) pattern.
        - For each such row `r`:
            - Calculate columns: `left = marker_col + 1`, `right = width - 1`.
            - Fill the output grid row `r` from `left` to `right` with 2s.

    Subcase B2 (Only short (0, 6, 0) patterns exist - e.g., train_2):
        - Find a map of input 0 coordinates to their shape IDs.
        - Find all rows `r` in the *input* grid that contain the (0, 6, 0) pattern.
        - For each such row `r`:
            - Check if any 0 involved in a (0, 6, 0) pattern instance in row `r` 
              belongs to the same shape as any 0 in row `r+1`.
            - If vertically connected:
                - Calculate columns: `left = marker_col + 2`, `right = marker_col + 4`.
                - Fill the output grid in row `r` from `left` to `right` with 2s.
                - Fill the output grid in row `r+1` from `left` to `right` with 2s 
                  (checking bounds).
"""

# --- Helper Functions ---

def find_marker_col(grid: list[list[int]], marker_value: int = 5) -> int:
    """Finds the column index of the first occurrence of the marker value."""
    height = len(grid)
    if height == 0: return -1
    width = len(grid[0])
    for r in range(height):
        for c in range(width):
            if grid[r][c] == marker_value:
                return c
    return -1 # Should not happen based on problem description

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
    
    grid_np = np.array(grid) # Use numpy for efficient access if large
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

def find_all_coords(grid: list[list[int]], value: int) -> list[tuple[int, int]]:
    """Finds coordinates of all cells with a specific value."""
    coords = []
    height = len(grid)
    if height == 0: return []
    width = len(grid[0])
    for r in range(height):
        for c in range(width):
            if grid[r][c] == value:
                coords.append((r, c))
    return coords

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
                # Search for the next 0 at least 3 positions away (needs >=2 sixes)
                for j in range(i + 3, width): 
                    if row[j] == 0:
                        # Check if all elements between i and j are 6
                        if np.all(row[i + 1 : j] == 6):
                            return True
                        # Optimization: If non-6 found, no need to check further j for this i? Maybe...
                        # if not np.all(row[i + 1 : j] == 6): break # Probably not safe
    return False

def pattern_060_rows_and_indices(grid: list[list[int]]) -> dict[int, list[int]]:
    """Finds rows containing (0, 6, 0) and the starting column indices."""
    pattern_data = {}
    height = len(grid)
    if height == 0: return {}
    width = len(grid[0])
    
    for r in range(height):
        row_indices = []
        if width < 3: continue
        for c in range(width - 2):
            if grid[r][c] == 0 and grid[r][c+1] == 6 and grid[r][c+2] == 0:
                row_indices.append(c)
        if row_indices:
            pattern_data[r] = row_indices
    return pattern_data

def check_vertical_connectivity(r: int, c_indices: list[int], height: int, width: int, coord_to_shape_id: dict) -> bool:
    """Checks if any 0 at (r, c) or (r, c+2) for c in c_indices is connected to a 0 in row r+1."""
    if r + 1 >= height:
        return False # Cannot connect below if it's the last row

    connected = False
    for c_start in c_indices:
        # Coordinates of the two 0s in the pattern (r, c_start) and (r, c_start+2)
        coords_in_pattern = []
        if 0 <= c_start < width: coords_in_pattern.append((r, c_start))
        if 0 <= c_start + 2 < width: coords_in_pattern.append((r, c_start+2))
        
        for R_PAT, C_PAT in coords_in_pattern:
            if (R_PAT, C_PAT) in coord_to_shape_id:
                shape_id = coord_to_shape_id[(R_PAT, C_PAT)]
                # Check all cells in row r+1 for the same shape ID
                for c_below in range(width):
                    coord_below = (r + 1, c_below)
                    if coord_below in coord_to_shape_id and coord_to_shape_id[coord_below] == shape_id:
                        connected = True
                        break # Found connection for this pattern instance
            if connected: break # Found connection for this pattern instance
        if connected: break # Found connection for this row
    return connected

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules based on the number of 0-shapes.
    """
    height = len(input_grid)
    if height == 0: return []
    width = len(input_grid[0])
    
    # --- Analyze Input ---
    shapes, coord_to_shape_id = find_shapes_and_map(input_grid, 0)
    num_shapes = len(shapes)
    marker_col = find_marker_col(input_grid, 5)
    original_zero_coords = find_all_coords(input_grid, 0)

    # --- Initialize Output Grid (common step: replace 0s with 6s) ---
    output_grid = copy.deepcopy(input_grid)
    for r, c in original_zero_coords:
        output_grid[r][c] = 6

    # --- Case A: Exactly 2 Shapes ---
    if num_shapes == 2:
        # Calculate bounding boxes
        bboxes = [get_bounding_box(s) for s in shapes]
        
        # Sort shapes by min_row to identify Shape 1 and Shape 2
        # Shape 1 has the smaller min_row
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
            h = (r2_max - r2_min + 1)
            top = r1_max - h + 1
            bottom = r1_max
            left = r2_min + 1
            right = r2_max + 1
            
            # Fill the output rectangle with 2s
            for r in range(top, bottom + 1):
                for c in range(left, right + 1):
                    if 0 <= r < height and 0 <= c < width: # Check bounds
                        output_grid[r][c] = 2
                        
    # --- Case B: Not Exactly 2 Shapes ---
    else:
        # Shift original 0s right by 1 (modifies output_grid further)
        for r, c in original_zero_coords:
            if c + 1 < width: # Check bounds for shift
                 output_grid[r][c + 1] = 0

        # Determine subcase: long pattern exists?
        has_long = pattern_long_exists(input_grid)

        if has_long:
            # Subcase B1: Long pattern exists
            rows_with_pattern = pattern_06plus0_rows(input_grid)
            for r in rows_with_pattern:
                left = marker_col + 1
                right = width - 1 # Inclusive
                for c in range(left, right + 1):
                     if 0 <= r < height and 0 <= c < width: # Check bounds
                         output_grid[r][c] = 2
        else:
            # Subcase B2: Only short (0, 6, 0) patterns
            pattern_060_data = pattern_060_rows_and_indices(input_grid)
            for r, c_indices in pattern_060_data.items():
                # Check vertical connectivity for this row
                is_connected = check_vertical_connectivity(r, c_indices, height, width, coord_to_shape_id)
                
                if is_connected:
                    left = marker_col + 2
                    right = marker_col + 4 # Inclusive
                    
                    # Fill row r
                    for c in range(left, right + 1):
                        if 0 <= r < height and 0 <= c < width:
                            output_grid[r][c] = 2
                            
                    # Fill row r+1
                    r_below = r + 1
                    if r_below < height:
                         for c in range(left, right + 1):
                            if 0 <= c < width: # Row bound already checked
                                output_grid[r_below][c] = 2

    return output_grid
```