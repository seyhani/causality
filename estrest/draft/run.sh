DATA_ALL=data_c12_pi_all.csv
DATA_HALF=data_c12_pi_half.csv
PATHVERT=pathvert/pathvert.old.py
echo "n,N" > $DATA_ALL
echo "n,N" > $DATA_HALF
for i in {3..14}; do
    printf "Running for $i... "
    printf "$i\nall\n" |
        python cm.py |
        python $PATHVERT |
        python -c "a = [int(x) for x in input().split()]; print(f'{$i},{sum(a)/len(a)}')" >> $DATA_ALL
        printf "all, "
    printf "$i\nhalf\n" |
        python cm.py |
        python $PATHVERT |
        python -c "a = [int(x) for x in input().split()]; print(f'{$i},{sum(a)/len(a)}')" >> $DATA_HALF
        printf "half, "
    printf "done!\n"
done