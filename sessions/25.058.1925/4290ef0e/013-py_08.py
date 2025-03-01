import numpy as np

# Provided transform function and helper functions (find_target_pixels)
def find_target_pixels(grid):
    """Finds all pixels that are not azure (color 8) and returns their coordinates and colors."""
    rows, cols = grid.shape
    target_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 8:
                target_pixels.append(((r, c), grid[r, c]))
    return target_pixels

def transform(input_grid):
    # Find target pixels (non-azure pixels).
    target_pixels = find_target_pixels(input_grid)

    # initialize output_grid
    output_grid = np.zeros((7, 7), dtype=int)


    # If only one target pixel color, place it in the bottom-right corner.
    if len(set(color for _, color in target_pixels)) == 1:
      if len(target_pixels) > 0:
        output_grid[6, 6] = target_pixels[0][1]

    # handle more than one target pixel color
    elif len(target_pixels) > 1:
        # get the coordinates of the target pixels
        coords = [coord for coord, _ in target_pixels]
        # calculate row and col min/max
        min_r = min(r for r, _ in coords)
        max_r = max(r for r, _ in coords)
        min_c = min(c for _, c in coords)
        max_c = max(c for _, c in coords)

        # calculate the size of the area to copy
        height = max_r - min_r + 1
        width = max_c - min_c + 1

        # if we can fit the identified rectangle, copy it
        if height <= 7 and width <=7:
            for (r,c), color in target_pixels:
                # shift the input to the output grid
                output_grid[r-min_r, c-min_c] = color
        else: # fallback: find pixel farthest down and right
          # find bottom-right most pixel by sorting by row and then by column
          target_pixels.sort(key=lambda item: (item[0][0], item[0][1]), reverse=True)
          output_grid[6,6] = target_pixels[0][1]

    return output_grid
# Example data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 0, 8, 8]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8]]),
        "output": np.array([[8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8],
                            [8, 8, 8, 8, 8, 8, 8]])
    },
    {
        "input": np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8, 8, 1]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1]])
    },
]

for i, example in enumerate(examples):
    input_grid = example["input"]
    expected_output = example["output"]
    target_pixels = find_target_pixels(input_grid)
    unique_colors = set(color for _, color in target_pixels)
    transformed_output = transform(input_grid)
    correct = np.array_equal(transformed_output, expected_output)

    print(f"Example {i+1}:")
    print(f"  Input Dimensions: {input_grid.shape}")
    print(f"  Target Pixels: {target_pixels}")
    print(f"  Unique Target Colors: {unique_colors}")
    print(f"  Transformed Output Correct: {correct}")
    # if not correct:
    #   print("Transformed Output:\n", transformed_output)
    #   print("Expected Output:\n", expected_output)
    print("-" * 20)