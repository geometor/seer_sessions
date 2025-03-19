import numpy as np

def get_object_coordinates(grid, color=None):
    coords = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != 0 and (color is None or grid[r][c] == color):
                coords.append((r, c))
    return coords

def calculate_center(width):
    return (width - 1) / 2

def calculate_mirrored_col(col, width):
    center = calculate_center(width)
    return int(2 * center - col)

task_data = {
    "train": [
        {
            "input": [[0, 0, 0], [0, 3, 0], [0, 0, 0]],
            "output": [[0, 0, 0, 0, 0], [0, 3, 0, 3, 0], [0, 0, 0, 0, 0]],
            "result": [[0, 0, 0, 0, 0], [0, 3, 0, 3, 0], [0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 9, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 9, 0, 0, 0, 0, 9, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "result": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 9, 0, 0, 0, 0, 9, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
       {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]],
            "result": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[1, 0, 0], [0, 0, 0], [0, 0, 2]],
            "output": [[1, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 2]],
            "result": [[1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 2]]

        },

    ],
    "test": [
        {"input": [[0, 0, 0], [0, 5, 0], [0, 0, 0]]},
    ],
}
for group_name, examples in task_data.items():
  for i, ex in enumerate(examples):

        input_grid = ex['input']
        expected_output_grid = ex['output']
        result_grid = ex.get('result', None)  # result might not be provided.

        input_height = len(input_grid)
        input_width = len(input_grid[0])
        output_height = len(expected_output_grid)
        output_width = len(expected_output_grid[0])
        print(f"Example {i+1}:")
        print(f"  Input:  height={input_height}, width={input_width}")
        print(f"  Output: height={output_height}, width={output_width}")

        # get all objects and positions.
        input_objects = {}
        for color in range(1, 10):  # Check colors 1-9
            coords = get_object_coordinates(input_grid, color)
            if coords:
                input_objects[color] = coords

        print(f"    Input Objects: {input_objects}")

        if result_grid is not None:
            result_height = len(result_grid)
            result_width = len(result_grid[0])
            print(f"  Result: height={result_height}, width={result_width}")

            result_objects = {}
            for color in range(1, 10):
                coords = get_object_coordinates(result_grid, color)
                if coords:
                    result_objects[color] = coords
            print(f"    Result Objects: {result_objects}")
        else:
            print("  Result: (not provided)")

        expected_objects = {}
        for color in range(1,10):
            coords = get_object_coordinates(expected_output_grid, color)
            if coords:
                expected_objects[color] = coords
        print(f"    Expected Objects: {expected_objects}")