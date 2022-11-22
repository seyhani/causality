echo "n,N" > data
for i in {5..14}; do
    printf "Running for $i... "
    printf "$i\n" |
        python cm.py |
        python pathvert/pathvert.py |
        python -c "a = [int(x) for x in input().split()]; print(f'{$i},{sum(a)/len(a)}')" >> data
    printf "done!\n"
done