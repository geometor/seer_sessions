import numpy as np

def find_objects(grid, color, size=2):
    objects = []
    rows, cols = grid.shape
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            if np.all(grid[r:r+size, c:c+size] == color):
                objects.append((r, c))
    return objects

def get_stripe_bounds(col, grid_width):
    stripe_start = col
    while stripe_start >= 0 and (stripe_start % 3) != 2:
        stripe_start -= 1
    stripe_end = col
    while stripe_end < grid_width and (stripe_end % 3) != 1:
        stripe_end += 1
    return stripe_start, stripe_end

def analyze_example(input_grid, expected_output, actual_output):
    rows, cols = input_grid.shape
    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)
    all_objects = green_objects + red_objects

    print("Green Objects:", green_objects)
    print("Red Objects:", red_objects)

    for r, c in all_objects:
        color = input_grid[r,c]
        stripe_start, stripe_end = get_stripe_bounds(c, cols)
        print(f"Object at ({r}, {c}), Color: {color}, Stripe: ({stripe_start}, {stripe_end})")

    diff_expected_actual = np.where(expected_output != actual_output)
    print("Differences between Expected and Actual Output:")
    for r, c in zip(*diff_expected_actual):
        print(f"  at ({r}, {c}), Expected: {expected_output[r, c]}, Actual: {actual_output[r, c]}")

    diff_input_expected = np.where(input_grid != expected_output)
    print("Differences between Input and Expected Output:")
    for r, c in zip(*diff_input_expected):
        print(f"  at ({r}, {c}), Input: {input_grid[r, c]}, Expected: {expected_output[r, c]}")

# Example Usage (replace with actual grids)
# Assuming you have loaded the grids into variables:
# input_grid_0, expected_output_0, actual_output_0, etc.

task_id = "6b6a7a85"
examples = task.train

for i, example in enumerate(examples):
  input_grid = np.array(example.input)
  expected_output = np.array(example.output)
  actual_output = transform(input_grid) # call the function defined by the system prompt
  print(f"--- Example {i} ---")
  analyze_example(input_grid, expected_output, actual_output)