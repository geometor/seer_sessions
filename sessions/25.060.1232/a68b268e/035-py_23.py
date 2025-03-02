def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = example['input']
        expected_output = example['output']
        predicted_output = transform(input_grid)
        is_correct = np.array_equal(predicted_output, np.array(expected_output))
        results.append({
            'input': input_grid,
            'expected_output': expected_output,
            'predicted_output': predicted_output.tolist(),
            'is_correct': is_correct
        })
    return results

# this is a placeholder for the ARC task data - replace with the actual task
task_data = {
  "train": [
    {
      "input": [
        [8, 5, 5, 8],
        [5, 5, 5, 5],
        [1, 1, 1, 1],
        [5, 0, 0, 5],
        [8, 0, 5, 8]
      ],
      "output": [
        [8, 8, 8, 8],
        [8, 8, 8, 8],
        [8, 8, 8, 8],
        [8, 8, 8, 5]
      ]
    },
   {
      "input": [
       [7, 7, 7, 7, 7, 7, 7],
       [7, 7, 2, 7, 7, 2, 7],
       [7, 7, 7, 7, 7, 7, 7],
       [1, 1, 1, 1, 1, 1, 1],
       [7, 7, 7, 7, 7, 7, 7],
       [7, 2, 7, 7, 7, 2, 7]
      ],
      "output": [
        [7, 7, 7, 7],
        [7, 7, 7, 7],
        [7, 7, 7, 7],
        [7, 7, 7, 7]
      ]
    },
{
      "input": [
        [0, 0, 9, 9, 9, 0, 0, 0, 9],
        [9, 9, 0, 9, 9, 9, 9, 9, 9],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [9, 9, 9, 9, 0, 9, 9, 9, 9],
        [0, 0, 9, 9, 9, 0, 0, 9, 0]
      ],
      "output" :[
       [0, 9, 9, 0],
       [9, 9, 9, 9],
       [0, 9, 9, 0],
       [0, 9, 9, 9]
      ]
    }
  ]
}

analysis = analyze_results(task_data)

for item in analysis:
    print(f"Input:\n{np.array(item['input'])}\n")
    print(f"Expected Output:\n{np.array(item['expected_output'])}\n")
    print(f"Predicted Output:\n{np.array(item['predicted_output'])}\n")
    print(f"Is Correct: {item['is_correct']}\n")
    print("-" * 20)