import numpy as np

def calculate_metrics(task, transform_function):
    """
    Calculates and displays metrics for each example in the task's training set.

    Args:
        task: The task object containing the training examples.
        transform_function: The function that transforms the input grid.
    """
    metrics_report = []
    for example in task.train:
        input_grid = example["input"]
        expected_output_grid = example["output"]
        predicted_output_grid = transform_function(np.array(input_grid))

        # Calculate differences
        diff_grid = (np.array(expected_output_grid) != predicted_output_grid).astype(int)
        num_differences = np.sum(diff_grid)

        report = {
            "example_index": task.train.index(example),
            "input_grid_shape": np.array(input_grid).shape,
            "output_grid_shape": np.array(expected_output_grid).shape,
            "predicted_output_shape": predicted_output_grid.shape,
            "num_differences": num_differences,
            "differences_grid": diff_grid.tolist() #Convert to list for easy viewing
        }

        metrics_report.append(report)

    for report in metrics_report:
        print(f"Example {report['example_index']}:")
        print(f"  Input Shape: {report['input_grid_shape']}")
        print(f"  Output Shape: {report['output_grid_shape']}")
        print(f"  Predicted Output Shape: {report['predicted_output_shape']}")
        print(f"  Number of Differences: {report['num_differences']}")
        print(f"  Differences Grid:\n{np.array(report['differences_grid'])}") # back to numpy array for viewing
        print("-" * 20)
    return metrics_report

# Assuming 'task' and 'transform' are defined elsewhere.
metrics = calculate_metrics(task, transform)

