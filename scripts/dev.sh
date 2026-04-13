#!/bin/bash

echo "Starting development server..."

(cd backend && poetry run uvicorn app.main:app --reload) &
(cd frontend && npm run dev) &

echo "Development server started" 

wait

