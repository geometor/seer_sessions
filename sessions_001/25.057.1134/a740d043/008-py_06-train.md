
## example 1
*input:*
```
1 1 1 1 1 1 1
1 2 2 1 1 1 1
1 2 2 3 1 1 1
1 1 1 2 1 1 1
1 1 1 1 1 1 1
```
*expected output:*
```
2 2 0
2 2 3
0 0 2
```
*transformed output:*
```
2 2 2
```
size: False
palette: True
color count: False
pixels off: None
**FAILED!**

## example 2
*input:*
```
1 1 1 1 1 1 1
1 1 3 1 2 1 1
1 1 3 1 2 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
```
*expected output:*
```
3 0 2
3 0 2
```
*transformed output:*
```
3 0 0
2 0 0
```
size: True
palette: True
color count: False
pixels off: 3
**FAILED!**

## example 3
*input:*
```
1 1 1 1 1 1
1 1 1 1 1 1
1 5 5 1 1 1
1 5 5 1 1 1
1 6 6 1 1 1
1 1 1 1 1 1
1 1 1 1 1 1
```
*expected output:*
```
5 5
5 5
6 6
```
*transformed output:*
```
6 5 0
```
size: False
palette: False
color count: False
pixels off: None
**FAILED!**
