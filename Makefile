install: 
	pip install -r requirements.txt	

lint:
	pylint --disable=R,C *.py 

serve:
	uvicorn main:app --reload & sleep 2

test:
	pytest test.py 