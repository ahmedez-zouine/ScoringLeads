.PHONY: install clean eda score visualize api dashboard frontend all

install:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

clean:
	. venv/bin/activate && cd src && python clean_data.py

eda:
	. venv/bin/activate && cd src && python eda.py

score:
	. venv/bin/activate && cd src && python score_leads.py

visualize:
	. venv/bin/activate && cd src && python visualize.py

pipeline: clean eda score visualize

api:
	. venv/bin/activate && uvicorn api:app --reload --port 8000

dashboard:
	. venv/bin/activate && streamlit run dashboard.py

frontend:
	cd frontend && npm run dev

all:
	@echo "Run in 3 separate terminals:"
	@echo "  make api        -> http://localhost:8000"
	@echo "  make dashboard  -> http://localhost:8501"
	@echo "  make frontend   -> http://localhost:5173"
