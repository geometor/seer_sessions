import numpy as np

def compare_grids(input_grid, output_grid):
    """Compares two grids and returns a description of the differences."""
    input_array = np.array(input_grid)
    output_array = np.array(output_grid)

    if input_array.shape != output_array.shape:
        return "Different dimensions"

    differences = []
    for row_index in range(input_array.shape[0]):
        for col_index in range(input_array.shape[1]):
            if input_array[row_index, col_index] != output_array[row_index, col_index]:
                differences.append(
                    f"Pixel at ({row_index}, {col_index}) changed from "
                    f"{input_array[row_index, col_index]} to {output_array[row_index, col_index]}"
                )
    return differences if differences else "No differences"
#test on first pair
task = {
    "train": [
        {
            "input": [[0, 0, 0], [0, 5, 0], [0, 0, 0]],
            "output": [[0, 0, 0], [0, 5, 0], [0, 0, 0]],
        },
        {
            "input": [[0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 8, 8, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 7, 7, 7, 7, 7, 7, 0, 0], [0, 0, 7, 7, 7, 7, 7, 7, 0, 0]],
        },
                {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 6, 6, 6, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        }
    ]
}

for i, example in enumerate(task["train"]):
  result = compare_grids(example['input'],example['output'])
  print(f"train[{i}]: {result}")