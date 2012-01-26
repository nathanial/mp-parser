for f in $(ls data)
do
    python.exe parser.py $f
done