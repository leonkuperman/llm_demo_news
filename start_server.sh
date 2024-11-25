#! /bin/bash
source venv/bin/activate

venv/bin/uvicorn main:app --reload