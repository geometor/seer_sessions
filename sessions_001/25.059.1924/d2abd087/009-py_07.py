import numpy as np

def report(input_grid, expected_output, transform):
    """Reports on the transformation, comparing the actual output with the expected output."""
    actual_output = transform(input_grid)
    diff = actual_output == expected_output
    correct_pixels = np.sum(diff)
    total_pixels = diff.size
    accuracy = correct_pixels/total_pixels
    print(f'  accuracy: {accuracy}')
    print(f'  correct_pixels: {correct_pixels}')
    print(f'  total_pixels: {total_pixels}')
    print(f'  equal: {np.array_equal(actual_output, expected_output)}')

def load(grid_string):
    return np.array([int(cell) for cell in grid_string],dtype="uint8").reshape((len(grid_string)**0.5,len(grid_string)**0.5))

task = {
    "train": [
        {
            "input": "0000000000005000000000000",
            "output": "0000000000002000000000000",
        },
        {
            "input": "0005000055000",
            "output": "0002000022000",
        },
        {
            "input": "0000055000000",
            "output": "0000022000000",
        },
        {
            "input": "050000005000",
            "output": "020000002000",
        },
        {
            "input": "00005000000050000",
            "output": "00002000000020000",
        },
    ],
}

for i, example in enumerate(task["train"]):
  print(f'example: {i}')
  report(load(example["input"]), load(example["output"]), transform)