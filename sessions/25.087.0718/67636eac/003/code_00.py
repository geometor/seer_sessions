import numpy as np
from collections import deque
import math

"""
Identify all distinct non-white objects (contiguous pixels of same color, 8-way connectivity).
For each object, find its minimal bounding box, extract the subgrid, determine its color, and calculate its center coordinates.
If zero objects, output a 1x1 white grid.
If one object, output its extracted subgrid.
If multiple objects, calculate standard deviation of row centers (std_rows) and column centers (std_cols).
Determine alignment type: 'Vertical' if std_cols < std_rows, otherwise 'Horizontal/Scattered'.
Sort the objects: by top-left position (row then col) if 'Vertical', by color index (ascending) if 'Horizontal/Scattered'.
Assemble output based on alignment:
    If 'Vertical': Stack sorted subgrids vertically, left-aligned. Output width is max subgrid width, output height is sum of subgrid heights. Pad right with white if needed.
    If 'Horizontal/Scattered': Place sorted subgrids horizontally adjacent, top-aligned. Output height is max subgrid height, output width is sum of subgrid widths. Pad bottom with white if needed.
"""

def find_objects_with_details(grid):
    """
    Finds all connected components (objects) of non-white pixels using 8-way connectivity,
    and gathers details like color, bounding box, center, and extracted subgrid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dict contains information about an object:
              {'pixels': set((r, c)), 'color': int, 'bbox': tuple(min_r, min_c, h, w),
               'center': tuple(center_r, center_c), 'subgrid': np.ndarray}
              Returns an empty list if no non-white objects are found.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects_data = []
    # 8-way connectivity (including diagonals)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for r in range(height):
        for c in range(width):
            # If pixel is non-white and not visited, start a search (BFS)
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_object_pixels.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    # Check all 8 neighbors
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds, visited status, and if neighbor has the same color
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            current_object_pixels.add((nr, nc))
                            q.append((nr, nc))

                # If an object was found, calculate its properties
                if current_object_pixels:
                    rows = [px_r for px_r, px_c in current_object_pixels]
                    cols = [px_c for px_r, px_c in current_object_pixels]
                    min_r, max_r = min(rows), max(rows)
                    min_c, max_c = min(cols), max(cols)
                    h = max_r - min_r + 1
                    w = max_c - min_c + 1
                    bbox = (min_r, min_c, h, w)
                    center_r = min_r + (h - 1) / 2.0
                    center_c = min_c + (w - 1) / 2.0
                    center = (center_r, center_c)
                    subgrid = grid[min_r : min_r + h, min_c : min_c + w]

                    objects_data.append({
                        'pixels': current_object_pixels,
                        'color': int(color), # Ensure standard int type
                        'bbox': bbox,
                        'center': center,
                        'subgrid': subgrid
                    })
    return objects_data


def transform(input_grid):
    """
    Transforms the input grid based on the spatial alignment of its non-white objects.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)

    # 1. Find Objects and their details
    objects_data = find_objects_with_details(input_np)
    num_objects = len(objects_data)

    # 2. Handle Simple Cases
    if num_objects == 0:
        return [[0]] # Output 1x1 white grid
    if num_objects == 1:
        return objects_data[0]['subgrid'].tolist() # Output the single object's subgrid

    # 3. Analyze Multiple Objects
    centers = np.array([obj['center'] for obj in objects_data])
    
    # Using try-except for std dev calculation in case of single point variance
    try:
        std_rows = np.std(centers[:, 0]) if centers.shape[0] > 1 else 0
    except IndexError:
        std_rows = 0
        
    try:
        std_cols = np.std(centers[:, 1]) if centers.shape[0] > 1 else 0
    except IndexError:
        std_cols = 0

    # Determine alignment and sort
    # Add a small epsilon to handle floating point comparisons near zero, though std>=0
    # Treat std_cols == std_rows as Horizontal/Scattered
    if std_cols < std_rows:
        alignment = "Vertical"
        # Sort by top-left (bbox[0], then bbox[1])
        objects_data.sort(key=lambda x: (x['bbox'][0], x['bbox'][1]))
    else: # std_cols >= std_rows
        alignment = "Horizontal/Scattered"
        # Sort by color index
        objects_data.sort(key=lambda x: x['color'])

    # 4. Assemble Output Grid
    if alignment == "Vertical":
        # Calculate output dimensions
        max_width = 0
        total_height = 0
        for obj in objects_data:
            h, w = obj['subgrid'].shape
            total_height += h
            if w > max_width:
                max_width = w

        # Initialize output grid
        output_grid = np.zeros((total_height, max_width), dtype=int)

        # Stack subgrids vertically
        current_row = 0
        for obj in objects_data:
            subgrid = obj['subgrid']
            h, w = subgrid.shape
            output_grid[current_row : current_row + h, 0 : w] = subgrid
            current_row += h

    else: # alignment == "Horizontal/Scattered"
        # Calculate output dimensions
        max_height = 0
        total_width = 0
        for obj in objects_data:
            h, w = obj['subgrid'].shape
            total_width += w
            if h > max_height:
                max_height = h

        # Initialize output grid
        output_grid = np.zeros((max_height, total_width), dtype=int)

        # Place subgrids horizontally adjacent
        current_col = 0
        for obj in objects_data:
            subgrid = obj['subgrid']
            h, w = subgrid.shape
            # Place subgrid, top-aligned. Padding bottom with 0 happens automatically.
            output_grid[0 : h, current_col : current_col + w] = subgrid
            current_col += w

    # Convert final numpy array back to a list of lists
    return output_grid.tolist()