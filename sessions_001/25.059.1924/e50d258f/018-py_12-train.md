
## example 1
*input:*
```
0 0 0 0 0 0 8 8 8 8
0 8 8 8 8 0 8 2 2 8
0 8 1 8 8 0 8 8 8 8
0 8 8 2 8 0 8 2 1 8
0 8 8 8 8 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 0
0 0 0 8 8 8 2 8 8 0
0 0 0 8 2 8 1 8 8 0
0 0 0 8 1 8 8 8 8 0
```
*expected output:*
```
8 8 8 8
8 2 2 8
8 8 8 8
8 2 1 8
8 8 8 8
```
*transformed output:*
```
1
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
1 1 1 8 0 0 0 0 0 0
1 8 1 1 0 1 8 8 1 8
8 2 8 1 0 8 1 8 2 8
1 1 1 8 0 8 8 8 8 1
8 1 8 8 0 8 1 2 8 2
0 0 0 0 0 8 8 8 1 8
0 0 0 0 0 1 1 8 1 8
0 8 2 2 0 8 1 1 8 2
0 2 2 1 0 0 0 0 0 0
0 2 1 8 0 0 0 0 0 0
```
*expected output:*
```
8 2 2
2 2 1
2 1 8
```
*transformed output:*
```
8
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
2 8 8 8 0 0 0 0 0 0
8 8 1 8 0 0 0 0 0 0
1 8 8 8 0 0 0 0 0 0
8 8 8 2 0 0 1 8 8 2
8 2 8 1 0 0 8 8 1 8
8 1 8 8 0 0 8 2 8 8
0 0 0 0 0 0 8 8 8 1
0 0 0 0 0 0 1 8 8 8
0 0 0 0 0 0 8 8 1 8
0 0 0 0 0 0 0 0 0 0
```
*expected output:*
```
2 8 8 8
8 8 1 8
1 8 8 8
8 8 8 2
8 2 8 1
8 1 8 8
```
*transformed output:*
```
2
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
