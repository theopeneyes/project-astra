install: 
	pip install -r requirements.txt 

lint: 
	pylint --disable=R,C *.py || true  

serve: 
	uvicorn main:app & sleep 4

test: 
	python -m pytest -vv test.py 