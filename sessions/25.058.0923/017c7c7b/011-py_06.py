import numpy as np

# Example data (replace with actual data from the task)
# example 1
example_1_input = np.array([[0, 1, 0, 1, 0, 1, 0, 1, 0],
                            [1, 0, 1, 0, 1, 0, 1, 0, 1],
                            [0, 1, 0, 1, 0, 1, 0, 1, 0],
                            [1, 0, 1, 0, 1, 0, 1, 0, 1],
                            [0, 1, 0, 1, 0, 1, 0, 1, 0]])
example_1_expected = np.array([[0, 2, 0, 2, 0, 2, 0, 2, 0],
                               [2, 0, 2, 0, 2, 0, 2, 0, 2],
                               [0, 2, 0, 2, 0, 2, 0, 2, 0]])
example_1_output = transform(example_1_input)

# example 2
example_2_input = np.array([[0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0],
                            [0, 1, 0, 1, 0, 1],
                            [1, 0, 1, 0, 1, 0]])
example_2_expected = np.array([[0, 2, 0, 2, 0, 2],
                               [2, 0, 2, 0, 2, 0],
                               [0, 2, 0, 2, 0, 2]])
example_2_output = transform(example_2_input)

# example 3
example_3_input = np.array([[0, 1, 0, 1, 0],
                            [1, 0, 1, 0, 1],
                            [0, 1, 0, 1, 0],
                            [1, 0, 1, 0, 1]])
example_3_expected = np.array([[0, 2, 0, 2, 0],
                               [2, 0, 2, 0, 2],
                               [0, 2, 0, 2, 0],
                               [2, 0, 2, 0, 2]])
example_3_output = transform(example_3_input)

def compare_grids(expected, actual, example_name):
    if expected.shape == actual.shape:
        element_wise_comparison = np.equal(expected, actual)
        all_elements_equal = np.all(element_wise_comparison)

        print(f"{example_name}:")
        print(f"  Shape Match: {expected.shape == actual.shape}")
        print(f"  All Elements Match: {all_elements_equal}")
    else:
        print(f"{example_name}:")
        print(f"  Shape Match: {expected.shape == actual.shape}")
        print(f"    Expected Shape: {expected.shape}")
        print(f"    Actual Shape: {actual.shape}")
        print(f"  All Elements Match: False")

compare_grids(example_1_expected, example_1_output, "Example 1")
compare_grids(example_2_expected, example_2_output, "Example 2")
compare_grids(example_3_expected, example_3_output, "Example 3")