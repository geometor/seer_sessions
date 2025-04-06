import collections

"""
Transforms a 2D grid containing blocks of 5s against a background of 0s.
Each block of 5s is replaced by a pattern of 1s, 2s, and 4s based on cell position:
- 1 for corners of the block.
- 4 for edges of the block (excluding corners).
- 2 for the interior of the block.
- 0s remain unchanged.
The transformation identifies each distinct rectangular block of 5s and applies the pattern locally.
"""

def find_blocks(grid: list[list[int]]) -> list[tuple[int, int, int, int]]:
    """
    Identifies rectangular blocks of 5s in the input grid.

    Args:
        grid: The input 2D list of integers.

    Returns:
        A list of tuples, where each tuple represents a block's boundaries
        as (min_row, max_row, min_col, max_col).
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    blocks = []

    for r in range(rows):
        for c in range(cols):
            # If we find a '5' that hasn't been visited, start a search for its block
            if grid[r][c] == 5 and (r, c) not in visited:
                current_block_cells = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Use Breadth-First Search (BFS) to find all connected '5's
                while q:
                    curr_r, curr_c = q.popleft()
                    current_block_cells.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds, if it's a '5', and if not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr][nc] == 5 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                # Assuming blocks are perfectly rectangular as per examples,
                # store the calculated boundaries.
                blocks.append((min_r, max_r, min_c, max_c))
                
                # Optimization: Mark all cells within the determined boundary as visited
                # This handles cases where BFS might finish before exploring all cells 
                # *if* we didn't assume perfect rectangles, but is good practice anyway.
                # However, the initial BFS *should* find all connected cells. Let's ensure
                # the visited set correctly covers the block found by BFS.
                # The BFS naturally handles connectivity. No extra marking needed here if
                # the blocks are truly contiguous '5's.

    return blocks


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: The 2D list representing the input grid.

    Returns:
        A 2D list representing the transformed output grid.
    """
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Find all the rectangular blocks of 5s
    blocks = find_blocks(input_grid)

    # Process each identified block
    for min_r, max_r, min_c, max_c in blocks:
        # Iterate through each cell within the block's boundaries
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                 # Ensure we only modify cells that were originally '5'
                 # (This check might be redundant if find_blocks is perfect,
                 # but adds robustness)
                if input_grid[r][c] == 5:
                    # Check if the cell is a corner
                    is_corner = (r == min_r or r == max_r) and \
                                (c == min_c or c == max_c)
                    # Check if the cell is on an edge
                    is_edge = (r == min_r or r == max_r or
                               c == min_c or c == max_c)

                    # Assign the output value based on position
                    if is_corner:
                        output_grid[r][c] = 1
                    elif is_edge: # It's an edge but not a corner
                        output_grid[r][c] = 4
                    else: # It must be an interior cell
                        output_grid[r][c] = 2

    # Background zeros are already in place from initialization

    return output_grid