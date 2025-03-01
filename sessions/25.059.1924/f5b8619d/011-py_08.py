import numpy as np

def describe_grid(grid):
    shape = grid.shape
    unique_colors = np.unique(grid)
    return f"Shape: {shape}, Unique Colors: {unique_colors}"

# Example Data (assuming this is available in a structured format)
examples = [
  {
        "input": np.array([[5]]),
        "output": np.array([[0, 0, 0, 0, 0],
       [0, 8, 8, 8, 0],
       [0, 8, 5, 8, 0],
       [0, 8, 8, 8, 0],
       [0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[5, 5], [5, 5]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
       [0, 8, 8, 8, 8, 8, 0],
       [0, 8, 5, 8, 5, 8, 0],
       [0, 8, 8, 8, 8, 8, 0],
       [0, 8, 5, 8, 5, 8, 0],
       [0, 8, 8, 8, 8, 8, 0],
       [0, 0, 0, 0, 0, 0, 0]])
    },
   {
        "input": np.array([[5, 5, 5], [5, 5, 5], [5, 5, 5]]),
        "output": np.array( [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0],
        [0, 8, 5, 8, 5, 8, 5, 8, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0],
        [0, 8, 5, 8, 5, 8, 5, 8, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0],
        [0, 8, 5, 8, 5, 8, 5, 8, 0],
        [0, 8, 8, 8, 8, 8, 8, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    }
]

for i, example in enumerate(examples):
    input_desc = describe_grid(example['input'])
    output_desc = describe_grid(example['output'])
    print(f"Example {i+1}:")
    print(f"  Input: {input_desc}")
    print(f"  Output: {output_desc}")