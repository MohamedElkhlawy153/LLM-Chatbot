# LLM Chatbot Project

A simple chatbot built using the **Groq API**, featuring a **FastAPI** backend and a **Streamlit** frontend. It supports conversation history, token usage display, execution time tracking, and is fully containerized with **Docker** for easy local deployment. The chatbot intelligently responds in the same language as the input query (Arabic or English), making it versatile for multilingual use.

## Project Structure

```
/chatbot
├── backend/
│   ├── app.py               # FastAPI backend handling Groq API requests and logging
│   └── .env                # Environment variables (not committed to Git)
├── frontend/
│   └── ui.py               # Streamlit frontend with chat interface and analytics
├── requirements.txt         # List of Python dependencies
├── .gitignore              # Files to exclude from Git (e.g., .env, logs)
├── api.log                 # Log file for API requests and responses (not committed)
├── Dockerfile              # Configuration for building the Docker image
├── docker-compose.yml      # Configuration for running multiple Docker containers
└── README.md               # Project documentation
```

## Prerequisites

- **Python 3.9+** (for non-Docker setup)
- **Docker and Docker Compose** (for containerized deployment)
- A **Groq API key** (obtain one at [Groq Console](https://console.groq.com))

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/LLM-Chatbot.git
cd LLM-Chatbot
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory with the following content:

```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
```

- Replace `your_groq_api_key_here` with your actual Groq API key.
- **Important:** Do not commit the `.env` file to Git (it is ignored via `.gitignore`).

### 3. Non-Docker Setup (Optional)

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend:

   ```bash
   uvicorn backend.app:app --host 0.0.0.0 --port 8000
   ```

5. Run the frontend (in a separate terminal):

   ```bash
   streamlit run frontend/ui.py
   ```

### 4. Docker Setup (Recommended)

1. Ensure **Docker** and **Docker Compose** are installed and running.
2. Build and run the application with a single command:

   ```bash
   docker-compose up --build
   ```

   This creates two containers:
   - Backend (port `8000`)
   - Frontend (port `8501`)

## Access

- **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI for API documentation)
- **Frontend UI**: [http://localhost:8501](http://localhost:8501) (Interactive Streamlit interface)

## Features

- **Backend**:
  - Built with **FastAPI** for robust API handling.
  - Integrates with **Groq API** for chatbot responses.
  - Uses **Pydantic** for input validation.
  - Logs requests and responses to `api.log`.

- **Frontend**:
  - Built with **Streamlit** for a user-friendly chat interface.
  - Displays conversation history, token usage, and execution time.
  - Styled for an enhanced user experience.

- **Deployment**:
  - Fully containerized with **Docker** and **Docker Compose**.
  - Supports easy local deployment.

- **Language Support**:
  - Automatically responds in the same language as the input (Arabic or English).

## Challenges

- **Groq API Connectivity**: Managing rate limits and ensuring stable API responses.
- **Docker Networking**: Configuring communication between frontend and backend containers.
- **UI Styling**: Enhancing the Streamlit interface for better usability and aesthetics.

## Future Improvements

- Add **SQLite database** for persistent conversation history.
- Implement **retry logic** for handling API failures.
- Enhance the UI with interactive features (e.g., theme switching, advanced analytics).
```
