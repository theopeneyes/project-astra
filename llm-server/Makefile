install: 
	pip install -r requirements.txt 

lint: 
	pylint --disable=R,C *.py || true  

serve: 
	fastapi run main.py & sleep 10

test: 
	python -m pytest -vv test.py 