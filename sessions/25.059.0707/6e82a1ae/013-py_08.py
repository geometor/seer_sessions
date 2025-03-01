import numpy as np

def find_objects(grid, color):
    """Finds contiguous blocks of pixels of a specified color."""
    visited = set()
    objects = []

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_horizontal_line(obj):
    """Checks if an object is a horizontal line segment of length 3 or more."""
    if len(obj) < 3:
        return False
    rows = [r for r, _ in obj]
    return len(set(rows)) == 1

def is_vertical_line(obj):
    """Checks if an object is a vertical line segment of length 2."""
    if len(obj) != 2:
        return False
    cols = [c for _, c in obj]
    return len(set(cols)) == 1

def is_square(obj):
    """check if object is a 3x3 square"""

    if len(obj) != 9:
        return False

    rows = [pos[0] for pos in obj]
    cols = [pos[1] for pos in obj]

    if len(set(rows)) == 3 and len(set(cols)) == 3:
      return True
    
    return False

def distance(r1,c1,r2,c2):
    return abs(r1-r2) + abs(c1 - c2)

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find all gray objects
    gray_objects = find_objects(input_grid, 5)

    red_objects = []
    blue_objects = []

    # Determine the new color for each object
    for obj in gray_objects:
        if is_horizontal_line(obj):
            # Change to red (2)
            for r, c in obj:
                output_grid[r, c] = 2
            red_objects.append(obj)

        elif is_vertical_line(obj):
            #change to blue (1)
            for r,c in obj:
                output_grid[r, c] = 1
            blue_objects.append(obj)

        elif is_square(obj):
            for r,c in obj:
                output_grid[r,c] = 3
        

    for obj in gray_objects:

        if len(obj) == 1:
            r,c = obj[0]

            # find minimum distance from red object
            min_dist_red = 1000
            if len(red_objects) > 0:

                for red in red_objects:
                    for red_r, red_c in red:
                        dist = distance(r,c,red_r,red_c)
                        if dist < min_dist_red:
                            min_dist_red = dist


            # find minimum distance from blue object
            min_dist_blue = 1000
            if len(blue_objects) > 0:
                for blue in blue_objects:
                    for blue_r, blue_c in blue:
                        dist = distance(r,c,blue_r,blue_c)
                        if dist < min_dist_blue:
                            min_dist_blue = dist

            if min_dist_red < min_dist_blue:
                output_grid[r,c] = 3 # red + 1
            elif min_dist_blue < min_dist_red:
                output_grid[r,c] = 2 # blue + 1
            else:
                output_grid[r,c] = 2 # handles case of equal distance


    return output_grid


# Provided task examples
train_input_0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 5, 5, 5, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 5, 0, 0, 0],[0, 0, 0, 0, 0, 0, 5, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 2, 2, 2, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_input_1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 5, 5, 5, 0, 0, 0, 5, 0, 0],[0, 0, 0, 0, 0, 0, 0, 5, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 2, 2, 2, 0, 0, 0, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_input_2 = np.array([[5, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 5, 5, 5, 0, 0, 0, 5, 0, 0],[0, 0, 0, 0, 0, 0, 0, 5, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 5, 5, 5, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_2 = np.array([[3, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 2, 2, 2, 0, 0, 0, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 2, 2, 2, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_input_3 = np.array([[5, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 5, 5, 5, 0, 0, 0, 5, 5, 5],[0, 0, 0, 0, 0, 0, 0, 5, 0, 0],[0, 0, 0, 0, 0, 0, 0, 5, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[5, 5, 0, 0, 0, 0, 5, 5, 5, 0],[0, 0, 0, 0, 0, 0, 5, 0, 0, 0],[0, 0, 0, 0, 0, 0, 5, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_3 = np.array([[3, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 2, 2, 2, 0, 0, 0, 2, 2, 2],[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[1, 1, 0, 0, 0, 0, 2, 2, 2, 0],[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

def compare_grids(predicted, expected):
    """Compares two grids and returns a list of differences."""
    differences = []
    if predicted.shape != expected.shape:
        return [("Shape mismatch", predicted.shape, expected.shape)]
    for r in range(predicted.shape[0]):
        for c in range(predicted.shape[1]):
            if predicted[r, c] != expected[r, c]:
                differences.append(((r, c), predicted[r, c], expected[r, c]))
    return differences

# Perform transformations and comparisons
results = []
inputs = [train_input_0,train_input_1,train_input_2, train_input_3]
outputs = [train_output_0, train_output_1, train_output_2, train_output_3]
for i in range(len(inputs)):
  predicted_output = transform(inputs[i])
  diff = compare_grids(predicted_output, outputs[i])
  results.append(diff)

# Print the results
for i, diff in enumerate(results):
    print(f"Example {i} Differences:")
    if not diff:
        print("   No differences found.")
    else:
        for d in diff:
            print(f"   Location: {d[0]}, Predicted: {d[1]}, Expected: {d[2]}")
    print("-" * 30)