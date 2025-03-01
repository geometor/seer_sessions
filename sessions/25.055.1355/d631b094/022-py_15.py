import numpy as np

# Define the transform function (from the provided code)
def transform(input_grid):
    azure_count = np.sum(input_grid == 8)
    output_grid = np.full((1, azure_count), 8)
    return output_grid

# Helper function to describe grid
def describe_grid(grid, grid_name):
    print(f"Describing {grid_name}:")
    print(f"  Dimensions: {grid.shape}")
    print(f"  Azure pixel count: {np.sum(grid == 8)}")
    for i in range(10):
        count = np.sum(grid == i)
        if count: print(f'  color {i} count: {count}')
    print()


# Input and Output examples (from provided data)
train_in_0 = np.array([[8, 1, 1, 1, 1, 1, 1, 8, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]])
train_out_0 = np.array([[8, 8]])
train_in_1 = np.array([[8, 1, 1, 1, 1, 1, 1, 1, 8], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]])
train_out_1 = np.array([[8, 8]])
train_in_2 = np.array([[1, 1, 1, 8, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 8]])
train_out_2 = np.array([[8, 8]])
train_in_3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8]])
train_out_3 = np.array([[8, 8, 8, 8, 8, 8]])
train_in_4 = np.array([[1, 1, 1, 8, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 8, 1, 1, 1, 1], [8, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 8, 1, 1, 1, 1, 1]])
train_out_4 = np.array([[8, 8, 8, 8]])

inputs = [train_in_0,train_in_1,train_in_2,train_in_3,train_in_4]
outputs = [train_out_0,train_out_1,train_out_2,train_out_3,train_out_4]

for i in range(len(inputs)):
  print(f'Example {i}')
  describe_grid(inputs[i],'input')
  describe_grid(outputs[i],'output')
  predicted_output = transform(inputs[i])
  describe_grid(predicted_output,'predicted')
  print('-' * 20)