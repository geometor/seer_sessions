import numpy as np
import collections

"""
Transforms the input grid by identifying a unique 'source' cell (Y), a 'background' value (X), 
and an 'internal hole' region (H) of zeros. 

The process involves:
1. Identifying the source value Y (least frequent non-zero, adjacent to another non-zero value X) 
   and its location (r_y, c_y).
2. Identifying the background value X (the non-zero value adjacent to Y).
3. Finding the connected component of zeros (H) that meets two criteria:
    a. All its non-zero orthogonal neighbors have the background value X.
    b. No cell within the component touches the grid boundary.
4. Filling this internal hole region H with the source value Y.
5. Changing the value at the original source cell location (r_y, c_y) to the background value X.
"""

def _get_value_counts(grid):
    """Counts occurrences of non-zero values in the grid."""
    counts = collections.Counter(val for val in grid.flat if val != 0)
    return counts

def _find_source_and_background(grid):
    """
    Finds the source value (Y), its location (r_y, c_y), and the background value (X).
    Y is the least frequent non-zero value adjacent to another non-zero value X.
    """
    counts = _get_value_counts(grid)
    if not counts:
        return None, None, None # No non-zero values

    if len(counts) == 1:
         # Only one non-zero value, cannot determine distinct source/background
         # Based on task structure, this likely means no transformation is applicable.
         return None, None, None

    # Find least frequent non-zero value (potential source Y)
    sorted_counts = counts.most_common()
    source_y = sorted_counts[-1][0]
    
    # Find the location of this potential source value Y
    locations_y = np.argwhere(grid == source_y)
    if locations_y.size == 0:
        # Should not happen if counts were > 0
        return None, None, None 
        
    # Assume unique location for Y based on problem constraints
    source_r, source_c = tuple(locations_y[0])
    source_location = (source_r, source_c)

    # Find the adjacent background value X
    rows, cols = grid.shape
    background_x = None
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = source_r + dr, source_c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbor_val = grid[nr, nc]
            if neighbor_val != 0 and neighbor_val != source_y:
                # Found a non-zero neighbor different from Y. Assume this is X.
                # The problem constraints imply Y is adjacent to only one other value type X.
                background_x = neighbor_val
                break # Found X, no need to check other neighbors

    if background_x is None:
        # The least frequent value wasn't adjacent to any *other* non-zero value.
        # This scenario might not fit the problem pattern.
        return None, None, None

    return source_y, source_location, background_x


def _find_internal_hole_region(grid, background_value):
    """
    Finds the connected region of zeros that is bordered only by the background value 
    (or other zeros) AND does not touch the grid boundary. Uses BFS.
    Returns a list of (row, col) tuples for the hole cells, or [] if none found.
    """
    rows, cols = grid.shape
    visited_zeros = set() # Keep track of zeros visited across different potential components
    
    for r_start in range(rows):
        for c_start in range(cols):
            if grid[r_start, c_start] == 0 and (r_start, c_start) not in visited_zeros:
                # Start BFS for a new potential hole component
                component_coords = []
                q = collections.deque([(r_start, c_start)])
                component_visited_bfs = set([(r_start, c_start)]) # Zeros visited in *this* BFS
                
                touches_boundary = False
                invalid_neighbor_found = False

                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.append((curr_r, curr_c))
                    visited_zeros.add((curr_r, curr_c)) # Mark as globally visited

                    # Check boundary condition
                    if curr_r == 0 or curr_c == 0 or curr_r == rows - 1 or curr_c == cols - 1:
                        touches_boundary = True

                    # Check neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        if 0 <= nr < rows and 0 <= nc < cols:
                            neighbor_val = grid[nr, nc]
                            neighbor_coord = (nr, nc)

                            if neighbor_val == 0:
                                if neighbor_coord not in component_visited_bfs:
                                    component_visited_bfs.add(neighbor_coord)
                                    q.append(neighbor_coord)
                            elif neighbor_val != background_value:
                                # Found a non-zero neighbor that isn't the background value
                                invalid_neighbor_found = True
                        # else: neighbor is out of bounds (implicitly handled)

                # After BFS for this component is complete, check conditions
                if not touches_boundary and not invalid_neighbor_found:
                    # This component satisfies all conditions for the internal hole
                    return component_coords

    # If loop completes without finding a valid internal hole
    return []


def transform(input_grid_list):
    """
    Transforms the input grid based on identifying background, source, and an internal hole region.
    
    1. Identifies source (Y), its location (r_y, c_y), and background (X).
    2. Finds the internal hole region (H) - zeros bordered only by X and not touching the boundary.
    3. Fills H with Y.
    4. Changes the cell at (r_y, c_y) to X.
    """
    # Convert list of lists to numpy array for easier processing
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Step 1: Identify Source (Y), its location, and Background (X)
    source_y, source_location, background_x = _find_source_and_background(input_grid)

    if source_y is None or source_location is None or background_x is None:
        # Could not identify the necessary components based on the rules.
        # Return the original grid copy.
        print("Warning: Could not identify source/background values/location per rules.")
        return output_grid.tolist() 
    
    source_r, source_c = source_location

    # Step 2: Identify Internal Hole Region (H)
    hole_coordinates = _find_internal_hole_region(input_grid, background_x)

    # Step 3: Fill Hole (if found)
    if hole_coordinates:
        for r_h, c_h in hole_coordinates:
             # Check bounds just in case, though BFS should handle it
             if 0 <= r_h < rows and 0 <= c_h < cols:
                 output_grid[r_h, c_h] = source_y
            
    # Step 4: Update Source Location
    # Check bounds for the source location as well
    if 0 <= source_r < rows and 0 <= source_c < cols:
        output_grid[source_r, source_c] = background_x
            
    # Step 5: Finalize - Convert back to list of lists
    return output_grid.tolist()