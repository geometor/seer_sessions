"""
Transforms a 3x3 input grid containing 0s and 2s.
Outputs 7 if and only if:
1. There exists at least one pair of '2's that are 4-way adjacent (horizontally or vertically).
2. All '2's in the grid form a single connected component using 8-way adjacency (including diagonals).
3. There is more than one '2' present in the grid.
Otherwise, outputs 1.
"""

from collections import deque

def _find_twos(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Finds the coordinates of all cells containing '2'."""
    twos_coords = []
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                twos_coords.append((r, c))
    return twos_coords

def _check_4way_adjacency(grid: list[list[int]], twos_coords: list[tuple[int, int]]) -> bool:
    """Checks if any two '2's are 4-way adjacent (up, down, left, right)."""
    rows = len(grid)
    cols = len(grid[0])
    twos_set = set(twos_coords) # Faster lookups

    for r, c in twos_coords:
        # Define 4-way neighbors
        neighbors = [
            (r - 1, c),  # Up
            (r + 1, c),  # Down
            (r, c - 1),  # Left
            (r, c + 1)   # Right
        ]

        for nr, nc in neighbors:
            # Check if neighbor is within bounds and is also a '2'
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in twos_set:
                return True # Found a 4-way adjacent pair

    return False # No 4-way adjacent pairs found

def _check_8way_connectivity(grid: list[list[int]], twos_coords: list[tuple[int, int]]) -> bool:
    """
    Checks if all '2's form a single connected component using 8-way adjacency.
    Assumes len(twos_coords) > 1.
    """
    rows = len(grid)
    cols = len(grid[0])
    total_twos = len(twos_coords)
    
    # Should not be called if total_twos <= 1, but adding safety check
    if total_twos <= 1:
        return True # A single node is considered connected by convention, though the main func handles this

    start_node = twos_coords[0]
    q = deque([start_node])
    visited = {start_node}
    connected_count = 0
    all_twos_set = set(twos_coords) # For efficient checking

    while q:
        r, c = q.popleft()
        connected_count += 1

        # Define 8 neighbors (horizontal, vertical, diagonal)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: # Skip self
                    continue
                
                nr, nc = r + dr, c + dc
                neighbor_coord = (nr, nc)

                # Check if neighbor is within bounds, is a '2', and not visited
                if 0 <= nr < rows and 0 <= nc < cols and \
                   neighbor_coord in all_twos_set and \
                   neighbor_coord not in visited:
                    
                    visited.add(neighbor_coord)
                    q.append(neighbor_coord)
                            
    # If the number of visited nodes equals the total number of '2's, they are all connected
    return connected_count == total_twos


def transform(input_grid: list[list[int]]) -> int:
    """
    Applies the transformation rule based on 4-way adjacency and 8-way connectivity of '2's.
    """
    
    # 1. Identify all cells containing the value '2'.
    twos_coords = _find_twos(input_grid)
    
    # 2. Count the total number of cells containing '2'.
    total_twos = len(twos_coords)

    # 3. Handle edge cases: 0 or 1 '2's always result in output 1.
    if total_twos <= 1:
        return 1

    # 4. Check for 4-way adjacency.
    has_4way_adj = _check_4way_adjacency(input_grid, twos_coords)

    # 5. Check for 8-way connectivity.
    is_single_component_8way = _check_8way_connectivity(input_grid, twos_coords)

    # 6. Determine Output based on both conditions.
    #    Output 7 only if both conditions are true.
    if has_4way_adj and is_single_component_8way:
        return 7
    else:
        # Output 1 if either condition is false
        return 1