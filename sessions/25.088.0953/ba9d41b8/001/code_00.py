import numpy as np

"""
Identifies solid-colored rectangular blocks (excluding white) in the input grid.
For each block with dimensions at least 3x3, applies a checkerboard pattern
to its interior pixels (excluding the 1-pixel border). The checkerboard uses
the block's original color and white (0). The pattern starts with the original
color at the top-left corner of the interior. Pixels whose relative row and
column sum (within the interior, starting from 0,0) is odd are changed to white.
Background pixels and block borders remain unchanged.
"""

def find_solid_rectangles(grid):
    """
    Finds all solid, monochromatic rectangular blocks in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a block
              and contains 'color' (int) and 'bbox' (tuple: min_r, min_c, max_r, max_c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                
                # Find potential width
                max_c = c
                while max_c + 1 < cols and grid[r, max_c + 1] == color and not visited[r, max_c + 1]:
                    max_c += 1
                
                width = max_c - c + 1

                # Find potential height
                max_r = r
                is_solid_rectangle = True
                while max_r + 1 < rows:
                    # Check if the entire row segment matches the color and is unvisited
                    row_matches = True
                    for col_check in range(c, max_c + 1):
                        if grid[max_r + 1, col_check] != color or visited[max_r + 1, col_check]:
                            row_matches = False
                            break
                    if row_matches:
                        max_r += 1
                    else:
                        break
                
                height = max_r - r + 1
                
                # Verify if the entire area is the same color (redundant check if DFS/BFS not used, but safe)
                # and mark as visited
                is_block_solid = True
                pixels_to_visit = []
                for rr in range(r, max_r + 1):
                    for cc in range(c, max_c + 1):
                        if grid[rr, cc] != color or visited[rr,cc]:
                           # This handles cases where blocks might overlap or the initial scan found
                           # a non-rectangular shape embedding a rectangle. Reset and break if inconsistency found.
                           # Although the current logic aims to prevent this, double-checking ensures robustness.
                           # A more efficient approach relies solely on the row-by-row check during height determination.
                           is_block_solid = False
                           break
                        pixels_to_visit.append((rr,cc))
                    if not is_block_solid:
                        break

                if is_block_solid:
                     # Mark visited only if confirmed solid
                    for rr, cc in pixels_to_visit:
                         visited[rr, cc] = True
                     blocks.append({
                         'color': color,
                         'bbox': (r, c, max_r, max_c),
                         'height': height,
                         'width': width
                     })
                # else: # If not solid, mark only the starting pixel visited if needed, or handle as per algorithm
                     # The current logic marks the found rectangle pixels as visited even if it fails the final solid check.
                     # A better approach would be to only mark visited *after* confirming it's a solid rectangle we process.
                     # Let's refine: Mark visited only if it's a valid block we add.
                     # The outer loop `if not visited[r,c]` ensures we don't re-process.
                     # We just need to ensure the marking happens correctly *after* validation.

    return blocks


def transform(input_grid):
    """
    Applies a checkerboard pattern to the interior of solid rectangular blocks.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    
    # Find all solid rectangular blocks
    blocks = find_solid_rectangles(input_np)

    # Apply checkerboard pattern to the interior of each block
    for block in blocks:
        min_r, min_c, max_r, max_c = block['bbox']
        height = block['height']
        width = block['width']

        # Check if the block has an interior (needs height and width >= 3)
        if height >= 3 and width >= 3:
            # Iterate through the interior pixels
            # Interior starts at row min_r + 1, col min_c + 1
            # Interior ends at row max_r - 1, col max_c - 1
            for r in range(min_r + 1, max_r):
                for c in range(min_c + 1, max_c):
                    # Calculate relative coordinates within the interior
                    # Top-left of interior is (min_r + 1, min_c + 1)
                    rel_r = r - (min_r + 1)
                    rel_c = c - (min_c + 1)

                    # Check if the sum of relative coordinates is odd
                    if (rel_r + rel_c) % 2 != 0:
                        # Set pixel to white (0)
                        output_grid[r, c] = 0
                        
    # Convert back to list of lists for the expected output format
    return output_grid.tolist()