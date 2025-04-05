import collections

# Helper functions (as defined in previous thought block)
def find_blocks_sim(data, value):
  if value == 0: return []
  blocks = []
  start_index = -1
  for i, element in enumerate(data):
    if element == value:
      if start_index == -1: start_index = i
    elif start_index != -1:
      blocks.append({'value': value, 'start': start_index, 'end': i - 1, 'length': (i - 1) - start_index + 1})
      start_index = -1
  if start_index != -1:
    blocks.append({'value': value, 'start': start_index, 'end': len(data) - 1, 'length': (len(data) - 1) - start_index + 1})
  return blocks

def find_longest_block_sim(blocks):
    if not blocks: return None
    # Python's max is stable, returns first element in case of ties.
    return max(blocks, key=lambda b: b['length'])


def analyze_example(input_list, output_list):
  analysis = {}
  n = len(input_list)
  unique_non_zeros = sorted(list(set(val for val in input_list if val != 0)))
  analysis['input_length'] = n
  analysis['output_length'] = len(output_list)
  analysis['unique_non_zeros'] = unique_non_zeros
  analysis['longest_blocks_info'] = {}
  analysis['all_blocks_count'] = {}

  simulated_output = [0] * n

  for value in unique_non_zeros:
    all_blocks = find_blocks_sim(input_list, value)
    analysis['all_blocks_count'][value] = len(all_blocks)
    longest = find_longest_block_sim(all_blocks)
    analysis['longest_blocks_info'][value] = {
        'start': longest['start'] if longest else -1,
        'end': longest['end'] if longest else -1,
        'length': longest['length'] if longest else 0
    }
    if longest:
      for i in range(longest['start'], longest['end'] + 1):
        simulated_output[i] = longest['value']

  analysis['output_matches_simulation'] = (simulated_output == output_list)
  return analysis

# Data representing the train examples (assuming direct list input now)
examples = [
    {'id': 'train_1', 'input': [3, 0, 3, 0, 3, 0, 0, 3, 3, 0, 0, 0], 'output': [0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0]},
    {'id': 'train_2', 'input': [3, 0, 0, 3, 3, 3, 3, 3, 0, 3, 0, 0], 'output': [0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0]},
    {'id': 'train_3', 'input': [0, 5, 5, 0, 5, 0, 0, 0, 5, 0, 5, 0], 'output': [0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    {'id': 'train_4', 'input': [0, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2], 'output': [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2]},
    {'id': 'train_5', 'input': [0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4], 'output': [0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0]},
    {'id': 'train_6', 'input': [1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0], 'output': [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    {'id': 'train_7', 'input': [0, 6, 0, 0, 6, 0, 6, 0, 0, 0, 6, 6], 'output': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6]},
]

# Run analysis
metrics = {}
for ex in examples:
    metrics[ex['id']] = analyze_example(ex['input'], ex['output'])

# Print relevant metrics
print("Example Analysis Summary:")
for ex_id, data in metrics.items():
    print(f"\n{ex_id}:")
    print(f"  Input/Output Length: {data['input_length']}")
    print(f"  Unique Non-zeros: {data['unique_non_zeros']}")
    for val in data['unique_non_zeros']:
        print(f"    Value {val}:")
        print(f"      Total Blocks Found: {data['all_blocks_count'][val]}")
        print(f"      Longest Block Length: {data['longest_blocks_info'][val]['length']} (Indices: {data['longest_blocks_info'][val]['start']}-{data['longest_blocks_info'][val]['end']})")
    print(f"  Simulated Output Matches Expected: {data['output_matches_simulation']}")
