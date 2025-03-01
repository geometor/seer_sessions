import numpy as np

def describe_grid(grid, grid_name):
    """Provides a description of the grid, including dimensions and pixel counts."""
    shape = grid.shape
    unique, counts = np.unique(grid, return_counts=True)
    pixel_counts = dict(zip(unique, counts))
    print(f"{grid_name}:")
    print(f"  Dimensions: {shape}")
    print(f"  Pixel Counts: {pixel_counts}")
    
def compare_grids(grid1, grid2):
    """Compares two grids and prints elements where they differ."""
    
    if grid1.shape != grid2.shape:
       print("Grids have different dimensions")
       return
       
    diff = grid1 != grid2
    
    if not np.any(diff):
       print("Grids are equal")
       return

    indices = np.where(diff)
    
    print("Different values")
    for i in range(len(indices[0])):
      x = indices[0][i]
      y = indices[1][i]
      
      print(f"  location {x,y} values: input {grid1[x,y]} output {grid2[x,y]}")
    

def show_grid(grid, title="Grid"):
    """
    Displays a grid-like representation of a NumPy array with coordinates.
    """
    print(f"{title}:")
    
    # Print column headers (y-coordinates)
    print("   " + "  ".join([str(i).rjust(2) for i in range(grid.shape[1])]))

    for i, row in enumerate(grid):
        # Print row header (x-coordinate)
        print(str(i).rjust(2), end=" ")
        
        # Print row values
        print(" ".join([str(val).rjust(2) for val in row]))
    print()

# Example Data (Assuming these are loaded from the task)
example_inputs = [
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),

    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 2, 2, 2, 0, 0],
              [0, 0, 0, 2, 0, 0, 2, 0, 0],
              [0, 0, 0, 2, 2, 2, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]])
]

example_outputs = [
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 2, 2, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 4, 4, 4, 0, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 4, 4, 4, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 4, 4, 4, 4, 0, 0],
              [0, 0, 0, 2, 0, 0, 2, 0, 0],
              [0, 0, 0, 4, 4, 4, 4, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]])
]

transformed_outputs = [transform(input_grid) for input_grid in example_inputs]

# Analyze each example
for i in range(len(example_inputs)):
  describe_grid(example_inputs[i], f"Example {i+1} Input")
  describe_grid(example_outputs[i], f"Example {i+1} Output")
  describe_grid(transformed_outputs[i], f"Example {i+1} Transformed")
  compare_grids(example_outputs[i], transformed_outputs[i])
  print("-" * 30)