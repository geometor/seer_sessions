
## example 1
*input:*
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 5 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
6 6 7
0 5 7
4 4 0
```
*transformed output:*
```
6 6 5 5 4 4 7 5 7
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0 0
0 0 5 0 7 5 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 2 2 0 0 3 3 3 0 0
0 0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
6 2 2
7 5 7
3 3 3
```
*transformed output:*
```
6 5 7 5 7 5 2 2 3 3 3 5
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0
1 5 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 2 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 9 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
0 1 1
1 5 2
9 9 2
```
*transformed output:*
```
1 1 1 5 5 2 2 5 9 9
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
