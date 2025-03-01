import numpy as np

def get_grid_dimensions(grid_string):
    grid = np.array(eval(grid_string))
    return grid.shape

# Example usage with the provided training data:
train_examples = [
    {
        "input": "[[0, 0, 0], [0, 2, 0], [0, 0, 0]]",
        "output": "[[0, 0, 0], [0, 2, 0], [0, 0, 0]]"
    },
    {
        "input": "[[0, 0, 0], [0, 0, 0], [0, 2, 0]]",
        "output": "[[0, 2, 0], [0, 0, 0], [0, 0, 0]]"
    },
   {
        "input": "[[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0]]",
        "output": "[[0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]"
    }
]

for i, example in enumerate(train_examples):
  input_shape = get_grid_dimensions(example["input"])
  output_shape = get_grid_dimensions(example["output"])
  print(f"Example {i+1}: Input Shape: {input_shape}, Output Shape: {output_shape}")