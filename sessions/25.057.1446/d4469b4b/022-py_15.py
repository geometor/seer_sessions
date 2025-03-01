import numpy as np

train_examples = [
    {
        'input': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
        'output': [[0, 0, 0], [0, 5, 0], [0, 0, 0]]
    },
    {
        'input': [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]],
        'output': [[0, 5, 0], [0, 5, 0], [0, 5, 0]]
    },
    {
        'input': [[0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0], [0, 1, 0, 1, 0], [0, 0, 0, 0, 0]],
        'output': [[5, 0, 5], [0, 0, 0], [5, 0, 5]]
    },
     {
        'input': [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]],
        'output': [[5, 0, 0], [0, 0, 0], [0, 0, 5]]
    }
]

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        # Input grid analysis
        input_blue_count = np.sum(input_grid == 1)
        input_blue_positions = np.where(input_grid == 1)
        
        # Output grid analysis
        output_gray_count = np.sum(output_grid == 5)
        output_gray_positions = np.where(output_grid == 5)

        results.append({
            'example': i + 1,
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'input_blue_count': input_blue_count,
            'input_blue_positions': list(zip(input_blue_positions[0].tolist(), input_blue_positions[1].tolist())),
            'output_gray_count': output_gray_count,
            'output_gray_positions': list(zip(output_gray_positions[0].tolist(), output_gray_positions[1].tolist())),
        })
    return results

analysis = analyze_examples(train_examples)

for result in analysis:
    print(result)