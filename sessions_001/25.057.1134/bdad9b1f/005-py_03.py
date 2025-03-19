import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1]
                or visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] != 0:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append(obj)
    return objects

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Copy and extend objects
    for obj in objects:
        first_pixel = obj[0]
        color = input_grid[first_pixel]

        # if is a horizontal object
        is_horizontal = all(pixel[0] == first_pixel[0] for pixel in obj)

        if is_horizontal:
          #copy the horizontal object
          for r,c in obj:
            output_grid[r,c] = input_grid[r,c]

          #start extending it.
          row = first_pixel[0]
          col = obj[-1][1] #last pixel to start extending
          while col+1 < output_grid.shape[1]:
            col = col + 1
            if input_grid[row,col] != 0 and input_grid[row,col]!=color:
              output_grid[row,col-1]=4 #meeting point color
              break;
            else:
              output_grid[row,col]=color

        else:
          #copy other object type
          for r,c in obj:
            output_grid[r,c] = input_grid[r,c]
          
    return output_grid

def analyze_results(input_grid, output_grid, predicted_grid):
    correct = np.array_equal(output_grid, predicted_grid)
    diff_pixels = np.sum(output_grid != predicted_grid)
    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)
    predicted_objects = find_objects(predicted_grid)

    print(f"Correct: {correct}")
    print(f"Number of differing pixels: {diff_pixels}")
    print(f"Input objects: {len(input_objects)}")
    print(f"Output objects: {len(output_objects)}")
    print(f"Predicted objects: {len(predicted_objects)}")
    print("Input Objects:")
    for i, obj in enumerate(input_objects):
        color = input_grid.flat[np.ravel_multi_index(np.array(obj).T, input_grid.shape)]
        print(f"  Object {i+1}: Color={color[0]}, Size={len(obj)}, is_horizontal={all(o[0] == obj[0][0] for o in obj)}")


# Example Usage (replace with actual task data)
#These are hardcoded for simplicty
task_examples = [
   {
    "input":  np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]]),
    "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 1, 1, 1, 4, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]])
   },
   {
    "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                       [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                       [1, 1, 1, 1, 1, 4, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
   },
   {
    "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 3, 3, 3, 3, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 2, 0]]),
    "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 3, 3, 3, 3, 4, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 2, 0]])
   },
   {
    "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 7, 7, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 3, 0, 0, 0, 0, 0]]),
    "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 7, 7, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 3, 0, 0, 0, 0, 0]])
   }

]


for i, example in enumerate(task_examples):
  input_grid = example["input"]
  output_grid = example["output"]
  predicted_grid = transform(input_grid)

  print(f"----- Example {i+1} -----")
  analyze_results(input_grid, output_grid, predicted_grid)
  print("\n")