import numpy as np

def describe_grid(grid):
    return f"Size: {grid.shape}, Colors: {np.unique(grid)}"

def analyze_example(input_grid, output_grid, predicted_grid):
    print("Input Grid:", describe_grid(input_grid))
    print("Output Grid:", describe_grid(output_grid))
    print("Predicted Grid", describe_grid(predicted_grid))
    print("Correct Prediction", np.array_equal(output_grid,predicted_grid))
    print("---")


# Example Data (Recreated from the prompt images)
example_data = [
    (np.array([[5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5]]),
     np.array([[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]])),

     (np.array([[5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 5],
               [5, 5, 5, 5, 5, 0]]),
     np.array([[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 3]])),

    (np.array([[5, 5, 5, 5, 5, 6],
              [5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5],
              [5, 5, 5, 5, 5, 5]]),
     np.array([[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [3, 0, 0, 0]]))

]

def transform(input_grid):
    # Initialize output grid. The output dimensions are given as 4x4 in examples
    output_grid = np.zeros((4, 4), dtype=int)

    # Partition the input grid
    top_section = input_grid[:4]
    bottom_section = input_grid[4:]
    # Compare corresponding cells and update output_grid
    for i in range(4):
        for j in range(4):
            #The bottom section start with an offset of 1 row.
            if bottom_section.shape[0] > i : #make sure the offset is valid.
               if top_section[i, j] != bottom_section[i, j]:
                output_grid[i, j] = 3
               else:
                output_grid[i, j] = 0
            

    return output_grid

for input_grid, output_grid in example_data:
  predicted_grid = transform(input_grid)
  analyze_example(input_grid, output_grid, predicted_grid)