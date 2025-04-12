```python
"""
Transforms an input grid containing white (0) and gray (5) pixels into an output grid containing white (0), gray (5), and green (3) pixels.

The transformation rule is applied locally to each gray pixel based on its diagonal neighbors (NW, NE, SW, SE):

1.  **White pixels (0)** remain unchanged.
2.  **Gray pixels (5)** are evaluated as follows:
    a.  **V-Top:** If both the South-West (SW) and South-East (SE) diagonal neighbors are gray (5), the pixel remains gray (5).
    b.  **Isolated:** If the pixel has no gray diagonal neighbors:
        - If it's on the bottom row of the grid, it remains gray (5).
        - Otherwise (not on the bottom row), it changes to green (3).
    c.  **Anchor-1:** If the pixel has exactly one gray diagonal neighbor, and it's either:
        - On the top row with a gray SW or SE neighbor, OR
        - On the bottom row with a gray NW or NE neighbor,
        then the pixel remains gray (5).
    d.  **NonAnchor-1:** If the pixel has exactly one gray diagonal neighbor but doesn't meet the Anchor-1 criteria, it changes to green (3).
    e.  **Diag-2:** If the pixel has exactly two gray diagonal neighbors, but it's *not* a V-Top configuration (i.e., not SW and SE both gray), it changes to green (3).
    f.  **Diag-3+:** If the pixel has three or more gray diagonal neighbors, it remains gray (5) (based on assumption as this case wasn't explicitly needed for examples).
3.  If none of the above conditions for changing a gray pixel are met, it defaults to remaining gray (though the logic covers all cases for num_diag 0, 1, 2, 3+).
"""

import copy

def get_diagonal_neighbors(grid: list[list[int]], r: int, c: int) -> tuple[dict[str, bool], int]:
    """
    Checks the diagonal neighbors of a pixel and counts how many are gray.

    Args:
        grid: The input grid.
        r: The row index of the pixel.
        c: The column index of the pixel.

    Returns:
        A tuple containing:
        - A dictionary indicating whether each diagonal neighbor (nw, ne, sw, se) is gray (True) or not (False/missing).
        - An integer count of gray diagonal neighbors.
    """
    height = len(grid)
    width = len(grid[0])
    neighbors = {"nw": False, "ne": False, "sw": False, "se": False}
    gray_count = 0
    
    coords = {
        "nw": (r - 1, c - 1),
        "ne": (r - 1, c + 1),
        "sw": (r + 1, c - 1),
        "se": (r + 1, c + 1),
    }

    for direction, (nr, nc) in coords.items():
        if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] == 5:
            neighbors[direction] = True
            gray_count += 1
            
    return neighbors, gray_count

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: The input grid as a list of lists of integers.

    Returns:
        The transformed output grid as a list of lists of integers.
    """
    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid.
    # White pixels remain 0, gray pixels start as 5 and might change to 3.
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each cell (pixel) of the input grid
    for r in range(height):
        for c in range(width):
            # Only process gray pixels
            if input_grid[r][c] == 5:
                # Get diagonal neighbor information
                neighbors, num_diag = get_diagonal_neighbors(input_grid, r, c)
                
                # Check row position
                is_top = (r == 0)
                is_bottom = (r == height - 1)
                
                # --- Apply transformation rules ---
                
                # Default is to keep gray (5), only change to green (3) if a condition is met.
                output_color = 5 

                # Rule a: V-Top (SW and SE are gray) - Stays gray (handled by default)
                is_v_top = neighbors["sw"] and neighbors["se"]
                if is_v_top:
                    output_color = 5 # Explicitly keep gray
                
                # Rule b: Isolated (0 diagonal gray neighbors)
                elif num_diag == 0:
                    if is_bottom:
                        output_color = 5 # Keep gray if on bottom row
                    else:
                        output_color = 3 # Change to green if not on bottom row
                        
                # Rule c: Anchor-1 (1 diagonal gray neighbor at specific edges)
                elif num_diag == 1:
                    is_anchor1 = (is_top and (neighbors["sw"] or neighbors["se"])) or \
                                 (is_bottom and (neighbors["nw"] or neighbors["ne"]))
                    if is_anchor1:
                        output_color = 5 # Keep gray if anchor
                    else:
                        # Rule d: NonAnchor-1 (1 diagonal gray neighbor, not anchor)
                        output_color = 3 # Change to green if not anchor

                # Rule e: Diag-2 (2 diagonal gray neighbors, not V-Top)
                elif num_diag == 2 and not is_v_top:
                    output_color = 3 # Change to green

                # Rule f: Diag-3+ (3 or more diagonal gray neighbors) - Stays gray (handled by default)
                elif num_diag >= 3:
                     output_color = 5 # Explicitly keep gray
                
                # Update the output grid
                output_grid[r][c] = output_color

    return output_grid
```