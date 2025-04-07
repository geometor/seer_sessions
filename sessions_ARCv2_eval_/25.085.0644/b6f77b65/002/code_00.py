import numpy as np
from collections import deque

def find_mono_objects(grid):
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []
    if rows > 0 and cols > 0:
        visited[0, 0] = True # Ignore indicator pixel location

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and not visited[r, c]:
                # Start BFS for a new monochromatic object
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    current_object_pixels.append((row, col)) # Store only coords

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Must be in bounds, same color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'pixels': current_object_pixels, # List of (r, c) tuples
                    'color': color
                })
    return objects

# Reuse input grids defined previously
grids = {'ex1': input_grid_ex1, 'ex2': input_grid_ex2, 'ex3': input_grid_ex3, 'ex4': input_grid_ex4, 'ex5': input_grid_ex5}
indicators = {'ex1': 9, 'ex2': 4, 'ex3': 6, 'ex4': 4, 'ex5': 7}
shifts = {'ex1': 0, 'ex2': 3, 'ex3': 2, 'ex4': 3, 'ex5': 3}

report = {}
for name, grid in grids.items():
    indicator = indicators[name]
    shift = shifts[name]
    mono_objects = find_mono_objects(grid)
    objects_to_keep = []
    objects_to_remove = []
    for obj in mono_objects:
        if obj['color'] == indicator:
            objects_to_remove.append(obj)
        else:
            objects_to_keep.append(obj)
    report[name] = {
        'grid_shape': grid.shape,
        'indicator_color': indicator,
        'shift_amount': shift,
        'total_mono_objects': len(mono_objects),
        'objects_kept': len(objects_to_keep),
        'objects_removed': len(objects_to_remove),
        'pixels_in_kept_objects': sum(len(o['pixels']) for o in objects_to_keep),
        'pixels_in_removed_objects': sum(len(o['pixels']) for o in objects_to_remove)
    }

# Example 1 has indicator 9, shift 0. find_mono_objects won't be used by transform.
input_grid_ex1 = np.array([ # Redefining Ex1 grid locally for the tool
    [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 6, 3, 3, 3, 0, 5, 5, 7, 0, 0],
    [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 0, 0],
    [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 0, 0],
    [0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 7, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0]
])
grids['ex1'] = input_grid_ex1 # Update dict
# Run report generation
print(report)
