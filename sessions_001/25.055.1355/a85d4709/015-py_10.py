import numpy as np

def describe_grid(grid):
    """Provides a basic description of the grid."""
    rows, cols = grid.shape
    print(f"Grid Dimensions: {rows} x {cols}")
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print(f"Color Counts: {color_counts}")


def get_pixel(grid, r, c):
    """Safely gets a pixel value, handling out-of-bounds."""
    rows, cols = grid.shape
    if 0 <= r < rows and 0 <= c < cols:
        return grid[r, c]
    else:
        return None

train_examples = [
    {
        'input': np.array([[5, 0, 5], [0, 5, 0], [5, 0, 5]]),
        'output': np.array([[2, 2, 2], [2, 4, 2], [2, 2, 2]])
    },
    {
        'input': np.array([[0, 5, 0], [5, 5, 5], [0, 5, 0]]),
        'output': np.array([[2, 2, 2], [2, 4, 2], [2, 2, 2]])
    },
    {
      'input':  np.array([[5, 5, 5, 5, 5, 5, 5, 5, 0], [5, 5, 5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
      'output': np.array([[2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2]])
    }
]

for i, example in enumerate(train_examples):
    print(f"--- Example {i+1} ---")
    print("Input:")
    describe_grid(example['input'])
    print("Output:")
    describe_grid(example['output'])
    print("\n")

    # Example-specific checks can go here (if needed)
    # For instance, check specific pixel locations
    # print(f"Input center pixel: {get_pixel(example['input'], 1, 1)}")
    # print(f"Output center pixel: {get_pixel(example['output'], 1, 1)}")

    predicted_output = transform(example['input'])
    if np.array_equal(predicted_output, example['output']):
        print("Prediction: CORRECT")
    else:
        print("Prediction: INCORRECT")
        print("Predicted Output:")
        print(predicted_output)
