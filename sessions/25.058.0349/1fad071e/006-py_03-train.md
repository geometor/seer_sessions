
## example 1
*input:*
```
0 0 0 0 2 2 0 0 1
0 1 1 0 2 2 0 0 0
0 1 1 0 0 0 0 2 2
0 0 0 0 0 0 0 2 2
1 0 2 2 0 0 0 0 0
0 0 2 2 0 1 1 0 0
0 0 0 0 0 1 1 0 0
0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1
```
*expected output:*
```
1 1 0 0 0
```
*transformed output:*
```
12 9 9 0 0
```
size: True
palette: False
color count: False
pixels off: 3
**FAILED!**

## example 2
*input:*
```
1 1 0 2 0 0 0 0 2
1 1 0 0 0 1 1 0 0
0 0 0 2 0 1 1 0 0
0 0 0 0 0 0 0 0 1
0 1 1 0 2 2 0 0 0
0 1 1 0 2 2 0 0 2
0 0 0 0 0 0 0 0 0
0 0 0 2 2 0 1 1 0
0 1 0 2 2 0 1 1 0
```
*expected output:*
```
1 1 1 1 0
```
*transformed output:*
```
18 9 9 0 0
```
size: True
palette: False
color count: False
pixels off: 4
**FAILED!**

## example 3
*input:*
```
2 2 0 1 1 0 0 0 0
2 2 0 1 1 0 0 1 1
1 0 0 0 0 0 0 1 1
0 2 2 0 0 0 0 0 0
0 2 2 0 1 1 0 1 0
0 0 0 0 1 1 0 0 0
0 0 0 0 2 0 0 0 0
0 1 1 0 0 0 0 2 2
0 1 1 0 0 1 0 2 2
```
*expected output:*
```
1 1 1 1 0
```
*transformed output:*
```
19 9 9 0 0
```
size: True
palette: False
color count: False
pixels off: 4
**FAILED!**
