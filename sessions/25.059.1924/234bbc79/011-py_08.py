import numpy as np

def code_execution(input_grid, output_grid, predicted_grid):
    """Analyzes the input, expected output, and predicted output grids."""

    input_pixels = {}
    output_pixels = {}
    predicted_pixels = {}

    for color in range(10):  # Check all colors
        input_pixels[color] = np.argwhere(input_grid == color).tolist()
        output_pixels[color] = np.argwhere(output_grid == color).tolist()
        predicted_pixels[color] = np.argwhere(predicted_grid == color).tolist()

    return {
        'input_pixels': input_pixels,
        'output_pixels': output_pixels,
        'predicted_pixels': predicted_pixels,
        'grid_dims': input_grid.shape,
    }

#Dummy data for example analysis, replaced with real data in actual execution
example_data = [
    {
        "input": np.array([[5, 1, 5], [2, 2, 2], [3, 3, 3]]),
        "output": np.array([[1, 1, 1], [2, 2, 2], [3, 3, 3]]),
        "predicted": np.array([[0, 1, 0], [2, 2, 2], [3, 3, 3]]),
    },
    {
        "input": np.array([[5, 5, 5, 5, 5], [5, 1, 5, 2, 5], [5, 5, 5, 5, 5]]),
        "output": np.array([[1, 1, 1, 1, 1], [1, 1, 1, 2, 1], [1, 1, 1, 1, 1]]),
        "predicted": np.array([[0, 0, 0, 0, 0], [0, 1, 0, 2, 0], [0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[5, 5, 5, 2], [1, 5, 1, 5], [5, 5, 5, 5]]),
        "output": np.array([[1, 1, 1, 2], [1, 1, 1, 1], [1, 1, 1, 1]]),
        "predicted": np.array([[0, 0, 0, 2], [1, 0, 1, 0], [0, 0, 0, 0]]),
    }

]

results = []

for ex in example_data:
  results.append(code_execution(ex['input'], ex['output'], ex['predicted']))

for i,result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Grid Dimensions: {result['grid_dims']}")
    print(f"  Input Pixels: {result['input_pixels']}")
    print(f"  Output Pixels: {result['output_pixels']}")
    print(f"  Predicted Pixels: {result['predicted_pixels']}")
    print("-" * 20)