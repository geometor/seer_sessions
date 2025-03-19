import numpy as np

def analyze_examples(task):
    results = []
    for example in task.train:
        input_grid = example['input']
        output_grid = example['output']
        input_array = np.array(input_grid)
        output_array = np.array(output_grid)

        rotated_input = np.rot90(input_array, k=-1)
        is_rotated = np.array_equal(rotated_input, output_array)
        is_identity = np.array_equal(input_array, output_array)

        input_height, input_width = input_array.shape
        input_colors = np.unique(input_array)

        results.append({
            'example_id': example['id'], # Assuming examples have IDs
            'is_rotated': is_rotated,
            'is_identity': is_identity,
            'input_height': input_height,
            'input_width': input_width,
            'input_colors': input_colors.tolist(),
            # Add more properties as needed.  E.g., presence of specific shapes
            # 'has_rectangle': detect_rectangle(input_array),
        })
    return results

# Example Usage (replace with actual task data)
# analysis_results = analyze_examples(task)
# print(analysis_results)

#The following is added to simulate running the code execution block
class MockExample:
    def __init__(self, input_grid, output_grid, example_id):
        self.input = input_grid
        self.output = output_grid
        self.id = example_id

class MockTask:
    def __init__(self, train_examples):
        self.train = train_examples

# Mock data - Replace this with your actual task data
train_examples = [
  MockExample([[5, 5, 5], [5, 5, 5], [5, 5, 5]], [[5, 5, 5], [5, 5, 5], [5, 5, 5]], 'ex1'),
  MockExample([[1, 2], [3, 4]], [[3, 1], [4, 2]], 'ex2'),
  MockExample([[1, 1, 1], [2, 2, 2]], [[2, 1], [2, 1], [2, 1]], 'ex3'),
  MockExample([[7,8,9,0]], [[7,8,9,0]], 'ex4'),
]

mock_task = MockTask(train_examples)
analysis_results = analyze_examples(mock_task)
print(analysis_results)

