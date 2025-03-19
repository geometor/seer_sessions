import numpy as np

def analyze_grid(input_grid, output_grid, expected_output_grid):
    """Analyzes the input, output, and expected output grids."""

    rows, cols = input_grid.shape
    red_pixels = np.argwhere(input_grid == 2)
    azure_pixels = np.argwhere(input_grid == 8)
    green_pixels_output = np.argwhere(output_grid == 3)
    green_pixels_expected = np.argwhere(expected_output_grid == 3)

    analysis = {
        "grid_size": (rows, cols),
        "red_pixels": red_pixels.tolist(),
        "azure_pixels": azure_pixels.tolist(),
        "green_pixels_output": green_pixels_output.tolist(),
        "green_pixels_expected": green_pixels_expected.tolist(),
        "differences": []
    }

    #find differences
    for p in analysis["green_pixels_output"]:
      if p not in analysis["green_pixels_expected"]:
        analysis["differences"].append({"pixel":p, "type":"unexpected_output"})
    for p in analysis["green_pixels_expected"]:
      if p not in analysis["green_pixels_output"]:
        analysis["differences"].append({"pixel":p, "type":"missing_from_output"})


    return analysis

# Example data (replace with actual data from each training example)
example_data = [
    (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 8],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 3, 0, 8],
                  [0, 0, 0, 0, 0, 0, 3, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 3, 0, 8],
                  [0, 0, 0, 0, 0, 0, 3, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]),
    ),
   (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    ),
    (
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2]]),
        np.array([[0, 0, 0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 3, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 3, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2]]),
        np.array([[0, 0, 0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 3, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 3, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 2]]),
    ),
    (
        np.array([[2, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[2, 0, 0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 3, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 3, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 3]]),
        np.array([[2, 0, 0, 0, 3, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 3, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 3, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 3, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 3]]),
    )
]

results = []
for input_grid, output_grid, expected_output_grid in example_data:
    analysis = analyze_grid(input_grid, output_grid, expected_output_grid)
    results.append(analysis)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Grid Size: {result['grid_size']}")
    print(f"  Red Pixels: {result['red_pixels']}")
    print(f"  Azure Pixels: {result['azure_pixels']}")
    print(f"  Green Pixels (Output): {result['green_pixels_output']}")
    print(f"  Green Pixels (Expected): {result['green_pixels_expected']}")
    print(f"  Differences: {result['differences']}")
    print("-" * 20)
