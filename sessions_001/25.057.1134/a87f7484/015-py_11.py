import numpy as np

def report(grid):
    colors = set(np.unique(grid).tolist())
    rows, cols = grid.shape
    print(f"  - Dimensions: {rows}x{cols}")
    print(f"  - Colors: {colors}")

def find_object_by_color(grid, color):
    coords = np.argwhere(grid == color)
    return coords

def get_bounding_box(coords):
    if len(coords) == 0:  # Handle empty coords
        return 0, 0, -1, -1 #empty grid
    min_y, min_x = np.min(coords, axis=0)
    max_y, max_x = np.max(coords, axis=0)
    return min_y, min_x, max_y, max_x

def extract_subgrid(grid, bounding_box):
  min_y, min_x, max_y, max_x = bounding_box
  return grid[min_y:max_y+1, min_x:max_x+1]

examples = [
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 0, 0, 0, 4, 0, 0, 0, 8],
                           [8, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[0, 0, 0],
                            [0, 4, 0],
                            [0, 0, 0]])
    },
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 8, 0, 0, 0, 0, 4, 0, 0, 0, 8],
                           [8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[0, 0, 0],
                            [0, 4, 0],
                            [0, 0, 0]])
    },
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 0, 0, 0, 4, 0, 0, 0, 0, 8],
                           [8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 0, 0, 0, 0, 0, 0, 4, 0, 8],
                           [8, 0, 0, 0, 0, 0, 0, 0, 0, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[4, 0, 0],
                            [0, 0, 0],
                            [0, 0, 4]])
    },
        {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8],
                           [8, 0, 0, 0, 0, 0, 8],
                           [8, 0, 4, 0, 0, 0, 8],
                           [8, 0, 0, 0, 0, 0, 8],
                           [8, 0, 0, 0, 0, 0, 8],
                           [8, 8, 8, 8, 8, 8, 8]]),
        "output": np.array([[4]])
    },

]

for i, example in enumerate(examples):
    input_grid = example["input"]
    output_grid = example["output"]
    predicted = transform(input_grid)

    print(f"Example {i+1}:")
    print("Input:")
    report(input_grid)
    print("Expected Output:")
    report(output_grid)
    print("Predicted:")
    report(predicted)

    yellow_coords = find_object_by_color(input_grid, 4)
    bounding_box = get_bounding_box(yellow_coords)
    expected_bb = get_bounding_box(find_object_by_color(output_grid, 4))
    print(f"  - Yellow Bounding Box (Input): {bounding_box}")
    print(f"  - Yellow Bounding Box (output): {expected_bb}")
    correct = np.array_equal(predicted,output_grid)    
    print(f"  - Correct: {correct}")
    print("-" * 20)