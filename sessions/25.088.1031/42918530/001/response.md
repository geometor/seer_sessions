```python
import numpy as np

def find_neighbors(r, c, height, width):
    """Yields coordinates of 4 orthogonal neighbors within grid bounds."""
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            yield nr, nc

def transform(input_grid):
    """
    Identifies contiguous areas of white pixels (0) within the input grid.
    If a white area is completely enclosed by pixels of a single non-white color
    (i.e., the white area does not touch the grid border), then all pixels
    in that white area are changed to the color of the enclosing pixels.
    Other pixels remain unchanged.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.copy(input_grid)
    visited = np.zeros_like(input_grid, dtype=bool)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the pixel is white (0) and hasn't been visited yet
            if input_grid[r, c] == 0 and not visited[r, c]:
                
                # Start a search (BFS) to find the connected white area
                q = [(r, c)]
                current_area_pixels = []
                touches_border = False
                fill_color = -1 # Use -1 to indicate no fill color found yet
                
                # Mark the starting pixel as visited within this specific search context
                # We use a temporary visited set for the current BFS exploration,
                # but mark the global `visited` grid immediately.
                bfs_visited_local = set([(r,c)]) 
                visited[r, c] = True 

                while q:
                    curr_r, curr_c = q.pop(0)
                    current_area_pixels.append((curr_r, curr_c))

                    # Check if this pixel is on the grid border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        touches_border = True
                        # Optimization: If it touches the border, we know we won't fill,
                        # but we still need to explore the whole area to mark it visited.
                        # No need to break here, let it finish marking visited.

                    # Explore neighbors
                    for nr, nc in find_neighbors(curr_r, curr_c, height, width):
                        neighbor_color = input_grid[nr, nc]
                        
                        if neighbor_color == 0: # Neighbor is white
                            if (nr, nc) not in bfs_visited_local:
                                visited[nr, nc] = True # Mark globally visited
                                bfs_visited_local.add((nr, nc))
                                q.append((nr, nc))
                        else: # Neighbor is non-white
                            if fill_color == -1:
                                fill_color = neighbor_color
                            # Optional consistency check (uncomment if needed):
                            # elif fill_color != neighbor_color:
                            #     print(f"Warning: Inconsistent border colors found for area starting at ({r},{c}). Found {neighbor_color} and {fill_color}")
                            #     # Decide handling strategy: maybe invalidate fill_color?
                            #     # For this problem, seems shapes have uniform border color.
                            #     pass

                # After BFS for the area is complete:
                # If the area did NOT touch the border and a valid fill color was found
                if not touches_border and fill_color != -1:
                    # Fill the area in the output grid
                    for pr, pc in current_area_pixels:
                        output_grid[pr, pc] = fill_color
                
                # All pixels in current_area_pixels are now fully processed (either filled or left white)
                # The global `visited` grid ensures we don't start another BFS from within this area.

    return output_grid.tolist() # Return as list of lists
```