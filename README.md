FastAPI Simple SKU

# Install requirements
pip install -r requirements.txt


# Run Service
uvicorn main:app


# Browse Api/Reading Docs
127.0.0.1:8000/docs


#Project structure


::
	app
	├── api/v1           - web routes
	│	├── item         - item routes
	│	└── item_type    - item type routes
	├── db               - db related stuff
	│	├── crud         - crud methods
	│	├── models       - db models
	│	└── schema       - serializers 
	├── tests            - api tests 
	├── config.py        - config for app
	└── main.py          - FastAPI app creation and configuration  