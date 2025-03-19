
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1
0 0 0 5 0 0 0 1 1 0
0 0 0 1 0 0 0 0 1 0
0 0 1 1 1 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 1 1 0 0
```
*expected output:*
```
0 1 0
1 1 1
0 1 1
```
*transformed output:*
```
0 1 1
1 1 1
0 1 1
```
size: True
palette: True
color count: False
pixels off: 1
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 4 4 0 0
0 0 4 0 0 0 0 0 4 0
0 4 0 4 0 0 0 4 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
4 4 0
0 0 4
0 4 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: min() iterable argument is empty

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 5 0 0
0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 2 2
2 2 0
0 2 0
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: min() iterable argument is empty
