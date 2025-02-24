def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        input_shape = input_grid.shape
        output_shape = output_grid.shape
        shape_ratio = (output_shape[0] / input_shape[0], output_shape[1] / input_shape[1])

        results.append({
            'input_shape': input_shape,
            'output_shape': output_shape,
            'shape_ratio': shape_ratio
        })
    return results

# task is defined in the context, no need to define it again, just use it to access data
analysis_results = analyze_examples(task)
print(analysis_results)
