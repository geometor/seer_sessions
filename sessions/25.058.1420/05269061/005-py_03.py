def analyze_example(example):
    input_grid = example['input']
    output_grid = example['output']
    input_np = np.array(input_grid)
    output_np = np.array(output_grid)
    seed = input_np[:3, :3]

    results = {
        'input_shape': input_np.shape,
        'output_shape': output_np.shape,
        'seed': seed.tolist(),
        'input_first_row': input_np[0].tolist(),
        'output_first_row': output_np[0].tolist(),
        'input_colors': np.unique(input_np).tolist(),
        'output_colors': np.unique(output_np).tolist(),
        'seed_colors':np.unique(seed).tolist(),

    }
    return results

train_examples = task['train']
example_results = [analyze_example(ex) for ex in train_examples]
print(example_results)

#check transform on test examples
for i, ex in enumerate(task['train']):
    print(f"Example: {i}")
    pred = transform(ex['input'])
    print(f"Prediction:\n{np.array(pred)}")
    print(f"Expected:\n{np.array(ex['output'])}")
    print(f"Correct: {np.array_equal(np.array(pred),np.array(ex['output']))}")
