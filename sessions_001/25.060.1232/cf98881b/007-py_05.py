def get_metrics(input_grid, expected_output, actual_output):
    """
    Compares the expected and actual outputs, reporting discrepancies.

    Args:
        input_grid: The input grid.
        expected_output:  The expected output grid.
        actual_output: The actual output grid produced by the transform function.

    Returns:
        A dictionary containing metrics about the comparison.
    """
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    metrics = {
        "input_shape": input_grid.shape,
        "expected_shape": expected_output.shape,
        "actual_shape": actual_output.shape,
        "match": np.array_equal(expected_output, actual_output),
    }
    if not metrics["match"]:
        diff = expected_output - actual_output
        metrics["difference"] = diff.tolist()
    else:
        metrics["difference"] = None  # No difference if they match

    return metrics

def test_transform_on_examples(transform_func, examples):
    results = []
    for example in examples:
        input_grid = example["input"]
        expected_output = example["output"]
        actual_output = transform_func(input_grid)
        metrics = get_metrics(input_grid, expected_output, actual_output)
        results.append(metrics)
    return results