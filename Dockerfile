# Step 1: Build the React frontend
FROM node:16-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy the React project files
COPY news-dashboard/package*.json ./
COPY news-dashboard/ ./

# Install dependencies and build the React app
RUN npm install
RUN npm run build

# Step 2: Build the Python FastAPI backend
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy built frontend to the backend directory
COPY --from=frontend-builder /app/frontend/build /app/frontend/build

# Expose only the backend port
EXPOSE 8000

# Command to run the backend (serves both API and frontend)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]