import collections

"""
Identifies all connected components of '1's in the input 9x9 grid. 
For each component, checks if it forms a perfect 2x2 block. 
Counts the number of such 2x2 blocks.
Generates an output list containing '1' for each identified 2x2 block, 
padded with '0's at the end to ensure a total length of 5.
"""

def _is_valid(r, c, rows, cols):
    """Checks if the coordinates are within the grid boundaries."""
    return 0 <= r < rows and 0 <= c < cols

def _find_connected_component(start_r, start_c, grid, visited):
    """
    Finds a connected component of '1's using Breadth-First Search (BFS).
    Returns the list of coordinates in the component.
    """
    rows = len(grid)
    cols = len(grid[0])
    component_coords = []
    queue = collections.deque([(start_r, start_c)])
    visited[start_r][start_c] = True

    while queue:
        r, c = queue.popleft()
        component_coords.append((r, c))

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if _is_valid(nr, nc, rows, cols) and \
               grid[nr][nc] == 1 and \
               not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc))
                
    return component_coords

def _is_2x2_block(component_coords):
    """
    Checks if a component with exactly 4 cells forms a 2x2 block.
    """
    if len(component_coords) != 4:
        return False

    # Find the min/max row and column
    min_r = min(r for r, c in component_coords)
    max_r = max(r for r, c in component_coords)
    min_c = min(c for r, c in component_coords)
    max_c = max(c for r, c in component_coords)

    # Check if the dimensions correspond to a 2x2 block
    return (max_r - min_r == 1) and (max_c - min_c == 1)

def transform(input_grid: list[list[int]]) -> list[int]:
    """
    Transforms the input grid by finding 2x2 blocks of '1's and representing
    their count in a fixed-length binary list.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Keep track of visited cells to avoid processing the same component multiple times
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    
    output_list = []
    
    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # If the cell contains '1' and hasn't been visited yet
            if input_grid[r][c] == 1 and not visited[r][c]:
                # Find the entire connected component starting from this cell
                component = _find_connected_component(r, c, input_grid, visited)
                
                # Check if this component is a 2x2 block
                if _is_2x2_block(component):
                    # If it is, add a '1' to the output list
                    output_list.append(1)

    # Pad the output list with '0's until it reaches the target length of 5
    output_len = 5
    while len(output_list) < output_len:
        output_list.append(0)
        
    # Ensure the output list does not exceed the target length (though unlikely with this logic)
    output_list = output_list[:output_len] 

    return output_list