import numpy as np
from collections import defaultdict, deque

"""
Transformation Rule:

1.  **Identify L-Shapes:** Scan the input grid to find all "L-shapes". An L-shape consists of exactly three pixels of the same non-white color (1-9) occupying three out of the four cells in any 2x2 square. Record the color and the set of three coordinate pairs for each distinct L-shape found.
2.  **Determine Fill Color and Seed:** Examine the identified L-shapes. Find the *single* L-shape whose color is *not* azure (color 8). The color of this L-shape is the "Fill Color". The coordinates of the pixels forming this L-shape are the "Seed Coordinates". If no L-shapes are found, or if only azure L-shapes are found, or if more than one non-azure L-shape is found, return the original input grid unchanged.
3.  **Identify Obstacles:** Find the coordinates of all non-white pixels (colors 1-9) in the original input grid. Remove the Seed Coordinates from this set. The remaining coordinates are the "Obstacle Coordinates".
4.  **Generate Output Grid via Flood Fill:**
    a.  Create a copy of the input grid. This will be the output grid.
    b.  Initialize a queue for the flood fill algorithm and add all Seed Coordinates to it.
    c.  Initialize a set to keep track of visited coordinates during the fill. Add all Seed Coordinates to the visited set.
    d.  While the queue is not empty:
        i.  Dequeue a coordinate `(r, c)`.
        ii. If the pixel `(r, c)` in the *original input grid* was white (0), change the color of this cell in the *output grid* to the Fill Color. (Pixels that were originally non-white, including the seed pixels, are not recolored).
        iii. Explore the 8 adjacent neighbors `(nr, nc)` of `(r, c)`.
        iv. For each valid neighbor (within grid bounds):
            - If the neighbor `(nr, nc)` has not been visited AND its coordinate is *not* in the Obstacle Coordinates:
                - Add `(nr, nc)` to the visited set.
                - Enqueue `(nr, nc)`.
5.  Return the modified output grid.
"""

# ================= HELPER FUNCTIONS =================

def find_l_shapes(grid):
    """
    Finds all distinct L-shaped objects in the grid.

    An L-shape is defined as 3 pixels of the same non-white color
    occupying 3 cells of a 2x2 square.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (color, frozenset_of_coordinates).
              frozenset_of_coordinates contains (row, col) tuples for the 3 pixels
              of the L-shape. Returns an empty list if no L-shapes are found.
    """
    potential_l_shapes = []
    rows, cols = grid.shape
    if rows < 2 or cols < 2:
        return [] # Cannot form 2x2 squares

    added_shapes = set() # To track unique shapes (color, frozenset_coords)

    for r in range(rows - 1):
        for c in range(cols - 1):
            # Extract the 2x2 subgrid
            subgrid = grid[r:r+2, c:c+2]

            # Count colors in the 2x2 subgrid, excluding white (0)
            colors = defaultdict(list)
            white_count = 0
            for i in range(2):
                for j in range(2):
                    color = subgrid[i, j]
                    coord = (r + i, c + j)
                    if color == 0:
                        white_count += 1
                    else:
                        colors[color].append(coord)

            # Check for the L-shape condition: 1 white pixel and 3 pixels of the same non-white color
            if white_count == 1:
                for color, coords in colors.items():
                    if len(coords) == 3:
                        # Use frozenset for hashability needed for set operations
                        fset_coords = frozenset(coords)
                        shape_key = (int(color), fset_coords)
                        # Add if truly unique
                        if shape_key not in added_shapes:
                            potential_l_shapes.append(shape_key)
                            added_shapes.add(shape_key)
                        break # Only one L-shape per 2x2 possible

    return potential_l_shapes # Return list of (color, frozenset)

def get_all_non_white_coords(grid):
    """Finds coordinates of all non-white pixels (colors 1-9)."""
    rows, cols = grid.shape
    non_white = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                non_white.add((r, c))
    return non_white

# ================= MAIN TRANSFORM FUNCTION =================

def transform(input_grid):
    """
    Applies a flood fill transformation based on L-shapes.

    The fill color is determined by the unique non-azure L-shape.
    The fill starts from the non-azure L-shape pixels and spreads through
    white space (8-way adjacency), respecting other non-white pixels as boundaries.
    Only pixels that were originally white are recolored.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape
    output_grid = grid_np.copy() # Start with a copy

    # 1. Find all L-shapes
    all_l_shapes = find_l_shapes(grid_np)

    # 2. Find the unique non-azure L-shape to get fill color and seeds
    fill_color = -1
    seed_coords_set = set()
    non_azure_l_shape_count = 0
    for color, coords_fset in all_l_shapes:
        if color != 8: # Not azure
            non_azure_l_shape_count += 1
            fill_color = color
            seed_coords_set = set(coords_fset) # Store coordinates of the non-azure L

    # If not exactly one non-azure L-shape found, return original grid
    if non_azure_l_shape_count != 1:
        return input_grid

    # 3. Define Obstacles (all non-white pixels except the seeds)
    obstacle_coords = get_all_non_white_coords(grid_np)
    if seed_coords_set: # Should always be true if non_azure_l_shape_count == 1
        obstacle_coords = obstacle_coords - seed_coords_set # Remove seeds from obstacles
    else:
        # This case should not be reachable due to the count check above
        return input_grid

    # 4. Perform Flood Fill starting from seed coordinates
    queue = deque()
    visited = set() # Tracks cells added to queue or already processed

    # Initialize queue and visited set with seed points
    if seed_coords_set:
        for seed in seed_coords_set:
             if seed not in visited: # Check just in case, though set should handle uniqueness
                 visited.add(seed)
                 queue.append(seed)
    # If seed_coords_set is empty (no non-azure L found), the queue remains empty,
    # loop won't run, and original grid copy is returned (correct).

    # Define 8 directions for neighbors (includes diagonals)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    while queue:
        r, c = queue.popleft()

        # Action: Color the current cell IF it was originally white (0).
        # The non-azure L-shape's own pixels (seeds) are non-white and won't be colored.
        if grid_np[r, c] == 0:
             output_grid[r, c] = fill_color

        # Explore neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor_coord = (nr, nc)

            # Check bounds: Ensure neighbor is within grid limits
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor can be entered:
                # Must not have been visited AND must not be an obstacle
                if neighbor_coord not in visited and neighbor_coord not in obstacle_coords:
                     # Mark as visited and add to queue for processing
                     visited.add(neighbor_coord)
                     queue.append(neighbor_coord)

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()