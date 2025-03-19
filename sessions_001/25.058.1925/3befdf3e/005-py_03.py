import numpy as np

def describe_grid(grid):
    """Provides a basic description of the grid."""
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    return {
        "shape": grid.shape,
        "color_counts": color_counts,
    }

def analyze_example(input_grid, output_grid, predicted_output):
    """Analyzes an example pair and the predicted output."""
    
    input_desc = describe_grid(input_grid)
    output_desc = describe_grid(output_grid)
    predicted_desc = describe_grid(predicted_output)
    
    correct = np.array_equal(output_grid, predicted_output)

    diff_with_output = np.where(output_grid != predicted_output)
    diff_count = diff_with_output[0].size

    print(f"  Input: Shape {input_desc['shape']}, Colors: {input_desc['color_counts']}")
    print(f"  Output: Shape {output_desc['shape']}, Colors: {output_desc['color_counts']}")
    print(f"  Predicted: Shape {predicted_desc['shape']}, Colors: {predicted_desc['color_counts']}")
    print(f"  Correct: {correct}, Differences with Output: {diff_count}")
    if not correct:
        print(f"   Indices of differences: {diff_with_output}")


# Assuming the task examples are stored in variables like this:
# train_input_0, train_output_0, train_predicted_0, ...

task_examples = [
    (train_input_0, train_output_0, train_predicted_0),
    (train_input_1, train_output_1, train_predicted_1),
    (train_input_2, train_output_2, train_predicted_2),
]

for i, (input_grid, output_grid, predicted_output) in enumerate(task_examples):
    print(f"Example {i}:")
    analyze_example(input_grid, output_grid, predicted_output)
