file_=`echo $1|cut -d/ -f2`
if [ "$2dai" != "dai" ]
then
python pyNmonAnalyzer.py -bx -o  res/$2/${file_} -t static -i $1
else
python pyNmonAnalyzer.py -bx -o  res/${file_} -t static -i $1
fi
if [ $? -eq 0 ]
then 
echo 'OK'
fi
