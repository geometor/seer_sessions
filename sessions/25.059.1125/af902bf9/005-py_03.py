import numpy as np

def find_pixels_by_value(grid, value):
    """Finds coordinates of pixels with a specific value."""
    return np.argwhere(grid == value)

def calculate_center(coordinates):
    """Calculates the center point of a rectangle given corner coordinates."""
    return np.mean(coordinates, axis=0).astype(int)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find corner pixels (value 4)
    corner_pixels = find_pixels_by_value(input_grid, 4)

    # Calculate center point
    if len(corner_pixels) > 0: # handle empty corner case
        center_point = calculate_center(corner_pixels)

        # Add center pixel (value 2)
        output_grid[center_point[0], center_point[1]] = 2

    return output_grid

def show_grid(grid, title=None):
  if title is not None:
    print(title)
  for row in grid:
    print("".join(str(int(cell)) for cell in row))

task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 2, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ],
  "test": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 4, 4, 4, 4, 4, 0],
        [0, 4, 0, 0, 0, 4, 0],
        [0, 4, 0, 0, 0, 4, 0],
        [0, 4, 4, 4, 4, 4, 0],
        [0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 4, 4, 4, 4, 4, 0],
        [0, 4, 0, 0, 0, 4, 0],
        [0, 4, 0, 0, 0, 4, 0],
        [0, 4, 4, 4, 4, 4, 0],
        [0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}

def assess_example(example):
    input_grid = np.array(example['input'])
    expected_output_grid = np.array(example['output'])
    actual_output_grid = transform(input_grid)
    
    yellow_pixels_input = find_pixels_by_value(input_grid, 4)
    yellow_pixels_expected = find_pixels_by_value(expected_output_grid, 4)
    red_pixels_expected = find_pixels_by_value(expected_output_grid, 2)


    print("Input:")
    show_grid(input_grid)

    print("\nExpected Output:")
    show_grid(expected_output_grid)
    
    print("\nActual Output:")
    show_grid(actual_output_grid)
    
    print("\nYellow Pixels (Input):", yellow_pixels_input)
    print("Yellow Pixels (Expected Output):", yellow_pixels_expected)
    print("Red Pixels (Expected Output):", red_pixels_expected)

    
    correct = np.array_equal(expected_output_grid, actual_output_grid)    
    print("\nCorrect:", correct)

    if not correct:
        diff = expected_output_grid - actual_output_grid
        print("\nDifferences (Expected - Actual):")
        show_grid(diff)

    print("-" * 30)
    return correct


print("TRAIN EXAMPLES")
train_results = [assess_example(example) for example in task['train']]

print("\nTEST EXAMPLES")
test_results = [assess_example(example) for example in task['test']]