
## example 1
*input:*
```
1 0 0
2 1 0
0 0 1
```
*expected output:*
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
2 1 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
*transformed output:*
```
1 0 0 1 0 0
2 1 0 2 1 0
0 0 1 0 0 1
1 0 0 1 0 0
2 1 0 2 1 0
0 0 1 0 0 1
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
0 1 2
1 1 0
2 0 0
```
*expected output:*
```
0 0 0 0 0 0 0 1 2
0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 1 2 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0
```
*transformed output:*
```
0 1 2 0 1 2
1 1 0 1 1 0
2 0 0 2 0 0
0 1 2 0 1 2
1 1 0 1 1 0
2 0 0 2 0 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 3
*input:*
```
2 1 2
0 2 1
2 1 0
```
*expected output:*
```
2 1 2 0 0 0 2 1 2
0 2 1 0 0 0 0 2 1
2 1 0 0 0 0 2 1 0
0 0 0 2 1 2 0 0 0
0 0 0 0 2 1 0 0 0
0 0 0 2 1 0 0 0 0
2 1 2 0 0 0 0 0 0
0 2 1 0 0 0 0 0 0
2 1 0 0 0 0 0 0 0
```
*transformed output:*
```
2 1 2 2 1 2
0 2 1 0 2 1
2 1 0 2 1 0
2 1 2 2 1 2
0 2 1 0 2 1
2 1 0 2 1 0
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**
