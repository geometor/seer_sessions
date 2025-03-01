import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    """Analyzes a single example and provides metrics."""

    def find_objects(grid):
        """Identifies distinct objects based on color contiguity."""
        objects = {}
        visited = set()

        def dfs(row, col, color, obj_id):
            if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
                return
            visited.add((row, col))
            objects[obj_id].append((row, col))
            dfs(row + 1, col, color, obj_id)
            dfs(row - 1, col, color, obj_id)
            dfs(row, col + 1, color, obj_id)
            dfs(row, col - 1, color, obj_id)

        obj_id = 0
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                color = grid[row, col]
                if color != 0 and (row, col) not in visited:
                    objects[obj_id] = []
                    dfs(row, col, color, obj_id)
                    obj_id += 1
        return objects

    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    predicted_objects = find_objects(predicted_grid)

    print("Input Objects:", input_objects)
    print("Output Objects:", output_objects)
    print("Predicted Objects:", predicted_objects)
    print("Correct Prediction:", np.array_equal(output_grid, predicted_grid))
    print("-" * 20)

# Assuming 'transform' function and example data are defined as before
from task_data import train_data
for i, example in enumerate(train_data):
    input_grid = example["input"]
    output_grid = example["output"]
    predicted_grid = transform(np.array(input_grid))  # Ensure input is a numpy array
    print(f"Example {i+1}:")
    analyze_example(np.array(input_grid), np.array(output_grid), predicted_grid)