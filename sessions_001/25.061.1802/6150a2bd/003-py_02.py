import numpy as np

def transform(input_grid):
    input_array = np.array(input_grid)
    output_array = np.rot90(input_array, k=-1)
    return output_array.tolist()

def show_grid(grid, label):
    print(f"--- {label} ---")
    for row in grid:
        print(row)
    print()


def analyze_examples(task_data):
   results = {}
   for example_index, example in enumerate(task_data['train']):
        input_grid = example['input']
        expected_output_grid = example['output']
        predicted_output_grid = transform(input_grid)
        is_correct = predicted_output_grid == expected_output_grid

        results[f'example_{example_index}'] = {
            'input_grid': input_grid,
            'expected_output_grid': expected_output_grid,
            'predicted_output_grid': predicted_output_grid,
            'correct': is_correct
        }
   return results
        

task_data = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [2, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [8, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]},
        {'input': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]], 'output': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}
    ]
}


analysis_results = analyze_examples(task_data)

for example_key, result in analysis_results.items():
  print(example_key)
  show_grid(result['input_grid'], "Input")
  show_grid(result['expected_output_grid'], "Expected Output")
  show_grid(result['predicted_output_grid'], "Predicted Output")
  print(f"Correct: {result['correct']}")
  print("-" * 20)