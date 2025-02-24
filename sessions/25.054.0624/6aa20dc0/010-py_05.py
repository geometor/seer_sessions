"""
Transforms an input grid by expanding colored shapes based on their adjacency to other shapes.

1.  **Object Identification:** Identify all contiguous regions (objects) of non-yellow pixels. Each object is characterized by its color (1, 2, 3, 6, or 8). Adjacency is defined as 8-connectivity (including diagonals).

2.  **Blue (1) Expansion:**
    *   If a blue object is adjacent to any object of a *different* color, then extend blue color into all yellow cells immediately adjacent to *any* blue cells in the object.
    *    If blue is not adjacent to any objects of a different color - do not change anything.

3.  **Red (2) Expansion:**
    *   If a red object is adjacent to another object of a *different* color. Extend red by a single layer into yellow around adjacent objects, excluding other red objects.

4.  **Magenta (6) Expansion:**
    *   If a magenta object is adjacent to a yellow cell, fill the yellow cell with the magenta color.

5. **Green(3) and Azure(8):** These colors do not expand.

6.  **Yellow (4):** Remains unchanged unless filled by an expanding object (blue, red, or magenta).
"""

import numpy as np

def get_objects(grid):
    """
    Finds all contiguous regions of non-yellow pixels, identifying them as distinct objects.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj_id):
        if (r < 0 or r >= rows or c < 0 or c >= cols or visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        objects[obj_id]['pixels'].append((r, c))
        dfs(r + 1, c, color, obj_id)
        dfs(r - 1, c, color, obj_id)
        dfs(r, c + 1, color, obj_id)
        dfs(r, c - 1, color, obj_id)
        dfs(r + 1, c + 1, color, obj_id)
        dfs(r - 1, c - 1, color, obj_id)
        dfs(r + 1, c - 1, color, obj_id)
        dfs(r - 1, c + 1, color, obj_id)


    obj_id_counter = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 4 and not visited[r, c]:
                objects[obj_id_counter] = {'color': grid[r, c], 'pixels': []}
                dfs(r, c, grid[r, c], obj_id_counter)
                obj_id_counter += 1
    return objects

def get_neighbors(grid, r, c):
    """Returns a list of (row, col) tuples for all 8 neighbors of a pixel."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def expand_blue(grid, output_grid, objects):
    """Expands blue shapes based on adjacency to different colored shapes."""
    for obj_id, obj_data in objects.items():
        if obj_data['color'] == 1:  # Blue object
            adjacent_to_other_color = False
            for r, c in obj_data['pixels']:
                neighbors = get_neighbors(grid, r, c)
                for nr, nc in neighbors:
                    if grid[nr, nc] != 1 and grid[nr,nc] != 4:
                        adjacent_to_other_color = True
                        break
                if adjacent_to_other_color:
                    break

            if adjacent_to_other_color:
                for r, c in obj_data['pixels']:
                    neighbors = get_neighbors(grid, r,c)
                    for nr, nc in neighbors:
                        if output_grid[nr,nc] == 4:
                            output_grid[nr,nc] = 1


def expand_red(grid, output_grid, objects):
    """Expands red shapes to create a perimeter around adjacent objects."""
    for obj_id, obj_data in objects.items():
        if obj_data['color'] == 2:
            new_red_pixels = []
            for r, c in obj_data['pixels']:
                neighbors = get_neighbors(grid, r, c)

                for nr, nc in neighbors:
                    if grid[nr,nc] != 2 and grid[nr,nc] != 4: #neighbor is a different object
                        target_object = None
                        for other_obj_id, other_obj_data in objects.items():
                            if (nr,nc) in other_obj_data['pixels']:
                                target_object = other_obj_data
                                break

                        if target_object:
                            target_neighbors = get_neighbors(grid, nr, nc)
                            for tnr, tnc in target_neighbors:
                                if grid[tnr, tnc] == 4:
                                    new_red_pixels.append((tnr,tnc))
            for r,c in new_red_pixels:
                output_grid[r,c] = 2


def expand_magenta(grid, output_grid, objects):
    """Expands magenta shapes by filling immediately adjacent yellow cells."""
    for obj_id, obj_data in objects.items():
        if obj_data['color'] == 6:  # Magenta object
            for r, c in obj_data['pixels']:
                neighbors = get_neighbors(grid, r, c)
                for nr, nc in neighbors:
                    if grid[nr, nc] == 4:  # Adjacent to yellow
                        output_grid[nr, nc] = 6


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    objects = get_objects(input_grid)

    # change output pixels
    expand_blue(input_grid, output_grid, objects)
    expand_red(input_grid, output_grid, objects)
    expand_magenta(input_grid, output_grid, objects)


    return output_grid