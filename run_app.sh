#!/bin/bash
cd /home/user/Voynich
while true; do
    streamlit run app.py --server.port=8501
    echo "App crashed, restarting in 5 seconds..."
    sleep 5
done
