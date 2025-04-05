Okay, let's break down the transformation logic.

**Perception of Task Elements:**

*   The input and output are both sequences (lists) of single-digit integers.
*   The length of the output list is always the same as the length of the input list.
*   The transformation involves rearranging the elements of the input list. Specifically, the position of the *last* element seems to change based on its value, while the relative order of the other elements is preserved.
*   There appear to be two distinct transformation behaviors, conditional on whether the last element of the input is zero or non-zero.

**Facts (YAML):**


```yaml
objects:
  - name: input_list
    type: List[int]
    description: The input sequence of integers.
  - name: output_list
    type: List[int]
    description: The transformed sequence of integers.
  - name: last_element
    type: int
    description: The integer value at the last position of the input_list.
  - name: base_list
    type: List[int]
    description: The input_list excluding its last element.
properties:
  - object: last_element
    name: value
    description: The numerical value of the last element (specifically whether it is 0 or not).
  - object: base_list
    name: first_non_zero_index
    description: The index of the first element in the base_list that is not 0. If all elements are 0, this index is considered 0.
relationships:
  - type: derivation
    source: input_list
    target: last_element
    description: last_element is the final item in input_list.
  - type: derivation
    source: input_list
    target: base_list
    description: base_list consists of all elements of input_list except the last one.
actions:
  - name: remove_last
    object: input_list
    result: base_list, last_element
    description: Separate the input_list into the last_element and the remaining base_list.
  - name: find_insertion_point
    object: base_list
    condition: last_element == 0
    result: index
    description: Determine the index of the first non-zero element in the base_list (or index 0 if none exists).
  - name: insert_element
    target: base_list
    element: last_element
    position: index
    result: output_list
    description: Insert the last_element into the base_list at a specific index (either index 0 or the first_non_zero_index) to produce the output_list.
conditions:
  - name: check_last_element_value
    based_on: last_element.value
    outcomes:
      - value_is_zero: Determines the insertion logic (find first non-zero index).
      - value_is_non_zero: Determines the insertion logic (insert at beginning).
```


**Natural Language Program:**

1.  Examine the input list and identify its last element.
2.  Create a temporary list containing all elements from the input list *except* the last one, maintaining their original relative order.
3.  Check the value of the identified last element:
    *   **If the last element is 0:** Find the index of the first element in the temporary list that is not zero. If all elements in the temporary list are zero, use index 0. Insert the original last element (the 0) into the temporary list at this determined index.
    *   **If the last element is not 0:** Insert the original last element at the very beginning (index 0) of the temporary list.
4.  The modified temporary list is the final output list.