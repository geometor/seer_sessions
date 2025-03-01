import numpy as np

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a detailed report of their differences.
    """
    if grid1.shape != grid2.shape:
        return "Different shapes"

    diff = grid1 != grid2
    if not np.any(diff):
        return "Same"

    num_diff = np.sum(diff)
    diff_indices = np.where(diff)
    diff_details = []
    for i in range(len(diff_indices[0])):
        row, col = diff_indices[0][i], diff_indices[1][i]
        diff_details.append(
            f"  Pixel at ({row}, {col}): Expected {grid2[row, col]}, Got {grid1[row, col]}"
        )

    report = f"{num_diff} differences:\n" + "\n".join(diff_details)
    return report

# Example Usage (replace with actual data from ARC task)
# NOTE:
# task will be provided in NEXT turn
# example_input, example_output will be defined using the data from the task
# transform function will be defined using previous_code
# these are included here to demonstrate how to use code_execution to gather
# metrics.

# predicted_output = transform(example_input)
# comparison_report = compare_grids(predicted_output, example_output)
# print(comparison_report)
