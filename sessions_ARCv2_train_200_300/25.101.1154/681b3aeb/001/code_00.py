import numpy as np
from collections import deque

"""
Identifies the two distinct colored objects in the input grid.
For each object, determines its color, bounding box, shape within the bounding box, 
bounding box area, and maximum dimension (max(height, width)).
Determines a "Winner" and "Loser" object based on bounding box area (larger wins) 
or color index (lower wins if areas are equal).
Calculates the output grid size 'S' as the maximum of the two objects' maximum dimensions.
Creates an intermediate grid by overlaying the Winner's shape and then the Loser's shape 
(Winner's color takes precedence on overlap) onto an S x S grid.
Creates the final output grid by filling any remaining background cells in the intermediate grid 
with the Loser's color.
"""

def find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all distinct contiguous objects of non-background colors in the grid.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains 'color', 'coords' (set of (r, c) tuples), 'min_r', 'max_r',
        'min_c', 'max_c', 'height', 'width', 'bbox_area', 'max_dim', and 'shape'.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Explore 4-way neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                height = max_r - min_r + 1
                width = max_c - min_c + 1
                bbox_area = height * width
                max_dim = max(height, width)

                # Extract shape relative to bounding box top-left
                shape = np.zeros((height, width), dtype=int)
                for cr, cc in coords:
                    shape[cr - min_r, cc - min_c] = color

                objects.append({
                    'color': color,
                    'coords': coords,
                    'min_r': min_r,
                    'max_r': max_r,
                    'min_c': min_c,
                    'max_c': max_c,
                    'height': height,
                    'width': width,
                    'bbox_area': bbox_area,
                    'max_dim': max_dim,
                    'shape': shape
                })
    return objects

def pad_shape(shape: np.ndarray, target_size: int, fill_value: int = 0) -> np.ndarray:
    """
    Pads a shape (numpy array) to a target square size.

    Args:
        shape: The 2D numpy array representing the object's shape.
        target_size: The side length of the target square grid.
        fill_value: The value to fill the padding area with (default 0).

    Returns:
        A new numpy array of size target_size x target_size with the shape placed at the top-left.
    """
    padded_grid = np.full((target_size, target_size), fill_value, dtype=int)
    h, w = shape.shape
    padded_grid[0:h, 0:w] = shape
    return padded_grid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the described overlay and fill logic.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    grid_np = np.array(input_grid, dtype=int)

    # 1. Identify the two colored objects
    objects = find_objects(grid_np)
    if len(objects) != 2:
        # Handle error case or unexpected input
        # For ARC tasks, we generally assume valid input based on examples
        print(f"Warning: Expected 2 objects, found {len(objects)}")
        # Returning input might be a safe default, or raise an error
        return input_grid 
        
    obj1, obj2 = objects[0], objects[1]

    # 2. Determine the output grid dimension
    output_size = max(obj1['max_dim'], obj2['max_dim'])

    # 3. Determine the Winner (W) and Loser (L) objects
    if obj1['bbox_area'] > obj2['bbox_area']:
        winner = obj1
        loser = obj2
    elif obj2['bbox_area'] > obj1['bbox_area']:
        winner = obj2
        loser = obj1
    else: # Areas are equal, compare by color index
        if obj1['color'] < obj2['color']:
             winner = obj1
             loser = obj2
        else:
             winner = obj2
             loser = obj1

    # 4. Pad Winner's shape and Loser's shape to S x S grids
    padded_winner_shape = pad_shape(winner['shape'], output_size)
    padded_loser_shape = pad_shape(loser['shape'], output_size)

    # 5. Create the initial overlay grid (Overlay) of size S x S
    # Start with the loser's shape, then overlay winner
    overlay_grid = np.copy(padded_loser_shape)
    # Where winner shape is non-zero, overwrite loser shape
    overlay_grid[padded_winner_shape != 0] = padded_winner_shape[padded_winner_shape != 0]
    
    # # Alternative overlay logic (explicit iteration):
    # overlay_grid = np.zeros((output_size, output_size), dtype=int)
    # for r in range(output_size):
    #     for c in range(output_size):
    #         if padded_winner_shape[r, c] != 0:
    #             overlay_grid[r, c] = padded_winner_shape[r, c]
    #         elif padded_loser_shape[r, c] != 0:
    #             overlay_grid[r, c] = padded_loser_shape[r, c]


    # 6. Create the final output grid (Output) by filling background
    output_grid = np.copy(overlay_grid)
    # Fill background (0) cells with the Loser's color
    output_grid[output_grid == 0] = loser['color']

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()