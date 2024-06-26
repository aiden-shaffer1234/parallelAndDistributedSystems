touch temp.txt
for i in  {1...200}
do
    python3 mapper.py < input.txt >> temp.txt
done

python3 reducer.py < temp.txt
rm temp.txt