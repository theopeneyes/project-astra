serve: 
	uvicorn main:app --reload & sleep 5

lint: 
	pylint --disable=R,C *.py 

test: 
	pytest test.py 

install: 
	pip install -r requirements.txt 
