import numpy as np

def find_pixels(grid, color):
    return np.argwhere(grid == color)

def analyze_example(example):
    input_grid = np.array(example['input'])
    expected_output_grid = np.array(example['output'])
    actual_output_grid = transform(input_grid)
    
    input_azure_count = len(find_pixels(input_grid, 8))
    input_yellow_count = len(find_pixels(input_grid, 4))
    expected_azure_count = len(find_pixels(expected_output_grid, 8))
    expected_yellow_count = len(find_pixels(expected_output_grid, 4))
    actual_azure_count = len(find_pixels(actual_output_grid, 8))
    actual_yellow_count = len(find_pixels(actual_output_grid, 4))

    print(f"  Input shape: {input_grid.shape}")
    print(f"  Expected Output shape: {expected_output_grid.shape}")
    print(f"  Actual Output shape: {actual_output_grid.shape}")
    print(f"  Input Azure: {input_azure_count}, Yellow: {input_yellow_count}")
    print(f"  Expected Azure: {expected_azure_count}, Yellow: {expected_yellow_count}")
    print(f"  Actual Azure: {actual_azure_count}, Yellow: {actual_yellow_count}")
    print(f"  Correct: {np.array_equal(expected_output_grid, actual_output_grid)}")

task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 4, 4, 0, 0]
      ],
      "output": [
        [8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 4, 4, 0, 0]
      ]
    },
    {
      "input": [
        [0, 8, 0, 8, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 4, 4, 4, 0, 0],
        [0, 0, 0, 8, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [8, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 4, 4, 0, 0],
        [0, 0, 0, 8, 8, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 4, 4, 0, 0, 0, 0, 0, 0, 8],
        [0, 4, 4, 0, 0, 0, 0, 0, 0, 8]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 4, 4, 0, 0, 0, 0, 0, 0, 8],
        [0, 4, 4, 8, 8, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 4, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 0, 0, 0]
      ]
    },
      {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0],
        [8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      ]
    }
  ],
  "test": [
    {
      "input": [
        [0, 8, 0, 0, 0, 0, 4, 0],
        [0, 8, 0, 0, 0, 0, 4, 0],
        [0, 8, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [8, 0, 0, 0, 0, 0, 4, 0],
        [8, 0, 0, 0, 0, 0, 4, 0],
        [8, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}

for i, example in enumerate(task['train']):
    print(f"Example {i+1}:")
    analyze_example(example)