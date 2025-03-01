import numpy as np

# (Code from previous turn - get_regions, expand_region, transform, etc. pasted here for execution)

def get_regions(grid, colors):
    # find regions of specific colors in a grid
    regions = {}
    for color in colors:
        regions[color] = []
        visited = np.zeros_like(grid, dtype=bool)
        rows, cols = grid.shape
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color and not visited[r, c]:
                    region = []
                    stack = [(r, c)]
                    while stack:
                        row, col = stack.pop()
                        if 0 <= row < rows and 0 <= col < cols and grid[row, col] == color and not visited[row, col]:
                            visited[row, col] = True
                            region.append((row, col))
                            stack.extend([(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)])
                    regions[color].append(region)
    return regions

def expand_region_horizontally_with_boundary(grid, region, color):
    # expand each region horizontally until any non-white boundary, consider height
    min_y = min(r[0] for r in region)
    max_y = max(r[0] for r in region)
    min_x = min(r[1] for r in region)
    max_x = max(r[1] for r in region)

    # Find leftmost expansion limit (any non-white pixel)
    left_limit = 0
    for x in range(min_x - 1, -1, -1):
        if any(grid[y,x] != 0 for y in range(grid.shape[0])): #check entire column
            left_limit = x+1
            break

    # Find rightmost expansion limit (any non-white pixel)
    right_limit = grid.shape[1] - 1
    for x in range(max_x + 1, grid.shape[1]):
        if any(grid[y,x] != 0 for y in range(grid.shape[0])):  # Check entire column
           right_limit = x-1
           break
    
    # Check if expansion would make region height >1, if yes, expand entire height
    expand_full_height = False
    if (max_y - min_y +1) > 0:  # original had height = 1
          # check if any pixel in the expanded region has an occupied pixel above or below
          for x in range(left_limit, right_limit + 1):
              for y in range(grid.shape[0]):
                  if y < min_y or y > max_y:
                      if any(grid[y, x_check] !=0 for x_check in range(left_limit, right_limit+1)):
                          expand_full_height = True
                          break
              if expand_full_height:
                  break

    # Expand, either full height or the region's original y-coordinates
    for y in range(0 if expand_full_height else min_y, grid.shape[0] if expand_full_height else max_y + 1):  # Iterate through rows
        for x in range(left_limit, right_limit + 1):
             grid[y,x] = color
    return grid

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)


    # Identify Regions of blue and yellow.
    regions = get_regions(input_grid, [1, 4])


    # expand blue regions
    for region in regions[1]:
        output_grid = expand_region_horizontally_with_boundary(output_grid, region, 1)

    # expand yellow regions
    for region in regions[4]:
        output_grid = expand_region_horizontally_with_boundary(output_grid, region, 4)


    return output_grid.tolist()

# Define the training examples (replace with actual data from the task)
train_pairs = [
    ([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     ],
     [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 4, 4, 4, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
     ]),
    ([
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 4, 4, 4, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 4, 4, 4, 4, 4, 4, 4, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
    ([
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
       [0, 0, 0, 0, 4, 4, 4, 4, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ],
    [
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
       [4, 4, 4, 4, 4, 4, 4, 4, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
]


# Run the transformation on each example and check for errors
for i, (input_grid, expected_output) in enumerate(train_pairs):
    predicted_output = transform(input_grid)
    if predicted_output != expected_output:
        print(f"Example {i+1}: Error")
        print("Input:\n", np.array(input_grid))
        print("Expected Output:\n", np.array(expected_output))
        print("Predicted Output:\n", np.array(predicted_output))
    else:
        print(f"Example {i+1}: Success")