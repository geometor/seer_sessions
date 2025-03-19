def examine_examples(task):
    reports = []
    for example in task['train']:
        input_grid = example['input']
        output_grid = example['output']
        input_np = np.array(input_grid)
        output_np = np.array(output_grid)
        
        report = {
            'input_shape': input_np.shape,
            'output_shape': output_np.shape,
            'output_values': np.unique(output_np).tolist(),
            'colors_present':{}
        }
        
        for color in [1,2,4]:
            report['colors_present'][color] = np.any(input_np == color)

        reports.append(report)

    return reports

# Assuming 'task' variable holds the current ARC task data
# results = examine_examples(task) #call the function with task data
# for i, report in enumerate(results):
#  print(f"Example {i+1}:")
#  print(report)