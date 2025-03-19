import numpy as np

def analyze_transformation(input_grid, output_grid):
    """Analyzes the transformation between input and output grids."""
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    rows, cols = input_grid.shape
    transformations = {}

    for r in range(rows):
        for c in range(cols):
            input_val = input_grid[r, c]
            output_val = output_grid[r, c]
            if (input_val, (r + c) % 2) not in transformations:
              transformations[(input_val, (r+c)%2)] = {}
            if output_val not in transformations[(input_val, (r+c)%2)]:
              transformations[(input_val, (r+c)%2)][output_val]=0

            transformations[(input_val, (r + c) % 2)][output_val] += 1

    return transformations
def print_results(transformations):
    for k,v in transformations.items():
        input_val = k[0]
        parity = k[1]
        print(f"Input value {input_val}, {'even' if parity == 0 else 'odd'} parity:")
        for output_val, count in v.items():
          print(f'   -> Output: {output_val}, count: {count}')

task = {
    "train": [
        {
            "input": [[5, 0, 5], [0, 5, 0], [5, 0, 5]],
            "output": [[5, 8, 5], [1, 5, 8], [5, 1, 5]],
        },
        {
            "input": [[0, 5, 0, 5], [5, 0, 5, 0], [0, 5, 0, 5], [5, 0, 5, 0]],
            "output": [[8, 5, 1, 5], [5, 1, 5, 8], [8, 5, 1, 5], [5, 1, 5, 8]],
        },
        {
            "input": [[5, 5, 5, 5, 5], [5, 0, 5, 0, 5], [5, 5, 5, 5, 5], [5, 0, 5, 0, 5],[5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5], [5, 8, 5, 1, 5], [5, 5, 5, 5, 5], [5, 8, 5, 1, 5],[5, 5, 5, 5, 5]],
        },
        {
            "input": [[5, 5, 5, 5, 5, 5], [5, 0, 0, 5, 0, 0], [5, 5, 5, 5, 5, 5], [0, 0, 5, 0, 0, 5]],
            "output": [[5, 5, 5, 5, 5, 5], [5, 8, 1, 5, 8, 1], [5, 5, 5, 5, 5, 5], [1, 8, 5, 1, 8, 5]],
        },
    ],
    "test": [{"input": [[0, 0, 5], [0, 5, 0], [5, 0, 0]], "output": [[8, 1, 5], [1, 5, 8], [5, 1, 8]]}],
}

for i, example in enumerate(task["train"]):
    print(f"Example {i+1}:")
    transformations = analyze_transformation(example["input"], example["output"])
    print_results(transformations)

for i, example in enumerate(task["test"]):
    print(f"Test {i+1}:")
    transformations = analyze_transformation(example["input"], example["output"])
    print_results(transformations)