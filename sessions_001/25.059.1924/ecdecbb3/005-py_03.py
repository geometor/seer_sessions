import numpy as np

def get_grid_string(grid):
  return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

def compare_grids(grid1, grid2):
    """Compares two grids and returns a grid showing the differences."""
    diff_grid = np.zeros_like(grid1)
    for i in range(grid1.shape[0]):
        for j in range(grid1.shape[1]):
            if grid1[i, j] != grid2[i, j]:
                diff_grid[i, j] = 1  # Mark differences with 1
    return diff_grid

def show_example(task, index):
    input_grid = np.array(task['train'][index]['input'])
    expected_output = np.array(task['train'][index]['output'])
    predicted_output = transform(input_grid.copy())

    diff_grid = compare_grids(expected_output, predicted_output)
    
    print(f"Example {index + 1}:")
    print("Input:")
    print(get_grid_string(input_grid))
    print("Expected Output:")
    print(get_grid_string(expected_output))
    print("Predicted Output:")
    print(get_grid_string(predicted_output))
    print("Difference grid")
    print(get_grid_string(diff_grid))

# show results for training examples
task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 2, 0, 2, 0, 0, 2, 0, 0],
        [0, 2, 0, 2, 0, 0, 2, 0, 0],
        [0, 2, 0, 2, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 0, 0, 2, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 8, 2, 8, 0, 0, 0],
        [0, 0, 0, 8, 8, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 2, 2, 2, 0, 0, 0]
      ]
    }
    ,
        {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 8, 8, 8, 8, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 2, 2, 2, 0]
      ]
    }
  ]
}

for i in range(len(task["train"])):
  show_example(task, i)