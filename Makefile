dependencies:
	python3 -m venv venv
	venv/bin/python/ -m pip install requirements.txt
	cd frontend/
	npm i


back:
	cd backend/ ; \
		../venv/bin/python manage.py runserver 0.0.0.0:8000

front:
	cd frontend/ ; \
		npm run net

