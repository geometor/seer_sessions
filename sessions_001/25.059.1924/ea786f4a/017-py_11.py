import numpy as np

def get_report(input_grid, output_grid, predicted_grid):
    correct_pixels = np.sum(output_grid == predicted_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels
    return {
        "correct_pixels": int(correct_pixels),
        "total_pixels": int(total_pixels),
        "accuracy": float(accuracy),
    }

# Example Data (Replace with actual ARC grid data)
example_inputs = [
    np.array([
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 1, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5]
]),
    np.array([
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 3, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5]
]),
     np.array([
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 8, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5]
]),
]
example_outputs = [
     np.array([
    [5, 5, 5, 1, 5, 5, 5],
    [5, 5, 5, 1, 5, 5, 5],
    [5, 5, 5, 1, 5, 5, 5],
    [1, 1, 1, 1, 1, 1, 1],
    [5, 5, 5, 1, 5, 5, 5],
    [5, 5, 5, 1, 5, 5, 5],
    [5, 5, 5, 1, 5, 5, 5]
]),
    np.array([
    [5, 5, 5, 3, 5, 5, 5],
    [5, 5, 5, 3, 5, 5, 5],
    [5, 5, 5, 3, 5, 5, 5],
    [3, 3, 3, 3, 3, 3, 3],
    [5, 5, 5, 3, 5, 5, 5],
    [5, 5, 5, 3, 5, 5, 5],
    [5, 5, 5, 3, 5, 5, 5]
]),
    np.array([
    [5, 5, 5, 8, 5, 5, 5],
    [5, 5, 5, 8, 5, 5, 5],
    [5, 5, 5, 8, 5, 5, 5],
    [8, 8, 8, 8, 8, 8, 8],
    [5, 5, 5, 8, 5, 5, 5],
    [5, 5, 5, 8, 5, 5, 5],
    [5, 5, 5, 8, 5, 5, 5]
]),
]


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # find the center coordinates
    center_row = rows // 2
    center_col = cols // 2

    # get center pixel color
    center_color = input_grid[center_row, center_col]
    
    # change output pixels 
    for i in range(rows):
        output_grid[i, center_col] = center_color  # change pixels on central column
    for j in range(cols):
        output_grid[center_row, j] = center_color  # change pixels on central row
    
    return output_grid

example_predictions = [transform(inp) for inp in example_inputs]

reports = [get_report(inp, out, pred) for inp, out, pred in zip(example_inputs, example_outputs, example_predictions)]

for i, report in enumerate(reports):
    print(f"Example {i+1}:")
    print(f"  Accuracy: {report['accuracy']:.4f}")
    print(f"  Correct Pixels: {report['correct_pixels']} / {report['total_pixels']}")
