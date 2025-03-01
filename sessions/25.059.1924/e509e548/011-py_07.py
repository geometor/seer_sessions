
def check_solution(task):
    """
    Checks the solution against all training examples and prints relevant information.

    Args:
        task: The task dictionary containing 'train' and 'test' examples.
    """
    print("Checking solution...\n")

    for example_index, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        output_grid = transform(input_grid)
        
        print(f"Example {example_index + 1}:")
        print(f"Input Grid Dimensions: {input_grid.shape}")
        print(f"Input:\n{input_grid}")
        print(f"Output:\n{output_grid}")
        print(f"Expected:\n{expected_output}")


        green_regions = find_connected_regions(input_grid, 3)
        print(f"Green Regions: {green_regions}")
        
        correct = np.array_equal(output_grid, expected_output)
        print(f"Correct: {correct}")

        if not correct:
            diff = output_grid != expected_output
            print("Differences (Output != Expected):")
            print(diff)

        print("-" * 20)

# Assuming 'task' variable is loaded with the ARC task data
# check_solution(task)
