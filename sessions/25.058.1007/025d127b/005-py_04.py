import numpy as np

def code_execution(input_grid, output_grid, predicted_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_grid = np.array(predicted_grid)

    input_shapes = find_shapes(input_grid)
    output_shapes = find_shapes(output_grid)
    predicted_shapes = find_shapes(predicted_grid)

    input_shape_count = len(input_shapes)
    output_shape_count = len(output_shapes)
    predicted_shape_count = len(predicted_shapes)
    
    correct_pixels = np.sum(output_grid == predicted_grid)
    total_pixels = output_grid.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0

    print(f"  Input Shape Count: {input_shape_count}")
    print(f"  Output Shape Count: {output_shape_count}")
    print(f"  Predicted Shape Count: {predicted_shape_count}")
    print(f"  Pixel Accuracy: {accuracy:.4f}")

# Example Usage (replace with actual grids):
# You'll need to define example_input_grids, example_output_grids, predicted_output_grids from the task.

example_input_grids = [
    [[4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4],
    [4, 4, 4, 4, 4, 4]],
    
    [[8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8]],
    
    [[5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5],
    [5, 5, 5, 5, 5, 5, 5, 5, 5]]
]
example_output_grids = [
    [[4, 4, 4, 4, 4, 4],
     [4, 0, 0, 0, 0, 4],
     [4, 4, 4, 4, 4, 4]],

    [[8, 8, 8, 8, 8, 8, 8, 8],
     [8, 0, 0, 0, 0, 0, 0, 8],
     [8, 0, 0, 0, 0, 0, 0, 8],
     [8, 0, 0, 0, 0, 0, 0, 8],
     [8, 8, 8, 8, 8, 8, 8, 8]],
    
    [[5, 5, 5, 5, 5, 5, 5, 5, 5],
     [5, 0, 0, 0, 0, 0, 0, 0, 5],
     [5, 0, 0, 0, 0, 0, 0, 0, 5],
     [5, 0, 0, 0, 0, 0, 0, 0, 5],
     [5, 0, 0, 0, 0, 0, 0, 0, 5],
     [5, 5, 5, 5, 5, 5, 5, 5, 5]]
]
predicted_output_grids = [transform(input_grid) for input_grid in example_input_grids]

for i in range(len(example_input_grids)):
    print(f"Example {i+1}:")
    code_execution(example_input_grids[i], example_output_grids[i], predicted_output_grids[i])
    print("-" * 20)
