import numpy as np

def code_execution(input_grid, output_grid, expected_output, transform):
    """Executes the transform function and compares the output with the expected output."""    
    actual_output = transform(input_grid.copy())
    comparison = actual_output == expected_output

    report = f"""
Input Grid:
{input_grid}
Expected Output:
{expected_output}
Actual Output:
{actual_output}
Comparison (Actual == Expected):
{comparison.all()}
Differences:
"""
    if not comparison.all():
        diff = np.where(actual_output != expected_output)
        for r, c in zip(*diff):
          report += f"  - location: ({r},{c}), actual_output: {actual_output[r,c]}, expected: {expected_output[r,c]}\n"
    else:
       report += "  None\n"

    return report