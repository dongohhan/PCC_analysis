# PCC_analysis
PCC_analysis with bait  &amp; matrix

## bait_list format

```
Gene A
Gene B
Gene C
```

## Usage

```
python PCC_analysis.py \
-input_gene bait_list.csv \
-input_matrix matrix.tsv
```

## Output format

```
Bait      Score
Gene X    0.92
Gene Y    0.90
Gene Z    0.89
```
