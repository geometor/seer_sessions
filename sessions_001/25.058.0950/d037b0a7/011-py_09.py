import numpy as np

def analyze_grid(grid):
    """
    Analyzes a grid to find objects and their properties.
    Returns a dictionary of objects, their colors, and bounding box coordinates.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(row, col, color, object_id):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        objects[object_id]["coords"].append((row, col))
        dfs(row + 1, col, color, object_id)
        dfs(row - 1, col, color, object_id)
        dfs(row, col + 1, color, object_id)
        dfs(row, col - 1, color, object_id)

    object_count = 0
    for row in range(rows):
        for col in range(cols):
            if not visited[row, col]:
                color = grid[row, col]
                object_id = f"object_{object_count}"
                objects[object_id] = {"color": color, "coords": []}
                dfs(row, col, color, object_id)
                object_count += 1

    # calculate bounding box.
    for obj_id, obj_data in objects.items():
        coords = obj_data["coords"]
        if coords:
            min_row = min(coords, key=lambda x: x[0])[0]
            max_row = max(coords, key=lambda x: x[0])[0]
            min_col = min(coords, key=lambda x: x[1])[1]
            max_col = max(coords, key=lambda x: x[1])[1]
            objects[obj_id]["bounding_box"] = (min_row, min_col, max_row, max_col)

    return objects

def get_grid_summary(grid, title="Grid"):
    summary = f"{title}:\n"
    rows, cols = grid.shape
    summary += f"  Dimensions: {rows}x{cols}\n"
    objects = analyze_grid(grid)
    for obj_id, obj_data in objects.items():
        color = obj_data["color"]
        bounding_box = obj_data["bounding_box"]
        summary += f"  {obj_id}: Color={color}, Bounding Box={bounding_box}\n"
    return summary

def show_result_diff(expected_grid, actual_grid):
    """
    highlights the difference between the expected and actual grids
    """
    diff = expected_grid != actual_grid
    print(np.where(diff, 'X', '.'))

# Load the example grids and perform analyses

task_data = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
                [0, 8, 8, 8, 8, 8, 8, 8, 0, 0],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 0, 0, 6, 6, 6, 0],
                [0, 8, 8, 8, 0, 0, 6, 6, 6, 0],
                [0, 8, 8, 8, 0, 0, 6, 6, 6, 0],
                [0, 8, 8, 8, 0, 0, 6, 6, 6, 0],
                [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
                [0, 8, 8, 8, 0, 0, 6, 6, 6, 0],
                [0, 8, 8, 8, 0, 0, 6, 6, 6, 0],
                [0, 8, 8, 8, 0, 0, 6, 6, 6, 0],
                [0, 8, 8, 8, 0, 0, 6, 6, 6, 0],
                [0, 8, 8, 8, 0, 0, 6, 6, 6, 0],
                [0, 8, 8, 8, 0, 0, 6, 6, 6, 0],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
                [0, 4, 4, 4, 4, 4, 4, 4, 0, 0],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 6, 6, 6, 0],
                [0, 0, 0, 0, 0, 0, 6, 6, 6, 0],
                [0, 0, 0, 0, 0, 0, 6, 6, 6, 0],
                [0, 4, 4, 4, 0, 0, 6, 6, 6, 0],
                [0, 4, 4, 4, 0, 0, 6, 6, 6, 0],
                [0, 4, 4, 4, 0, 0, 0, 0, 0, 0],
                [0, 4, 4, 4, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 6, 6, 6, 0],
                [0, 0, 0, 0, 0, 0, 6, 6, 6, 0],
                [0, 0, 0, 0, 0, 0, 6, 6, 6, 0],
                [0, 4, 4, 4, 0, 0, 6, 6, 6, 0],
                [0, 4, 4, 4, 0, 0, 6, 6, 6, 0],
                [0, 4, 4, 4, 0, 0, 6, 6, 6, 0],
                [0, 4, 4, 4, 0, 0, 6, 6, 6, 0],
                [0, 4, 4, 4, 0, 0, 6, 6, 6, 0],
                [0, 4, 4, 4, 0, 0, 6, 6, 6, 0],
            ],
        },
    ]
}

import numpy as np

def get_cell_by_value(grid, value):
    # Find the coordinates of a cell with a specific value.
    coords = np.where(grid == value)
    if len(coords[0]) > 0:
       return (coords[0][0], coords[1][0])
    return None

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the cell with value 6 (magenta).
    magenta_cell = get_cell_by_value(input_grid, 6)
    yellow_cell = get_cell_by_value(input_grid, 4)
    
    if magenta_cell and yellow_cell:
      if magenta_cell[1] > yellow_cell[1]:
        right_cell = magenta_cell
        left_cell = yellow_cell
      else:
        right_cell = yellow_cell
        left_cell = magenta_cell

      output_grid[left_cell[0]:, right_cell[1]] = output_grid[right_cell[0], right_cell[1]]
      output_grid[right_cell[0]:, left_cell[1]] = output_grid[left_cell[0], left_cell[1]]
    elif magenta_cell:
        output_grid[magenta_cell[0]:, magenta_cell[1]] = 6
    elif yellow_cell:
        output_grid[yellow_cell[0]:, yellow_cell[1]] = 4
    
    return output_grid

# Perform analysis and print results

for i, example in enumerate(task_data["train"]):
    input_grid = np.array(example["input"])
    expected_output_grid = np.array(example["output"])
    actual_output_grid = transform(input_grid)

    print(f"--- Example {i + 1} ---")
    print(get_grid_summary(input_grid, "Input Grid"))
    print(get_grid_summary(expected_output_grid, "Expected Output Grid"))
    print(get_grid_summary(actual_output_grid, "Actual Output Grid"))
    print("Differences (X = mismatch):")
    show_result_diff(expected_output_grid, actual_output_grid)
    print("\n")