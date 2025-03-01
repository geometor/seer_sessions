import numpy as np

def report_results(examples, transform_function):
    """
    Analyzes the transformation results for a set of examples.

    Args:
        examples: A list of (input_grid, output_grid) tuples.
        transform_function: The function that performs the transformation.

    Returns:
        A string containing the report.
    """

    report = ""
    total_examples = len(examples)
    correct_count = 0

    for i, (input_grid, expected_output) in enumerate(examples):
        transformed_grid = transform_function(input_grid)
        comparison = np.array_equal(transformed_grid, expected_output)
        if comparison:
            correct_count += 1

        report += f"Example {i + 1}:\n"
        report += f"Input:\n{input_grid}\n"
        report += f"Expected Output:\n{expected_output}\n"
        report += f"Transformed Output:\n{transformed_grid}\n"
        report += f"Correct: {comparison}\n"
        report += "-" * 20 + "\n"
    
    accuracy = (correct_count / total_examples) * 100
    report += f"Overall Accuracy: {accuracy:.2f}% ({correct_count}/{total_examples})\n"
    return report

# dummy data for example purposes, using the code under analysis
examples = [
    (np.array([[0, 0, 0, 0, 8, 8, 8, 8], [0, 0, 0, 0, 8, 8, 1, 8], [0, 0, 0, 0, 8, 8, 8, 8]]), np.array([[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])),
    (np.array([[0, 0, 0, 8, 8, 8, 8, 8], [0, 0, 0, 8, 3, 8, 8, 8], [0, 0, 0, 8, 8, 8, 2, 8]]), np.array([[0, 0, 0, 0], [3, 0, 0, 0], [2, 0, 0, 0]])),
    (np.array([[0, 0, 0, 0, 8, 8, 8, 8], [0, 0, 0, 0, 8, 8, 8, 8], [0, 0, 0, 0, 8, 8, 8, 8], [0, 0, 0, 0, 8, 5, 8, 8]]), np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [5, 0, 0, 0]])),
]

from previous_code import transform # Using transform from "Previous Code"

print(report_results(examples, transform))