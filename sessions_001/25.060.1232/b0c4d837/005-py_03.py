import numpy as np

def analyze_example(input_grid, expected_output, actual_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    azure_coords = np.argwhere(input_grid == 8)
    num_azure = len(azure_coords)
    azure_positions = azure_coords.tolist() if num_azure > 0 else "None"

    input_dims = input_grid.shape
    output_dims = expected_output.shape

    comparison = (expected_output == actual_output).all()

    print(f"  Azure Pixels: Count={num_azure}, Positions={azure_positions}")
    print(f"  Input Dimensions: {input_dims}")
    print(f"  Output Dimensions: {output_dims}")
    print(f"  Expected Output Matches Actual: {comparison}")
    if not comparison:
       diff = np.where(expected_output!=actual_output)
       print(f"  Differences at: {list(zip(diff[0],diff[1]))}")

examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0], [0, 8, 0], [0, 8, 0]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0], [0, 8, 0], [0, 0, 0]],
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0], [0, 8, 0], [0, 0, 0]],
    },
    {
       "input":  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
       "output": [[0, 0, 0], [8, 0, 0], [0, 0, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
      "output": [[0, 0, 0], [8, 0, 0], [0, 0, 0]]
    }
]

for i, example in enumerate(examples):
    print(f"Example {i+1}:")
    actual_output = transform(example["input"])
    analyze_example(example["input"], example["output"], actual_output)
    print("-" * 40)
