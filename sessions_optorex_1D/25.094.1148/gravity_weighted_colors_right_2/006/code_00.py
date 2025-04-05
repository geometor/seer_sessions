import collections
import re

def parse_input_string(s):
    # Remove brackets and split by space, then convert to int
    s = s.strip('[]')
    if not s: # Handle empty case like '[]'
        return []
    # Handle potential multiple spaces between numbers
    return [int(x) for x in re.split(r'\s+', s.strip())]

def format_output_list(lst):
    return " ".join(map(str, lst))

examples = [
    {'input': '[2 2 0 1 0 2 2 0 2 2 0 0]', 'output': '2 2 2 2 2 2 1 0 0 0 0 0'},
    {'input': '[2 0 2 2 0 0 0 0 2 2 1 2]', 'output': '2 2 2 2 2 2 1 0 0 0 0 0'},
    {'input': '[0 0 0 2 2 1 0 0 2 0 0 2]', 'output': '2 2 2 2 1 0 0 0 0 0 0 0'},
    {'input': '[2 0 0 1 2 1 1 0 2 2 1 0]', 'output': '2 2 2 2 1 1 1 1 0 0 0 0'},
    {'input': '[0 1 0 2 0 0 2 2 2 0 1 0]', 'output': '2 2 2 2 1 1 0 0 0 0 0 0'},
    {'input': '[0 1 1 0 0 2 0 1 2 2 2 0]', 'output': '2 2 2 2 1 1 1 0 0 0 0 0'},
    {'input': '[0 0 0 0 0 0 2 2 0 0 0 2]', 'output': '2 2 2 0 0 0 0 0 0 0 0 0'},
]

results = []
print("Example | Input Counts        | Output Counts       | Counts Preserved? | Logic Matches?")
print("--------|---------------------|---------------------|-------------------|---------------")
for i, ex in enumerate(examples):
    input_list = parse_input_string(ex['input'])
    input_counts = collections.Counter(input_list)

    sorted_list = sorted(input_list, reverse=True)
    simulated_output = format_output_list(sorted_list)

    expected_output_list = [int(x) for x in ex['output'].split()]
    output_counts = collections.Counter(expected_output_list)

    match = (simulated_output == ex['output'])
    count_match = (input_counts == output_counts)

    # Format counts for printing
    ic_str = f"0:{input_counts.get(0,0)}, 1:{input_counts.get(1,0)}, 2:{input_counts.get(2,0)}"
    oc_str = f"0:{output_counts.get(0,0)}, 1:{output_counts.get(1,0)}, 2:{output_counts.get(2,0)}"

    results.append({
        'example': i + 1,
        'input_counts': ic_str,
        'output_counts': oc_str,
        'logic_matches_output': match,
        'counts_preserved': count_match
    })
    print(f"{i+1:<7} | {ic_str:<19} | {oc_str:<19} | {str(count_match):<17} | {str(match)}")

# print(results) # Optional: print full dictionary