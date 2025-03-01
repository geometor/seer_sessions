import numpy as np

def code_execution(input_grid, output_grid, predicted_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_grid = np.array(predicted_grid)

    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    predicted_objects = find_objects(predicted_grid)
    
    print("Input Objects:")
    for obj_id, obj_data in input_objects.items():
        print(f"  Object {obj_id}: Color={obj_data['color']}, Pixels={obj_data['pixels']}")

    print("\nOutput Objects:")
    for obj_id, obj_data in output_objects.items():
        print(f"  Object {obj_id}: Color={obj_data['color']}, Pixels={obj_data['pixels']}")

    print("\nPredicted Objects:")
    for obj_id, obj_data in predicted_objects.items():
        print(f"  Object {obj_id}: Color={obj_data['color']}, Pixels={obj_data['pixels']}")

    print(f"Correct Prediction: {np.array_equal(output_grid, predicted_grid)}")

def find_objects(grid):
    """
    Identifies distinct objects in a grid.  An object is a set of connected pixels of the same color.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, object_id):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return
        visited.add((r, c))
        objects[object_id]['pixels'].append((r, c))
        dfs(r + 1, c, color, object_id)
        dfs(r - 1, c, color, object_id)
        dfs(r, c + 1, color, object_id)
        dfs(r, c - 1, color, object_id)

    object_id = 0
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                objects[object_id] = {'color': grid[r, c], 'pixels': []}
                dfs(r, c, grid[r, c], object_id)
                object_id += 1

    return objects