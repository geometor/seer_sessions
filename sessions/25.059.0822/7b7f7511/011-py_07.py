import numpy as np

def describe_grid(grid, grid_name):
    """Provides dimensions and a sample of pixel values for a grid."""
    dims = grid.shape
    print(f"{grid_name} Dimensions: {dims}")
    #sample some pixels
    if (dims[0] > 2 and dims[1] > 2):
        print(f"{grid_name} Top Left 3x3:\n{grid[:3, :3]}")
        print(f"{grid_name} Bottom Right 3x3:\n{grid[-3:, -3:]}")
    elif (dims[0] > 1 and dims[1] > 1):
        print(f"{grid_name} Top Left 2x2:\n{grid[:2, :2]}")
        print(f"{grid_name} Bottom Right 2x2:\n{grid[-2:, -2:]}")
    else:
        print(f"{grid_name}: {grid}")
    

examples = [
    (np.array([[7, 7, 7, 7, 7, 7],
               [7, 7, 7, 7, 7, 7],
               [7, 7, 7, 7, 7, 7],
               [7, 7, 7, 7, 7, 7],
               [7, 7, 7, 7, 7, 7],
               [7, 7, 7, 7, 7, 7]]),
     np.array([[7, 7, 7],
               [7, 7, 7],
               [7, 7, 7],
               [7, 7, 7],
               [7, 7, 7],
               [7, 7, 7]])),
    (np.array([[3, 3, 3, 3, 0, 0, 0, 0],
               [3, 3, 3, 3, 0, 0, 0, 0],
               [3, 3, 3, 3, 0, 0, 0, 0],
               [3, 3, 3, 3, 0, 0, 0, 0],
               [5, 5, 5, 5, 1, 1, 1, 1],
               [5, 5, 5, 5, 1, 1, 1, 1],
               [5, 5, 5, 5, 1, 1, 1, 1],
               [5, 5, 5, 5, 1, 1, 1, 1]]),
     np.array([[3, 3, 0, 0],
               [3, 3, 0, 0],
               [3, 3, 0, 0],
               [3, 3, 0, 0],
               [5, 5, 1, 1],
               [5, 5, 1, 1],
               [5, 5, 1, 1],
               [5, 5, 1, 1]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
     np.array([[8, 8, 8, 8, 8],
               [8, 8, 8, 8, 8],
               [8, 8, 8, 8, 8],
               [8, 8, 8, 8, 8],
               [8, 8, 8, 8, 8],
               [8, 8, 8, 8, 8]]))
]

for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i + 1}:")
    describe_grid(input_grid, "Input Grid")
    describe_grid(output_grid, "Output Grid")
    print("-" * 20)