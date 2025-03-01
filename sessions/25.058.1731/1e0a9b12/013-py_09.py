import numpy as np

def find_object(grid, color):
    """Finds the coordinates of a single-cell object with the given color."""
    coords = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color:
                coords.append((r,c))
    return coords

def analyze_examples(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)  # Assuming 'transform' function from previous code
        
        example_data = {
            'correct': np.array_equal(output_grid, predicted_output),
            'input': input_grid.tolist(),
            'output': output_grid.tolist(),
            'predicted': predicted_output.tolist(),
            'objects_input':{},
            'objects_output':{}
        }
    
        colors = np.unique(input_grid)
        for color in colors:
            if color != 0:
                example_data['objects_input'][int(color)] = find_object(input_grid, color)
        colors = np.unique(output_grid)
        for color in colors:
            if color != 0:
                example_data['objects_output'][int(color)] = find_object(output_grid, color)
        results.append(example_data)

    return results

# this is used to create an object like the ARC json
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 8, 9, 0, 0, 0], [0, 7, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0], [0, 7, 9, 0, 0, 0], [0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 8, 9, 0, 0, 0], [0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0], [0, 5, 9, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        },
		{
            "input": [[0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0], [0, 0, 9, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 9, 0, 0, 0], [0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        }
    ]
}

analysis = analyze_examples(task)

for i, example_result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Correct prediction: {example_result['correct']}")
    print(f"  Objects Input:  {example_result['objects_input']}")
    print(f"  Objects Output: {example_result['objects_output']}")
    print(f"{'  Prediction Matches Output' if example_result['correct'] else '  Prediction Does NOT Match Output'}")
    #print(f"  Predicted Output:\n{example_result['predicted']}")
    print("-" * 20)