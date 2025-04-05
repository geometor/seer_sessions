def parse_string(s):
  """Parses a space-separated string of digits into a list of integers."""
  if not s.strip():
    return []
  return [int(x) for x in s.split()]

def format_list(lst):
  """Formats a list of integers into a space-separated string."""
  return " ".join(map(str, lst))

def transform_logic(input_list):
  """Moves the first element of the list to the end."""
  if not input_list or len(input_list) < 2:
    return input_list[:]
  first_element = input_list[0]
  remaining_elements = input_list[1:]
  output_list = remaining_elements + [first_element]
  return output_list

# Example Data
train_examples = [
    {"input": "0 9 9 9 9 9 9 9 9 9 9 0", "output": "9 9 9 9 9 9 9 9 9 9 0 0"},
    {"input": "9 9 0 0 0 0 0 0 0 0 0 9", "output": "9 0 0 0 0 0 0 0 0 0 9 9"},
    {"input": "0 0 9 9 9 9 9 9 0 0 0 0", "output": "0 9 9 9 9 9 9 0 0 0 0 0"},
    {"input": "0 0 0 7 7 7 7 7 7 7 7 0", "output": "0 0 7 7 7 7 7 7 7 7 0 0"},
    {"input": "2 2 0 0 0 0 0 0 2 2 2 2", "output": "2 0 0 0 0 0 0 2 2 2 2 2"},
    {"input": "4 4 0 4 4 4 4 4 4 4 4 4", "output": "4 0 4 4 4 4 4 4 4 4 4 4"},
    {"input": "4 4 4 4 4 4 4 0 0 0 0 0", "output": "4 4 4 4 4 4 0 0 0 0 0 4"},
]

# Verification
results = []
for i, ex in enumerate(train_examples):
    input_str = ex["input"]
    expected_output_str = ex["output"]

    # Parse
    parsed_input = parse_string(input_str)
    parsed_expected_output = parse_string(expected_output_str)

    # Transform
    transformed_list = transform_logic(parsed_input)

    # Format
    actual_output_str = format_list(transformed_list)

    # Compare
    match = (actual_output_str == expected_output_str)
    results.append({
        "example": i + 1,
        "input_str": input_str,
        "expected_output_str": expected_output_str,
        "parsed_input": parsed_input,
        "transformed_list": transformed_list,
        "actual_output_str": actual_output_str,
        "match": match,
        "input_length": len(parsed_input),
        "output_length": len(parsed_expected_output) # Should be same as input length
    })

# Print summary
print("Verification Results:")
for res in results:
    print(f"Example {res['example']}: Match={res['match']}, Input Length={res['input_length']}, Output Length={res['output_length']}")

# Check consistency
all_match = all(r['match'] for r in results)
consistent_length = all(r['input_length'] == r['output_length'] for r in results)

print(f"\nAll examples match: {all_match}")
print(f"Consistent lengths: {consistent_length}")
