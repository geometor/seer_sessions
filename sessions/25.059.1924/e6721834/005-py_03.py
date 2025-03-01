def describe_grid(grid):
    """Provides a basic description of a grid."""
    grid = np.array(grid)
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    print(f"  Dimensions: {rows}x{cols}")
    print(f"  Unique Colors: {list(unique_colors)}")
    # rudimentary region check.
    if rows > 1:
        top_left = grid[0,0]
        top_right = grid[0,-1]
        bottom_left = grid[-1,0]
        bottom_right = grid[-1, -1]

        print(f"Top left color: {top_left}")
        print(f"Top right color: {top_right}")
        print(f"Bottom left color: {bottom_left}")
        print(f"Bottom right color: {bottom_right}")
        if np.all(grid[0] == top_left) :
            print ("Top row is all the same color")
        if np.all(grid[-1] == bottom_left):
            print("Bottom row is all the same color")

train = task["train"]
test = task["test"]

for i, example in enumerate(train):
  print(f"Example Input {i+1}:")
  describe_grid(example["input"])
  print(f"Example Output {i+1}:")
  describe_grid(example["output"])
  print("-----")