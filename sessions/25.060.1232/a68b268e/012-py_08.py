import numpy as np

def analyze_example(example):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    
    input_shapes = []
    input_colors = []
    
    # very simplistic object detection - assumes no overlap
    for color in np.unique(input_grid):
        rows, cols = np.where(input_grid == color)
        if len(rows) > 0:
            min_row, max_row = np.min(rows), np.max(rows)
            min_col, max_col = np.min(cols), np.max(cols)
            width = max_col - min_col + 1
            height = max_row - min_row + 1
            input_shapes.append((height, width))
            input_colors.append(color)
    output_colors = [c for c in np.unique(output_grid) if c!= 0]
            
    return {
        'input_shapes': input_shapes,
        'input_colors': input_colors,
        'output_colors': output_colors,
        'output_shape': output_grid.shape
    }
task = {
    "train": [
        {
            "input": [
                [3, 3, 3, 8, 8, 8, 8, 8],
                [3, 3, 3, 8, 8, 8, 8, 8],
                [3, 3, 3, 8, 8, 8, 8, 8],
                [3, 3, 3, 8, 8, 8, 8, 8],
                [3, 3, 3, 8, 8, 8, 8, 8],
                [3, 3, 3, 8, 8, 8, 2, 2],
                [3, 3, 3, 8, 8, 8, 2, 2],
                [3, 3, 3, 8, 8, 8, 2, 2],
            ],
            "output": [[3, 8, 0, 8], [3, 8, 0, 0], [3, 0, 0, 0], [3, 2, 0, 2]],
        },
        {
            "input": [
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
                [8, 8, 8, 8, 8, 8, 3, 3],
            ],
            "output": [[8, 3, 0, 3], [8, 0, 0, 0], [8, 0, 0, 0], [8, 3, 0, 3]],
        },
        {
            "input": [
                [4, 4, 4, 4, 4, 1, 1, 1],
                [4, 4, 4, 4, 4, 1, 1, 1],
                [4, 4, 4, 4, 4, 1, 1, 1],
                [4, 4, 4, 4, 4, 1, 1, 1],
                [4, 4, 4, 4, 4, 1, 1, 1],
                [8, 8, 8, 8, 8, 1, 1, 1],
                [8, 8, 8, 8, 8, 1, 1, 1],
                [8, 8, 8, 8, 8, 1, 1, 1],
            ],
            "output": [[4, 1, 0, 1], [4, 0, 0, 0], [8, 0, 0, 0], [8, 1, 0, 1]],
        },
        {
            "input": [
                [7, 7, 7, 0, 0, 0, 0, 0],
                [7, 7, 7, 0, 0, 0, 0, 0],
                [7, 7, 7, 0, 0, 0, 0, 0],
                [0, 0, 0, 5, 5, 5, 5, 5],
                [0, 0, 0, 5, 5, 5, 5, 5],
                [0, 0, 0, 5, 5, 5, 5, 5],
                [0, 0, 0, 5, 5, 5, 5, 5],
                [0, 0, 0, 5, 5, 5, 5, 5],
            ],
            "output": [[7, 0, 0, 0], [0, 5, 0, 5], [0, 5, 0, 5], [0, 5, 0, 5]],
        },
    ],
    "test": [
        {"input": [[6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3], [6, 6, 6, 6, 6, 6, 3, 3]], "output": [[6, 3, 0, 3], [6, 0, 0, 0], [6, 0, 0, 0], [6, 3, 0, 3]]}
    ],
}

for i, example in enumerate(task['train']):
    analysis = analyze_example(example)
    print(f"Example {i}:")
    print(f"  Input Shapes: {analysis['input_shapes']}")
    print(f"  Input Colors: {analysis['input_colors']}")
    print(f"  Output Colors: {analysis['output_colors']}")
    print(f"  Output Shape: {analysis['output_shape']}")
    print("\n")

print("Test Example:")
analysis = analyze_example(task['test'][0])
print(f"  Input Shapes: {analysis['input_shapes']}")
print(f"  Input Colors: {analysis['input_colors']}")
print(f"  Output Colors: {analysis['output_colors']}")
print(f"  Output Shape: {analysis['output_shape']}")