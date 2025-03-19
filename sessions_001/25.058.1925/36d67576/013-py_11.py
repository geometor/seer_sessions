import numpy as np

def show_result(example_number, input_grid, expected_output, actual_output):
    print(f"Example {example_number}:")
    print("Input:")
    print(input_grid)
    print("Expected Output:")
    print(expected_output)
    print("Actual Output:")
    print(actual_output)
    print("Match:", np.array_equal(expected_output, actual_output))
    print("-" * 20)

# Example Grids (replace with actual data from the task)
example_1_in = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 4, 4, 4, 4, 4, 0],
                         [0, 0, 0, 0, 4, 4, 4, 4, 4, 0],
                         [0, 0, 0, 0, 4, 4, 4, 4, 4, 0],
                         [0, 0, 0, 0, 4, 4, 4, 4, 4, 0],
                         [0, 0, 3, 0, 4, 4, 4, 4, 4, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
example_1_out = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 3, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 4, 4, 4, 4, 4, 0],
                          [0, 0, 0, 0, 4, 4, 4, 4, 4, 0],
                          [0, 0, 0, 0, 4, 4, 3, 4, 4, 0],
                          [0, 0, 0, 0, 4, 4, 4, 4, 4, 0],
                          [0, 0, 3, 0, 4, 1, 4, 4, 4, 0],
                          [0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 3, 4, 3, 3, 0, 0, 0, 0],
                          [0, 0, 3, 4, 3, 3, 0, 0, 0, 0]])
example_2_in = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 4, 4, 0, 0],
       [0, 0, 0, 0, 4, 4, 0, 0],
       [0, 0, 0, 0, 4, 4, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]])
example_2_out = np.array([[0, 0, 0, 3, 0, 1, 0, 0],
        [0, 0, 0, 0, 4, 4, 0, 0],
        [0, 0, 0, 0, 4, 4, 0, 0],
        [0, 0, 0, 0, 4, 1, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 4, 3, 3, 0, 0],
        [0, 0, 3, 4, 3, 3, 0, 0]])
example_3_in = np.array([[4, 4, 4, 4, 0, 0, 0, 0, 0],
       [4, 4, 4, 4, 0, 0, 0, 0, 0],
       [4, 4, 4, 4, 0, 0, 0, 0, 0],
       [4, 4, 4, 4, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]])
example_3_out = np.array([[4, 4, 4, 4, 0, 0, 3, 0, 1],
       [4, 4, 3, 4, 0, 0, 0, 0, 0],
       [4, 4, 4, 4, 0, 0, 0, 0, 0],
       [4, 1, 4, 4, 0, 0, 0, 0, 0],
       [3, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 3, 4, 3, 3, 0, 0, 0],
       [0, 0, 3, 4, 3, 3, 0, 0, 0]])
example_4_in = np.array([[4, 4, 4, 0, 0, 0],
                          [4, 4, 4, 0, 0, 0],
                          [4, 4, 4, 0, 0, 0]])
example_4_out = np.array([[4, 4, 4, 0, 3, 1],
        [4, 3, 4, 0, 0, 0],
        [4, 1, 4, 0, 0, 0],
        [3, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [3, 4, 3, 3, 0, 0],
        [3, 4, 3, 3, 0, 0]])

# Assuming you have your `transform` function defined as before

actual_output_1 = transform(example_1_in)
show_result(1, example_1_in, example_1_out, actual_output_1)

actual_output_2 = transform(example_2_in)
show_result(2, example_2_in, example_2_out, actual_output_2)

actual_output_3 = transform(example_3_in)
show_result(3, example_3_in, example_3_out, actual_output_3)

actual_output_4 = transform(example_4_in)
show_result(4, example_4_in, example_4_out, actual_output_4)
