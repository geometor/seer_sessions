def code_execution(input_grid, expected_output, generated_output):
    """
    Simulates code execution to gather metrics. In reality,
    this would involve running the actual transform function.
    """

    input_colors = sorted(list(set(np.array(input_grid).flatten())))
    output_colors = sorted(list(set(np.array(expected_output).flatten())))
    generated_colors = []
    if generated_output:
       generated_colors = sorted(list(set(np.array(generated_output).flatten())))
    
    input_colors_nz = [c for c in input_colors if c != 0]
    output_colors_nz = [c for c in output_colors if c != 0]
    generated_colors_nz = [c for c in generated_colors if c != 0]

    return {
        "input_colors": input_colors_nz,
        "output_colors": output_colors_nz,
        "generated_colors": generated_colors_nz,
        "input_shape": np.array(input_grid).shape,
        "output_shape": np.array(expected_output).shape,
        "generated_shape": np.array(generated_output).shape if generated_output else None,
        "match": expected_output == generated_output
    }

# Mock data based on problem description
examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[1], [7], [2]],
        "generated": [[1], [7]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 5, 5, 5, 5, 0, 0], [0, 0, 5, 5, 5, 5, 5, 0, 0], [0, 0, 5, 5, 5, 5, 5, 0, 0], [0, 0, 5, 5, 5, 5, 5, 0, 0], [0, 0, 5, 5, 5, 5, 5, 0, 0], [0, 0, 5, 5, 5, 5, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [],
        "generated": []
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[1], [7], [2]],
        "generated": [[1], [2], [7]]

    },
        {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[1], [7], [2]],
        "generated": [[1], [2], [7]]
    }

]

results = [code_execution(ex["input"], ex["output"], ex["generated"]) for ex in examples]

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Colors (Non-Zero): {res['input_colors']}")
    print(f"  Output Colors (Non-Zero): {res['output_colors']}")
    print(f"  Generated Colors (Non-Zero): {res['generated_colors']}")
    print(f"  Input Shape: {res['input_shape']}")
    print(f"  Output Shape: {res['output_shape']}")
    print(f"  Generated Shape: {res['generated_shape']}")
    print(f"  Match: {res['match']}")
    print("-" * 20)