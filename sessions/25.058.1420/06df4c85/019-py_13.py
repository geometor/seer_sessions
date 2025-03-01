import numpy as np

def find_objects(grid, color, size=2):
    """Finds all 2x2 squares of a given color."""
    objects = []
    rows, cols = grid.shape
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            if np.all(grid[r:r+size, c:c+size] == color):
                objects.append((r, c))
    return objects

def get_stripe_bounds(col, grid_width):
    """Calculates the start and end columns of the yellow stripe."""
    stripe_start = col
    while stripe_start >= 0 and (stripe_start % 3) != 2:
        stripe_start -= 1
    stripe_end = col
    while stripe_end < grid_width and (stripe_end % 3) != 1:
        stripe_end += 1
    return stripe_start, stripe_end

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find green and red objects
    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)
    all_objects = green_objects + red_objects
    print(f"All objects (row, col): {all_objects}")

    # Iterate through the objects
    for r, c in all_objects:
        # find color
        color = input_grid[r,c]
        # Get stripe boundaries
        stripe_start, stripe_end = get_stripe_bounds(c, cols)
        print(f"Object at ({r}, {c}) - color {color} - stripe_start: {stripe_start}, stripe_end: {stripe_end}")

        if stripe_start < 0:
            stripe_start = 0

        # Replicate horizontally within stripe
        # First, replicate to the right
        current_col = c + 3
        while current_col <= stripe_end-1:
            output_grid[r:r+2, current_col:current_col+2] = color
            current_col += 3

        # Then, replicate to the left.
        current_col = c - 3
        while current_col >= stripe_start:
            output_grid[r:r+2, current_col:current_col+2] = color
            current_col -= 3

    return output_grid

# Example Usage (assuming you have your ARC task loaded)
# Replace this with your actual task data loading
task = {
  "train": [
    {"input": [[0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 3, 3, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 3, 3, 0, 0, 4, 0, 0, 4, 0, 0]],
     "output": [[0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0],
                [0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0],
                [0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0],
                [0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0],
                [0, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0],
                [3, 3, 3, 3, 3, 4, 0, 0, 4, 0, 0],
                [3, 3, 3, 3, 3, 4, 0, 0, 4, 0, 0]]},

    {"input": [[0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
               [0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
               [0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
               [0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
               [0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
               [0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
               [2, 2, 4, 0, 0, 4, 0, 0, 0, 0, 0],
               [2, 2, 4, 0, 0, 4, 0, 0, 0, 0, 0]],
     "output": [[0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
                [0, 0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 2, 4, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 2, 4, 0, 0, 0, 0, 0]]},

    {"input": [[0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
               [0, 0, 0, 3, 3, 4, 0, 0, 4, 0, 0],
               [0, 0, 0, 3, 3, 4, 0, 0, 4, 0, 0]],
     "output": [[0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 4, 0, 0],
                [0, 0, 0, 3, 3, 4, 0, 0, 4, 0, 0],
                [0, 0, 0, 3, 3, 4, 0, 0, 4, 0, 0]]}
  ]
}

for example in task["train"]:
    input_grid = np.array(example["input"])
    output_grid = transform(input_grid)
    print(f"Input:\n{input_grid}\n")
    print(f"Output:\n{output_grid}\n")
    print(f"Expected:\n{np.array(example['output'])}\n")
    print("-" * 20)