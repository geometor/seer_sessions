def code_execution(inputs, outputs, predictions):
    results = []
    for i, (input_grid, output_grid, predicted_grid) in enumerate(zip(inputs, outputs, predictions)):
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)
        predicted_grid = np.array(predicted_grid)

        correct = np.array_equal(output_grid, predicted_grid)
        diff = None
        if not correct:
            diff = output_grid - predicted_grid

        results.append({
            "example_index": i,
            "correct": correct,
            "input_shape": input_grid.shape,
            "output_shape": output_grid.shape,
            "predicted_shape": predicted_grid.shape,
            "diff": diff.tolist() if diff is not None else None,
        })
    return results