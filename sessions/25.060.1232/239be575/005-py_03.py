def analyze_examples(task):
    print("Example Analysis:\n")
    for i, example in enumerate(task["train"]):
        input_grid = example["input"]
        output_grid = example["output"]
        
        # Previous logic, for comparison.
        red_count = np.sum(input_grid == 2)
        azure_count = np.sum(input_grid == 8)
        predicted_output = abs(red_count - azure_count)
        actual_output = output_grid[0][0]

        print(f"Example {i + 1}:")
        print(f"  Red Count: {red_count}")
        print(f"  Azure Count: {azure_count}")
        print(f"  Predicted Output (Previous Logic): {predicted_output}")
        print(f"  Actual Output: {actual_output}")
        print(f"  Correct: {predicted_output == actual_output}")
        print("-" * 20)

# Assuming 'task' is a dictionary containing the ARC task data.
# For demonstration, I will create a sample 'task':

sample_task = {
    "train": [
        {"input": np.array([[2, 8], [8, 2]]), "output": np.array([[0]])},
        {"input": np.array([[2, 2, 2], [8, 8, 8], [2,8,2]]), "output": np.array([[0]])},
        {"input": np.array([[2, 2, 2], [2, 2, 2], [2, 2, 8]]), "output": np.array([[5]])},
    ]
}
analyze_examples(sample_task)
