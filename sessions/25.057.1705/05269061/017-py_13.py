def code_execution(inputs, outputs, transformed_outputs):
    results = []
    for i, (input_grid, output_grid, predicted_grid) in enumerate(zip(inputs, outputs, transformed_outputs)):
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)
        predicted_grid = np.array(predicted_grid)

        input_objects = get_objects(input_grid)
        output_objects = get_objects(output_grid)  # Analyze the *expected* output too

        results.append({
            'example': i + 1,
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'predicted_shape': predicted_grid.shape,
            'input_objects': [{'shape': obj['shape'], 'color': obj['color']} for obj in input_objects],
            'output_objects': [{'shape': obj['shape'], 'color': obj['color']} for obj in output_objects],
            'correct': np.array_equal(output_grid, predicted_grid)
        })
    return results

train_inputs = [
    [[1, 2, 3]],
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    [[1], [2], [3]],
    [[1, 0, 0], [0, 5, 0], [0, 0, 2]]
]
train_outputs = [
    [[1, 2, 3], [2, 3, 1], [3, 1, 2]],
    [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]],
    [[1, 1, 1], [2, 2, 2], [3, 3, 3]],
    [[1, 0, 0], [0, 5, 0], [0, 0, 2]]
]
transformed = [transform(inp) for inp in train_inputs]
results = code_execution(train_inputs, train_outputs, transformed)

for r in results:
    print(r)