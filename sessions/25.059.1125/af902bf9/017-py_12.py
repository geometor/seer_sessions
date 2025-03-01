import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous regions (objects) of a specified color in a grid.
    Returns a list of lists, where each inner list contains the coordinates
    of pixels belonging to a single object.
    """
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def analyze_example(input_grid, output_grid):
    """
    Analyzes a single input-output pair and returns a report.
    """
    yellow_objects_input = find_objects(input_grid, 4)
    yellow_objects_output = find_objects(output_grid, 4)
    red_objects_input = find_objects(input_grid, 2)
    red_objects_output = find_objects(output_grid, 2)

    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape

    changes = []
    for r in range(max(input_rows, output_rows)):
        for c in range(max(input_cols, output_cols)):
            input_val = input_grid[r, c] if r < input_rows and c < input_cols else None
            output_val = output_grid[r, c] if r < output_rows and c < output_cols else None
            if input_val != output_val:
                changes.append(
                    {
                        "location": (r, c),
                        "input_value": input_val,
                        "output_value": output_val,
                    }
                )

    report = {
        "input_grid_shape": input_grid.shape,
        "output_grid_shape": output_grid.shape,
        "yellow_objects_input": yellow_objects_input,
        "yellow_objects_output": yellow_objects_output,
        "red_objects_input": red_objects_input,
        "red_objects_output": red_objects_output,
         "changes": changes
    }
    return report

#Example usage with the training data
train = [
    [
        np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 4, 4, 4, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 4, 2, 4, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
            ]
        ),
    ],
    [
        np.array(
            [
                [4, 0, 0, 0, 0, 0, 0, 0, 0],
                [4, 0, 0, 0, 0, 0, 0, 0, 0],
                [4, 0, 0, 0, 0, 0, 0, 0, 0],
                [4, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 4],
                [0, 0, 0, 0, 0, 0, 0, 4, 4],
                [0, 0, 0, 0, 0, 0, 0, 0, 4],
            ]
        ),
        np.array(
            [
                [2, 0, 0, 0, 0, 0, 0, 0, 0],
                [4, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 0, 0, 0, 0, 0, 0, 0, 0],
                [4, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 4],
                [0, 0, 0, 0, 0, 0, 0, 4, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 4],
            ]
        ),
    ],
    [
        np.array(
            [
                [0, 0, 0, 4, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 4, 0, 0, 0, 0, 0, 0, 0],
                [0, 4, 0, 0, 0, 0, 0, 0, 0],
                [0, 4, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [4, 4, 4, 0, 0, 0, 0, 0, 0],
            ]
        ),
        np.array(
            [
                [0, 0, 0, 4, 2, 0, 0, 0, 0],
                [0, 0, 0, 0, 4, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 4, 0, 0, 0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0, 0, 0, 0, 0],
                [0, 4, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [4, 2, 4, 0, 0, 0, 0, 0, 0],
            ]
        ),
    ],
]

reports = [analyze_example(inp, out) for inp, out in train]

for i, report in enumerate(reports):
    print(f"--- Example {i+1} ---")
    print(report)