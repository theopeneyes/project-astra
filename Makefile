serve: 
	uvicorn main:app --reload & sleep 5

lint:
	pylint --disable=R,C *.py || true 

test: 
	pytest test.py 

install: 
	pip install -r requirements.txt 
