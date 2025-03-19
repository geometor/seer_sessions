import numpy as np

def get_grid_dimensions(grid_string):
    rows = grid_string.strip().split('\n')
    height = len(rows)
    width = len(rows[0])
    return height, width

def analyze_examples(task):
    analysis = []
    for example in task['train']:
        input_grid_str = example['input']
        output_grid_str = example['output']
        input_height, input_width = get_grid_dimensions(input_grid_str)
        output_height, output_width = get_grid_dimensions(output_grid_str)
        analysis.append({
            'input_height': input_height,
            'input_width': input_width,
            'output_height': output_height,
            'output_width': output_width,
            'height_ratio': output_height / input_height,
            'width_ratio': output_width / input_width
        })
    return analysis
task = {
    "train": [
        {
            "input": "000\n000\n000",
            "output": "000000000\n000000000\n000000000\n000000000\n000000000\n000000000\n000000000\n000000000\n000000000"
        },
        {
            "input": "11111\n11111\n11111\n11111\n11111",
            "output": "111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111\n111111111111111"
        },
        {
            "input": "22\n22",
            "output": "222222\n222222\n222222\n222222\n222222\n222222"
        },
        {
            "input": "1234567\n2345671\n3456712\n4567123\n5671234\n6712345\n7123456",
            "output": "123456712345671234567\n234567123456712345671\n34567123456712345671\n4567123456712345671\n567123456712345671\n67123456712345671\n7123456712345671\n123456712345671234567\n234567123456712345671\n34567123456712345671\n4567123456712345671\n567123456712345671\n67123456712345671\n7123456712345671\n123456712345671234567\n234567123456712345671\n34567123456712345671\n4567123456712345671\n567123456712345671\n67123456712345671\n7123456712345671"
        }

    ]
}

analysis = analyze_examples(task)
print(analysis)