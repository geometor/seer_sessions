import numpy as np

# Provided data from the problem description
task_data = [
    {
        'input': [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
        'expected': [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        'actual': [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        'correct': True
    },
    {
        'input': [[5, 5, 8], [5, 5, 5], [5, 5, 5]],
        'expected': [[1, 1, 9], [1, 1, 1], [1, 1, 1]],
        'actual': [[1, 1, 9], [1, 1, 1], [1, 1, 1]],
        'correct': True
    },
    {
        'input': [[6, 5, 8], [5, 5, 5], [5, 6, 8]],
        'expected': [[2, 1, 9], [1, 1, 1], [1, 2, 9]],
        'actual': [[2, 1, 9], [1, 1, 1], [1, 2, 9]],
        'correct': True
    }
]

# Check the correctness and consistency
for i, example in enumerate(task_data):
  # verify the correctness value
    expected_array = np.array(example['expected'])
    actual_array = np.array(example['actual'])
    calculated_correct = np.array_equal(expected_array, actual_array)

    print(f"Example {i+1}:")
    print(f"  Correctness matches expectation: {calculated_correct == example['correct']}")

    # check the substitution rules on this example
    input_array = np.array(example['input'])
    for r in range(input_array.shape[0]):
        for c in range(input_array.shape[1]):
            input_val = input_array[r,c]
            output_val = actual_array[r,c]

            if input_val == 5:
              print(f"  input {input_val} should map to 1: {output_val == 1}")
            if input_val == 8:
              print(f"  input {input_val} should map to 9: {output_val == 9}")
            if input_val == 6:
              print(f"  input {input_val} should map to 2: {output_val == 2}")