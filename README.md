# AI Study Partner

An AI-powered study partner application designed to help users manage their study tasks effectively. Built with Streamlit for the web interface, SQLite for data storage, and integrated with LangChain and Groq for AI-driven features like explanations and embeddings.

## Features

- **Task Management**: Add, view, update, and delete study tasks with assigned dates and periods (day, week, month, year).
- **Daily Checklist**: Sidebar interface for quick task status updates and progress tracking.
- **Upcoming Tasks**: View tasks scheduled for the next 7 days.
- **Auto-Move Pending Tasks**: Automatically move unfinished tasks to the next day.
- **AI Integration**: Use LLM (via Groq) for generating explanations or insights on study topics.
- **Embeddings Support**: Setup for vector embeddings using HuggingFace models and Qdrant for advanced search capabilities.


## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd ai_study_partner
   ```

2. **Install Python Dependencies**:
   Ensure you have Python 3.8+ installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. **Environment Variables**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   Obtain your API key from [Groq](https://groq.com/).

2. **Database**:
   The application uses SQLite, and the database file (`database/tasks.db`) will be created automatically on first run.

## Usage

1. **Run the Application**:
   ```bash
   streamlit run task_planner/main.py
   ```
   This will start the Streamlit server, and you can access the app in your browser at `http://localhost:8501`.

2. **Using the App**:
   - **Sidebar**: View today's tasks, mark them as done, and save statuses. Pending tasks can be moved to tomorrow.
   - **Main Page**: Add new tasks with titles, dates, and periods. View upcoming tasks and delete if needed.
   



## Project Structure

```
ai_study_partner/
├── .gitignore                 # Git ignore file (excludes .env)
├── README.md                  # This file
├── requirements.txt           # Pythondependencies             
├── database/
│   └── tasks.db               # SQLite database for tasks
├── task_planner/
│   ├── main.py                # Main Streamlit application
│   ├── tasks.py               # TaskManager class for database operations
│   ├── schedular.py           # Script for moving pending tasks
│   └── utils/
│       └── date_utils.py      # Date utility functions
└── utils/
    ├── llm_utils.py           # LLM setup with Groq
    └── embeddings.py          # Embeddings setup with HuggingFace
```

## Dependencies

- `langchain`: For AI chain management
- `langchain-groq==0.2.0`: Groq integration for LangChain
- `streamlit`: Web app framework
- `qdrant-client`: Vector database client
- `python-dotenv`: Environment variable management
- `groq`: Groq API client
- `langchain-community`: Community extensions for LangChain

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.


