def analyze_example(example):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])

    # Find colored blocks, even single pixels
    colored_blocks = find_colored_blocks(input_grid)
    
    num_target_blocks = len(colored_blocks)
    target_colors = sorted(list(set([block['color'] for block in colored_blocks.values()])))

    print(f"  Number of Target Blocks: {num_target_blocks}")
    print(f"  Target Colors: {target_colors}")
    print(f"  Output Grid Shape: {output_grid.shape}")

    return

example_data = task["train"]

for i, example in enumerate(example_data):
    print(f"Example {i+1}:")
    analyze_example(example)