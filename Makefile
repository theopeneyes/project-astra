install: 
	pip install -r requirements.txt 

lint: 
	pylint --disable=R,C *.py 

serve: 
	uvicorn main:app --reload & sleep 4

test: 
	python -m pytest -vv test.py 