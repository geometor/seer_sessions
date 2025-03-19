import numpy as np

def code_execution(input_grid, output_grid, predicted_grid):
    """
    Calculates and prints the difference grid between predicted and expected output.
    Also prints dimensions and seed location.
    """

    input_array = np.array(input_grid)
    output_array = np.array(output_grid)
    predicted_array = np.array(predicted_grid)

    difference_grid = np.where(output_array != predicted_array, 1, 0)  # Highlight differences

    print("Input Dimensions:", input_array.shape)
    print("Output Dimensions:", output_array.shape)
    print("Difference Grid:")
    print(difference_grid)
    #find the seed
    seed_x, seed_y = find_pixel(input_array, 1)
    print("seed coordinates: ", seed_x, seed_y)
    
    
def find_pixel(grid, color):
    # Find the coordinates of a specific color pixel.
    for y, row in enumerate(grid):
        for x, pixel in enumerate(row):
            if pixel == color:
                return x, y
    return None

# dummy grids since actual data not available in this turn
example_data = [
  {
    "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
    "output": [[8, 8, 8, 8, 1, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 1, 8, 8, 8, 8, 8],
              [1, 1, 1, 1, 8, 1, 1, 1, 1, 1],
              [8, 8, 8, 8, 1, 8, 8, 8, 8, 8]],
       "predicted": [[8, 8, 8, 8, 1, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 1, 8, 8, 8, 8, 8],
                    [1, 1, 1, 1, 8, 1, 1, 1, 1, 1],
                    [8, 8, 8, 8, 1, 8, 8, 8, 8, 8]]
  },
  {
    "input": [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]],
    "output": [[8, 8, 8, 8, 1, 8, 8, 8],
              [8, 8, 8, 8, 8, 8, 8, 8],
              [8, 8, 8, 8, 1, 8, 8, 8],
              [8, 8, 8, 8, 1, 8, 8, 8],
              [8, 8, 8, 8, 1, 8, 8, 8],
              [8, 8, 8, 8, 1, 8, 8, 8]],
     "predicted": [[8, 8, 8, 8, 1, 8, 8, 8],
                    [1, 1, 1, 1, 1, 1, 1, 1],
                    [8, 8, 8, 8, 1, 8, 8, 8],
                    [8, 8, 8, 8, 1, 8, 8, 8],
                    [8, 8, 8, 8, 1, 8, 8, 8],
                    [8, 8, 8, 8, 1, 8, 8, 8]],
  },
   {
    "input": [[0, 0, 0, 0, 0, 0,],
              [0, 0, 0, 1, 0, 0,],
              [0, 0, 0, 0, 0, 0,],
              [0, 0, 0, 0, 0, 0,]],
    "output": [[8, 8, 8, 1, 8, 8],
              [8, 8, 8, 8, 8, 8],
              [8, 8, 8, 1, 8, 8],
              [8, 8, 8, 1, 8, 8]],
       "predicted":  [[8, 8, 8, 1, 8, 8],
                     [1, 1, 1, 1, 1, 1],
                     [8, 8, 8, 1, 8, 8],
                     [8, 8, 8, 1, 8, 8]]
  },
     {
    "input": [[0, 1, 0, 0,],
              [0, 0, 0, 0,],
              [0, 0, 0, 0,],],
    "output": [[8, 8, 8, 8],
              [8, 1, 8, 8,],
              [8, 1, 8, 8,],],
       "predicted":  [[8, 1, 8, 8],
                    [8, 8, 8, 8],
                    [8, 1, 8, 8]]
  },
]

for example in example_data:
  code_execution(example["input"], example["output"], example["predicted"])
  print("-" * 20)