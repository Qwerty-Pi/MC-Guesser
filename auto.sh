for y in {1980..2000};
do
	#fail=1
	#while [[ fail -ne 0 ]];
	#do
	#	paper=paper-2/$y
	# ./parse $paper
	#	python3 ask_gemini.py $paper statement
	#	fail=$?
	#done
	./compile $y --fix
	# python3 ask_gemini.py $paper topic
done
