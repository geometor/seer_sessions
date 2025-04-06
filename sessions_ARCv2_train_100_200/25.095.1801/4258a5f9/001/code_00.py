import copy

"""
Transforms an input grid based on the following rules:
1. Initialize an output grid of the same dimensions as the input, filled with zeros.
2. Iterate through each cell (r, c) of the input grid.
3. If the input cell value is 5, set the corresponding output cell value to 5.
4. If the input cell value is 0, check its 8 neighbors (Moore neighborhood) in the *input* grid.
5. If any neighbor in the input grid has a value of 5, set the corresponding output cell value to 1.
6. Otherwise, the output cell remains 0.
"""

def _is_valid(r: int, c: int, rows: int, cols: int) -> bool:
    """Checks if the coordinates (r, c) are within the grid boundaries."""
    return 0 <= r < rows and 0 <= c < cols

def _has_neighbor_5(r: int, c: int, input_grid: list[list[int]], rows: int, cols: int) -> bool:
    """Checks if any Moore neighbor of cell (r, c) in the input_grid has the value 5."""
    # Define the 8 neighbor offsets (dx, dy) for Moore neighborhood
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]
    
    for dr, dc in neighbor_offsets:
        nr, nc = r + dr, c + dc
        # Check if the neighbor coordinates are valid
        if _is_valid(nr, nc, rows, cols):
            # Check if the neighbor cell in the input grid is 5
            if input_grid[nr][nc] == 5:
                return True
    return False

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    Cells with 5 remain 5. Cells with 0 become 1 if any neighbor in the input
    grid was 5, otherwise they remain 0.
    """
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid with zeros
    # Using deepcopy might be slightly less efficient than list comprehension for zeros,
    # but ensures a completely separate structure if we were copying non-zero defaults.
    # For zeros, list comprehension is cleaner:
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            input_value = input_grid[r][c]
            
            # Rule 1: Preserve Source Markers (5s)
            if input_value == 5:
                output_grid[r][c] = 5
            # Rule 2: Generate Neighbor Markers (1s) for original 0s
            elif input_value == 0:
                # Check if any neighbor in the *input* grid is 5
                if _has_neighbor_5(r, c, input_grid, rows, cols):
                    output_grid[r][c] = 1
            # Otherwise, the cell remains 0 (already initialized)

    return output_grid