.PHONY: help install clean eda score visualize pipeline api dashboard frontend docker docker-down all

help:
	@echo ""
	@echo "  Lead Scoring - Commandes disponibles"
	@echo "  ======================================"
	@echo ""
	@echo "  Setup:"
	@echo "    make install       Installer toutes les dependances (Python + React)"
	@echo ""
	@echo "  Data Pipeline:"
	@echo "    make clean         Nettoyer les donnees brutes"
	@echo "    make eda           Analyse exploratoire (genere les graphiques)"
	@echo "    make score         Calculer les scores des leads"
	@echo "    make visualize     Generer le dashboard et le classement"
	@echo "    make pipeline      Executer tout le pipeline (clean+eda+score+visualize)"
	@echo ""
	@echo "  Serveurs (local):"
	@echo "    make api           Lancer l'API FastAPI        -> http://localhost:8000"
	@echo "    make dashboard     Lancer le dashboard Streamlit -> http://localhost:8501"
	@echo "    make frontend      Lancer le frontend React     -> http://localhost:5173"
	@echo ""
	@echo "  Docker:"
	@echo "    make docker        Lancer tout avec Docker      -> http://localhost:3000"
	@echo "    make docker-down   Arreter les containers"
	@echo ""

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

docker:
	docker-compose up --build

docker-down:
	docker-compose down
