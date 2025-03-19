import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    """Analyzes a single example and provides metrics."""

    # Find green pixels in input
    green_pixels_input = np.where(input_grid == 3)
    green_coords_input = list(zip(green_pixels_input[0], green_pixels_input[1]))

    # Find different colors in output
    magenta_pixels_output = np.where(output_grid == 6)
    blue_pixels_output = np.where(output_grid == 1)
    red_pixels_output = np.where(output_grid == 2)
    
    magenta_coords_output = list(zip(magenta_pixels_output[0], magenta_pixels_output[1]))
    blue_coords_output = list(zip(blue_pixels_output[0], blue_pixels_output[1]))
    red_coords_output = list(zip(red_pixels_output[0], red_pixels_output[1]))
   


    # Calculate bounding box for green pixels
    if green_coords_input:
        min_row = min(green_coords_input, key=lambda p: p[0])[0]
        max_row = max(green_coords_input, key=lambda p: p[0])[0]
        min_col = min(green_coords_input, key=lambda p: p[1])[1]
        max_col = max(green_coords_input, key=lambda p: p[1])[1]
        center_row = (min_row + max_row) / 2
        center_col = (min_col + max_col) / 2
    else:
        min_row, max_row, min_col, max_col, center_row, center_col = None, None, None, None, None, None

    # Check prediction accuracy
    correct_pixels = np.sum(output_grid == predicted_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0

    return {
        "green_pixels_input": green_coords_input,
        "magenta_pixels_output": magenta_coords_output,
        "blue_pixels_output": blue_coords_output,
        "red_pixels_output": red_coords_output,
        "bounding_box": {
            "min_row": min_row,
            "max_row": max_row,
            "min_col": min_col,
            "max_col": max_col,
            "center_row": center_row,
            "center_col": center_col,
        },
        "prediction_accuracy": accuracy,
    }

def calculate_metrics(task):
    results = []
    for i,example in enumerate(task['train']):
      predicted = transform(np.array(example['input']))
      results.append(analyze_example(np.array(example['input']), np.array(example['output']), predicted))
    return results

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 3, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 3, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input" : [[3,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,3]],
            "output": [[6,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,2]],
        },
        {
            "input" : [[0,0,0,3],[0,0,0,0],[0,0,0,0],[3,0,0,0]],
            "output": [[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]]
        }
    ]
}

results = calculate_metrics(task)

for i, r in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Green Pixels (Input): {r['green_pixels_input']}")
    print(f"  Magenta Pixels (Output): {r['magenta_pixels_output']}")
    print(f"  Blue Pixels (Output): {r['blue_pixels_output']}")
    print(f"  Red Pixels (Output): {r['red_pixels_output']}")
    print(f"  Bounding Box: {r['bounding_box']}")
    print(f"  Prediction Accuracy: {r['prediction_accuracy']:.4f}")
    print("-" * 30)