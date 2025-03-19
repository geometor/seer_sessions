import numpy as np
from collections import Counter

def get_objects(grid):
    """
    Identifies contiguous objects within a grid.

    Args:
        grid: A 2D numpy array representing the grid.

    Returns:
        A dictionary where keys are object IDs (integers) and values are lists
        of (row, col) tuples representing the object's pixels.
        Also returns a dictionary mapping object id to color
    """

    objects = {}
    object_colors = {}
    visited = set()
    object_id_counter = 0

    def dfs(row, col, color, object_id):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return
        visited.add((row, col))
        if object_id not in objects:
            objects[object_id] = []
        objects[object_id].append((row, col))
        dfs(row + 1, col, color, object_id)
        dfs(row - 1, col, color, object_id)
        dfs(row, col + 1, color, object_id)
        dfs(row, col - 1, color, object_id)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                color = grid[row, col]
                dfs(row, col, color, object_id_counter)
                object_colors[object_id_counter] = color
                object_id_counter += 1
    return objects, object_colors

def analyze_example(input_grid, output_grid):
    """
    Analyzes a single input-output pair.

    Args:
        input_grid: The input grid.
        output_grid: The output grid.

    Returns:
        A dictionary containing analysis results.
    """

    input_objects, input_object_colors = get_objects(input_grid)
    output_objects, output_object_colors = get_objects(output_grid)

    # Basic counts
    input_object_count = len(input_objects)
    output_object_count = len(output_objects)

    # Color counts
    input_color_counts = Counter(input_object_colors.values())
    output_color_counts = Counter(output_object_colors.values())

    # Object size analysis
    input_object_sizes = {obj_id: len(pixels) for obj_id, pixels in input_objects.items()}
    output_object_sizes = {obj_id: len(pixels) for obj_id, pixels in output_objects.items()}

    print(f"Input object count: {input_object_count}")
    print(f"Output object count: {output_object_count}")
    print(f"Input Color counts: {input_color_counts}")
    print(f"Output Color counts: {output_color_counts}")
    print(f"Input object sizes: {input_object_sizes}")
    print(f"output object sizes: {output_object_sizes}")

    return {
        "input_object_count": input_object_count,
        "output_object_count": output_object_count,
        "input_color_counts": input_color_counts,
        "output_color_counts": output_color_counts,
        "input_object_sizes": input_object_sizes,
        "output_object_sizes": output_object_sizes,
    }

# Example Usage (replace with actual grids from the task)
task_data = {
    "train": [
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]],
        },
        {
            "input": [[0, 0, 5, 0, 0, 0, 0, 5, 0, 0], [0, 5, 0, 0, 0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 5, 0, 0, 0], [0, 0, 0, 0, 5, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 0, 0, 0, 0, 0, 0, 5, 0], [0, 0, 5, 0, 0, 0, 0, 5, 0, 0]],
            "output": [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]],
        },
		{
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]],
        },
    ]
}

for example in task_data["train"]:
  input_grid = np.array(example["input"])
  output_grid = np.array(example["output"])
  print(f"Analyzing example:")
  analyze_example(input_grid, output_grid)
  print("-" * 20)