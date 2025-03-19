import numpy as np

def describe_grid(grid):
    """Describes a grid by listing non-zero pixel locations and colors."""
    description = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] != 0:
                description.append(f"Pixel at ({i}, {j}) is color {grid[i, j]}")
    return description
                
# Example Data (Replace with actual data from the task)

example_data = [
  {
      "input": np.array([[0,0,0],[0,1,0],[0,0,0]]),
      "output": np.array([[0,0,0],[0,1,1],[0,1,1]])
  },
    {
      "input": np.array([[0,0,0,0],[0,0,5,0],[0,0,0,0],[0,0,0,0]]),
      "output": np.array([[0,0,0,0],[0,0,5,5],[0,0,5,5],[0,0,0,0]])
    },
    {
       "input": np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,3,0],[0,0,0,0,0],[0,0,0,0,0]]),
       "output": np.array([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,3,3],[0,0,0,3,3],[0,0,0,0,0]])
    },
    {
       "input": np.array([[0,2,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]),
       "output": np.array([[0,2,2,0],[0,2,2,0],[0,0,0,0],[0,0,0,0]])
    }
]

for i, example in enumerate(example_data):
    print(f"Example {i+1}:")
    print("Input Description:")
    print(describe_grid(example["input"]))
    print("Output Description:")
    print(describe_grid(example["output"]))
    print("-" * 20)
