def analyze_examples(examples):
    results = []
    for example in examples:
        input_grid = example['input']
        output_grid = example['output']
        input_array = np.array(input_grid)
        rows_with_red = np.any(input_array == 2, axis=1)
        num_rows_with_red = np.sum(rows_with_red)
        output_width = len(output_grid[0]) if len(output_grid) >0 else 0
        output_height = len(output_grid)
        
        results.append({
            'input_rows': len(input_grid),
            'input_cols': len(input_grid[0]),
            'rows_with_red': num_rows_with_red,
            'output_width': output_width,
            'output_height' : output_height,
            'output_color': output_grid[0][0] if output_width>0 else None, #check first pixel
            'match': num_rows_with_red == output_width
        })
    return results

examples = [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[2, 2]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0]], 'output': [[2, 2]]},
    {'input': [[0, 0, 0, 0, 0, 0], [0, 0, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0]], 'output': [[2]]},
    {'input': [[0, 0, 0, 0, 0], [0, 2, 2, 2, 0], [0, 0, 0, 0, 0], [0, 2, 2, 2, 0]], 'output': [[2, 2]]},
    {'input': [[0, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0]], 'output': [[2, 2]]}
]

analysis = analyze_examples(examples)

for i, result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Input: {result['input_rows']}x{result['input_cols']}")
    print(f"  Rows with Red: {result['rows_with_red']}")
    print(f"  Output: {result['output_height']}x{result['output_width']}")
    print(f"  Output Color: {result['output_color']}")
    print(f"  Match: {result['match']}")