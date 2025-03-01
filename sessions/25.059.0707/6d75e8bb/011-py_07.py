import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    """Analyzes a single example, comparing output and predicted grids."""

    # Convert to numpy arrays for easier manipulation
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_grid = np.array(predicted_grid)

    # 1. Find the azure region in the input
    azure_pixels = np.where(input_grid == 8)
    if azure_pixels[0].size == 0:  # No azure pixels
        return {
            "azure_region_exists": False,
            "red_pixels_added": False,
            "prediction_correct": np.array_equal(output_grid, predicted_grid)
        }

    azure_region_exists = True
    min_row, min_col = np.min(azure_pixels[0]), np.min(azure_pixels[1])
    max_row, max_col = np.max(azure_pixels[0]), np.max(azure_pixels[1])
    azure_height = max_row - min_row + 1
    azure_width = max_col - min_col + 1

    # 2. Find red pixels in the output
    red_pixels_output = np.where(output_grid == 2)
    red_pixels_added = red_pixels_output[0].size > 0

    #3. Find red pixels in predicted grid
    red_pixels_predicted = np.where(predicted_grid == 2)

    # 4. Check if the prediction is correct
    prediction_correct = np.array_equal(output_grid, predicted_grid)


    # 5. Relative position of red pixels within the azure region (output)
    relative_red_positions_output = []
    if red_pixels_added:
        for r, c in zip(red_pixels_output[0], red_pixels_output[1]):
            relative_red_positions_output.append((r - min_row, c - min_col))


    # 6. Relative position of incorrectly predicted pixels
    incorrect_red_additions = []
    incorrect_red_omissions = []

    for r, c in zip(red_pixels_predicted[0], red_pixels_predicted[1]):
        if output_grid[r,c] != 2:
            incorrect_red_additions.append((r - min_row, c - min_col))
    
    for r, c in zip(red_pixels_output[0], red_pixels_output[1]):
        if predicted_grid[r,c] != 2:
            incorrect_red_omissions.append((r - min_row, c-min_col))

    return {
        "azure_region_exists": azure_region_exists,
        "azure_top_left": (min_row, min_col),
        "azure_height": azure_height,
        "azure_width": azure_width,
        "red_pixels_added": red_pixels_added,
        "relative_red_positions_output": relative_red_positions_output,
        "prediction_correct": prediction_correct,
        "incorrect_red_additions": incorrect_red_additions,
        "incorrect_red_omissions": incorrect_red_omissions
    }

# Example Usage with the provided data (replace with your actual data)
train_data = [
   ([
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 8, 8, 8, 8, 8, 0, 0],
      [0, 0, 8, 8, 8, 8, 8, 0, 0],
      [0, 0, 8, 8, 8, 8, 8, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 8, 8, 8, 2, 8, 0, 0],
      [0, 0, 8, 8, 2, 2, 8, 0, 0],
      [0, 0, 2, 8, 2, 8, 8, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 8, 8, 8, 2, 8, 0, 0],
      [0, 0, 8, 8, 2, 2, 8, 0, 0],
      [0, 0, 2, 8, 2, 8, 8, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]),
   ([
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 0, 0, 0],
      [0, 0, 0, 8, 8, 8, 0, 0],
      [0, 0, 0, 8, 8, 8, 0, 0],
      [0, 0, 0, 8, 8, 8, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 0, 0, 0],
      [0, 0, 0, 8, 2, 8, 0, 0],
      [0, 0, 0, 8, 2, 8, 0, 0],
      [0, 0, 0, 8, 8, 8, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
      [0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 0, 0, 0],
      [0, 0, 0, 8, 2, 8, 0, 0],
      [0, 0, 0, 2, 2, 8, 0, 0],
      [0, 0, 0, 8, 8, 8, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0],
    ]),
   ([
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 2, 2, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    [
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 2, 2, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 2, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]),
   ([
      [8, 8, 8, 8],
      [8, 8, 8, 8],
      [8, 8, 8, 8],
      [8, 8, 8, 8]
    ],
    [
      [8, 8, 8, 8],
      [8, 2, 2, 8],
      [8, 8, 8, 8],
      [8, 8, 8, 8]
    ],
    [
      [8, 8, 8, 8],
      [8, 2, 2, 8],
      [8, 8, 2, 8],
      [8, 8, 8, 8]
    ])
]


results = [analyze_example(inp, outp, pred) for inp, outp, pred in train_data]

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    for key, value in res.items():
        print(f"  {key}: {value}")
    print("-" * 20)