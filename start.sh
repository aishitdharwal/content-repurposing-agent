#!/bin/bash
python -c "from health_check import run_health_check_server; run_health_check_server()" &
streamlit run app.py --server.port=8080 --server.address=0.0.0.0 --server.headless=true
