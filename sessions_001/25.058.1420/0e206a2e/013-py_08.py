import numpy as np

def get_objects(grid):
    """
    Identifies and returns a dictionary of objects in the grid.
    (Same as provided code)
    """
    objects = {}
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def dfs(row, col, color, obj_id):
        if (row, col) in visited or row < 0 or row >= rows or col < 0 or col >= cols or grid[row][col] != color:
            return []

        visited.add((row, col))
        pixels = [(row, col)]

        pixels.extend(dfs(row + 1, col, color, obj_id))
        pixels.extend(dfs(row - 1, col, color, obj_id))
        pixels.extend(dfs(row, col + 1, color, obj_id))
        pixels.extend(dfs(row, col - 1, color, obj_id))

        return pixels

    obj_count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                obj_count += 1
                obj_id = f"obj_{obj_count}"
                pixels = dfs(r, c, grid[r][c], obj_id)
                objects[obj_id] = {
                    'color': grid[r][c],
                    'pixels': pixels
                }
    return objects

def object_properties(objects):
    """Computes and adds bounding box and centroid to each object's properties."""
    object_data = {}
    for obj_id, obj in objects.items():
        pixels = obj['pixels']
        if not pixels:
            continue
        min_row = min(p[0] for p in pixels)
        max_row = max(p[0] for p in pixels)
        min_col = min(p[1] for p in pixels)
        max_col = max(p[1] for p in pixels)
        centroid_row = (min_row + max_row) / 2.0
        centroid_col = (min_col + max_col) / 2.0
        object_data[obj_id] = {
            'color': obj['color'],
            'size': len(pixels),
            'bounding_box': (min_row, min_col, max_row, max_col),
            'centroid': (centroid_row, centroid_col),
            'pixels': pixels
        }
    return object_data

def calculate_centroid_shifts(input_grid, output_grid):
    """Calculates the centroid shift for each object between input and output."""
    input_objects = get_objects(input_grid)
    output_objects = get_objects(output_grid)

    input_props = object_properties(input_objects)
    output_props = object_properties(output_objects)

    shifts = {}
    for obj_id, props in input_props.items():
        # Find corresponding object in output (matching color and size, could refine)
        for out_obj_id, out_props in output_props.items():
            if (props['color'] == out_props['color'] and props['size'] == out_props['size']):
                row_shift = out_props['centroid'][0] - props['centroid'][0]
                col_shift = out_props['centroid'][1] - props['centroid'][1]
                shifts[obj_id] = (row_shift, col_shift)
                break  # Assume only one matching object

    return shifts, input_props, output_props

# Task examples (replace with your actual task data)
task_examples = [
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 4, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0, 0]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 6, 6, 6, 6, 0, 0, 0, 7, 7, 7], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    ([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
]

for i, (input_grid, output_grid) in enumerate(task_examples):
    shifts, input_props, output_props = calculate_centroid_shifts(input_grid, output_grid)
    print(f"Example {i+1}:")
    print(f"  Shifts: {shifts}")
    #for obj_id, props in input_props.items():
        #print(f"{obj_id}:{props}")
    #for obj_id, props in output_props.items():
        #print(f"{obj_id}:{props}")