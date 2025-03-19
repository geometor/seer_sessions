import numpy as np

def code_execution(input_grid, output_grid, transformed_grid):
    """Executes code and prints information about results"""

    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    transformed_grid = np.array(transformed_grid)

    print(f"Input Grid:\n{input_grid}\n")
    print(f"Expected Output Grid:\n{output_grid}\n")
    print(f"Transformed Grid:\n{transformed_grid}\n")

    print(f"Shapes - Input: {input_grid.shape}, Expected: {output_grid.shape}, Transformed: {transformed_grid.shape}")
    print(f"Correct Transformation: {np.array_equal(output_grid, transformed_grid)}")
    
    # identify where differences are:
    if not np.array_equal(output_grid, transformed_grid):
        diff = output_grid != transformed_grid
        print(f"Number of incorrect pixels: {np.sum(diff)}")
        print(f"Locations of incorrect pixels: {np.argwhere(diff)}")

# Example Data (replace with your actual data)
task_examples = [
  {
        "input": [
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "output": [
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
      },
      {
        "input": [
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "output": [
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
      },
    {
        "input": [
          [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 4, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "output": [
          [4, 4, 4, 4, 4, 4, 4, 4],
          [4, 4, 4, 4, 4, 4, 4, 4],
          [1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1]
        ]
      },
      {
        "input": [
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "output": [
          [0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4],
          [0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4],
          [0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
      },
      {
        "input": [
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 4, 0, 0, 0, 0, 1, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "output": [
          [4, 4, 4, 4, 4, 4, 4, 1, 1, 1],
          [4, 4, 4, 4, 4, 4, 4, 1, 1, 1],
          [4, 4, 4, 4, 4, 4, 4, 1, 1, 1]
        ]
      }
]

from SEER_utils import transform

for i, example in enumerate(task_examples):
    print(f"Example {i+1}:")
    transformed_grid = transform(example["input"])
    code_execution(example["input"], example["output"], transformed_grid)
    print("-" * 40)