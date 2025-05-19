# ReplyGen 🤖

An intelligent agent that reply to the user from understanding the post and platform


## Features

- Reply To User Post

## Tech Stack

- Backend: Python
- LLM Integration: Groq (Claude 3.5 Sonnet)
- API: FastAPI
- Storage: TIDB(SQL Database)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/KetuPatel806/Replygen.git
cd Replygen
```

2. Create the virtual environment:
```bash
conda create -p venv python==3.12 -y
```

3. Activate virtual environment:
```bash
conda activate venv/
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file and add required environment variables:
```
GROQ_API_KEY=your_api_key_here
TIDB_HOST = host
TIDB_PASSWORD = password_here
TIDB_USER = username
TIDB_DATABASE = database_name
```

## Usage

1. Start the application:
```bash
uvicorn app:app --reload
```

2. Navigate to http://127.0.0.1:8000 in your browser

3. Endpoint is /reply 

4. Else use the swagger UI http://127.0.0.1:8000/docs

4. Follow the guided SDLC process:
   - Enter the Platform[Twitter,Linkedin,Instagram]
   - Enter the Post_text

## Project Structure

```
Replygen
├── app.py              # Fast_API
├── src/
│   ├── logger/         # Logging Module
│   ├── graph/          # Graph of the Project
│   ├── node/           # Graph Nodes
│   ├── notebook/       # Jupyter Notebook
│   ├── state/          # States
│   ├── tools           # RAG Tool
├── requirements.txt   # Project dependencies
└── .env              # Environment variables
```

## Contributing

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```
3. Commit your changes:
```bash
git commit -am 'Add some feature'
```
4. Push to the branch:
```bash
git push origin feature/your-feature-name
```
5. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com)
- Powered by [Groq](https://groq.com/)