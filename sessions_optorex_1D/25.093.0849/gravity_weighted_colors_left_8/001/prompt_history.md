
## train_1

**input:**
```
1 2 1 2 1 0 0 0 0 2 0 0
```


**output:**
```
0 0 0 0 0 0 1 1 1 2 2 2
```


## train_2

**input:**
```
2 0 1 0 2 1 0 0 0 0 1 0
```


**output:**
```
0 0 0 0 0 0 0 1 1 1 2 2
```


## train_3

**input:**
```
1 2 0 2 1 0 0 1 2 1 0 2
```


**output:**
```
0 0 0 0 1 1 1 1 2 2 2 2
```


## train_4

**input:**
```
2 1 0 1 0 0 2 0 1 1 1 1
```


**output:**
```
0 0 0 0 1 1 1 1 1 1 2 2
```


## train_5

**input:**
```
0 2 2 0 1 0 0 0 1 1 2 1
```


**output:**
```
0 0 0 0 0 1 1 1 1 2 2 2
```


## train_6

**input:**
```
0 1 1 1 0 0 2 0 2 0 0 2
```


**output:**
```
0 0 0 0 0 0 1 1 1 2 2 2
```


## train_7

**input:**
```
2 1 0 1 1 1 0 1 2 0 2 2
```


**output:**
```
0 0 0 1 1 1 1 1 2 2 2 2
```

**Perception of Task Elements:**

The task involves transforming a sequence of integers. Both input and output are sequences of integers. The integers present in the sequences appear to be limited to 0, 1, and 2. The length of the input sequence and the output sequence is consistently 12 across all provided examples. A comparison of the input and output sequences reveals that the output sequence contains the same integers as the input sequence, but arranged in non-decreasing (ascending) order. The frequency of each integer (0, 1, and 2) remains the same between the input and its corresponding output.

**YAML Facts:**


```yaml
Task: SortSequence
Input:
  Type: Sequence
  Elements:
    Type: Integer
    Values: [0, 1, 2]
  Length: 12 (based on examples)
Output:
  Type: Sequence
  Elements:
    Type: Integer
    Values: [0, 1, 2]
  Length: Same as input length (12 based on examples)
  Property: Sorted in non-decreasing order
Relationship:
  - Action: Sorting
  - Constraint: The multiset of elements in the output sequence is identical to the multiset of elements in the input sequence.
  - Transformation: The output sequence is the result of sorting the input sequence in ascending order.
```


**Natural Language Program:**

1.  Receive the input sequence of integers.
2.  Sort the integers within the sequence in ascending order (0s first, then 1s, then 2s).
3.  Return the resulting sorted sequence.
