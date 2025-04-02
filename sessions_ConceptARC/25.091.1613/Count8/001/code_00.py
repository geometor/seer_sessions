import numpy as np
from collections import deque

"""
1. Identify the largest contiguous block of non-white pixels in the input grid. Determine the color of this block (the 'dominant color').
2. Iterate through all pixel locations occupied by this dominant color block.
3. Count the number of pixels within these locations that have a color *different* from the dominant color. Let this count be `N`.
4. Construct an output grid with dimensions `N` rows and 1 column.
5. Fill every cell of the output grid with the color red (2).
"""

def find_connected_components(grid, ignore_color=0):
    """Finds all connected components of colors other than ignore_color."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != ignore_color and not visited[r, c]:
                component_color = grid[r, c]
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                is_uniform = True

                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] != ignore_color:
                             # Check if the neighbor has the *same* color to define the component
                             if grid[nr, nc] == component_color:
                                 visited[nr, nc] = True
                                 q.append((nr, nc))
                             else:
                                 # If a neighbor belongs to the potential object but has a different color,
                                 # the component based on initial color isn't strictly uniform.
                                 # However, for finding the *largest* object, we usually base it on
                                 # connectivity regardless of minor color variations within.
                                 # Let's refine this based on the task description "largest contiguous block".
                                 # The description implies the block has *a* dominant color.
                                 # Let's assume the component is defined by connectivity of *any* non-ignored color,
                                 # and we determine the dominant color *after* finding the component.
                                 pass # Let the main logic handle color analysis later

                # Refined approach: A component is connected non-background pixels. Find the largest one.
                # Restart BFS to ensure we capture the *entire* connected non-background region
                # if the initial pixel wasn't representative or if impurities break strict color uniformity.

                q = deque([(r, c)])
                visited_component = set([(r,c)])
                full_component_pixels = []

                while q:
                     row, col = q.popleft()
                     full_component_pixels.append((row, col))

                     for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nr, nc = row + dr, col + dc
                         if 0 <= nr < rows and 0 <= nc < cols and \
                            grid[nr, nc] != ignore_color and (nr, nc) not in visited_component:
                              visited_component.add((nr, nc))
                              visited[nr, nc] = True # Mark globally visited too
                              q.append((nr, nc))

                if full_component_pixels:
                    components.append(full_component_pixels)


    return components


def get_dominant_color(grid, pixels):
    """Finds the most frequent color among the specified pixels."""
    colors = [grid[r, c] for r, c in pixels]
    if not colors:
        return -1 # Or some indicator of empty
    counts = np.bincount(colors)
    return np.argmax(counts)


def transform(input_grid):
    """
    Transforms the input grid by finding the largest non-white object,
    counting pixels within it that don't match its dominant color,
    and creating a red column output grid whose height equals this count.
    """
    input_grid = np.array(input_grid)
    
    # 1. Find all connected components of non-white pixels
    components = find_connected_components(input_grid, ignore_color=0)

    if not components:
        # Handle edge case: no non-white pixels found
        return np.array([[]], dtype=int) # Or maybe empty grid of shape (0,1)? Task output suggests height > 0.

    # Find the largest component (the 'main object')
    largest_component_pixels = max(components, key=len)

    # Determine the dominant color *within* this largest component
    dominant_color = get_dominant_color(input_grid, largest_component_pixels)

    # 2. & 3. Iterate through the pixels of the largest component and count 'impurities'
    impurity_count = 0
    for r, c in largest_component_pixels:
        if input_grid[r, c] != dominant_color:
            impurity_count += 1

    # 4. & 5. Construct the output grid
    output_grid = np.full((impurity_count, 1), 2, dtype=int) # Fill with red (2)

    return output_grid.tolist() # Return as list of lists per ARC standard
