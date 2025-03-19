import numpy as np

train_examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0], [0, 3, 0], [0, 0, 0]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 6, 6, 0, 0, 0, 0], [0, 0, 6, 0, 6, 0, 0, 0, 0], [0, 0, 6, 6, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
      "output": [[6, 6, 6], [6, 0, 6], [6, 6, 6]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 4, 4, 0, 0], [0, 0, 0, 0, 4, 4, 4, 0, 0], [0, 0, 0, 0, 4, 4, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[4, 4, 4], [4, 4, 4], [4, 4, 4]]
    },
    {
        "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 2, 1, 1], [1, 1, 1, 1, 1, 2, 2, 2, 1], [1, 1, 1, 1, 1, 1, 2, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]],
        "output": [[1, 1, 1], [1, 2, 1], [1, 1, 1]]
    },
    {
        "input" : [[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 3, 5, 5], [5, 5, 5, 5, 5, 3, 3, 3, 5], [5, 5, 5, 5, 5, 5, 3, 5, 5]],
        "output": [[5, 5, 5], [5, 3, 5], [5, 5, 5]]
    }
]

def analyze_examples(examples):
    results = []
    for example in examples:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        # Find the non-background color in the output
        output_colors = np.unique(output_grid)
        target_colors = output_colors[output_colors != 0]
        
        
        # Find coordinates of target color in input grid
        target_coords = []
        
        for color in target_colors:
            coords = np.argwhere(input_grid == color)
            if len(coords) > 0 :
                target_coords.append(coords)

        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'output_colors': output_colors.tolist(),
            'target_coords' : target_coords
        })
    return results

analysis = analyze_examples(train_examples)

for i, result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Output Colors: {result['output_colors']}")
    if result['target_coords']:
        print(f"  Coords of target colors in input: {[coords.tolist() for coords in result['target_coords']]}")
    else:
        print("Target Color not found in input")
    print("-" * 20)