import numpy as np

def execute_and_compare(input_grid, expected_output_grid, transform_function):
    actual_output_grid = transform_function(np.array(input_grid))
    comparison = np.array_equal(actual_output_grid, np.array(expected_output_grid))
    print(f"Input:\n{np.array(input_grid)}\n")
    print(f"Expected Output:\n{np.array(expected_output_grid)}\n")
    print(f"Actual Output:\n{actual_output_grid}\n")
    print(f"Match: {comparison}\n")
    return comparison

#Original examples
input_grid1 = [[5, 5, 5], [5, 5, 5], [5, 5, 5]]
expected_output_grid1 = [[3, 3, 3], [3, 3, 3], [3, 3, 3]]

input_grid2 = [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]
expected_output_grid2 = [[3, 5, 5, 5], [3, 5, 5, 5], [3, 5, 5, 5], [3, 5, 5, 5]]

input_grid3 = [
            [6, 6, 8, 8, 8, 8, 6, 6, 6, 8, 8, 8, 8, 6, 6],
            [6, 6, 8, 8, 8, 8, 6, 6, 6, 8, 8, 8, 8, 6, 6],
            [6, 6, 8, 8, 8, 8, 6, 6, 6, 8, 8, 8, 8, 6, 6],
            [6, 6, 8, 8, 8, 8, 6, 6, 6, 8, 8, 8, 8, 6, 6],
            [6, 6, 8, 8, 8, 8, 6, 6, 6, 8, 8, 8, 8, 6, 6],
            [6, 6, 8, 8, 8, 8, 6, 6, 6, 8, 8, 8, 8, 6, 6],
            [6, 6, 8, 8, 8, 8, 6, 6, 6, 8, 8, 8, 8, 6, 6],
        ]
expected_output_grid3 = [
            [6, 6, 3, 3, 3, 3, 6, 6, 6, 3, 3, 3, 3, 6, 6],
            [6, 6, 3, 3, 3, 3, 6, 6, 6, 3, 3, 3, 3, 6, 6],
            [6, 6, 3, 3, 3, 3, 6, 6, 6, 3, 3, 3, 3, 6, 6],
            [6, 6, 3, 3, 3, 3, 6, 6, 6, 3, 3, 3, 3, 6, 6],
            [6, 6, 3, 3, 3, 3, 6, 6, 6, 3, 3, 3, 3, 6, 6],
            [6, 6, 3, 3, 3, 3, 6, 6, 6, 3, 3, 3, 3, 6, 6],
            [6, 6, 3, 3, 3, 3, 6, 6, 6, 3, 3, 3, 3, 6, 6],
        ]

# Simulate code execution and comparison
print("Example 1:")
execute_and_compare(input_grid1, expected_output_grid1, transform)
print("Example 2:")
execute_and_compare(input_grid2, expected_output_grid2, transform)
print("Example 3:")
execute_and_compare(input_grid3, expected_output_grid3, transform)
