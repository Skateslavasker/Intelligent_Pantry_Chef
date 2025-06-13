# 🧠 Intelligent Pantry Chef

**Zero-Waste AI Cooking Assistant**  
Turn your pantry into possibilities! Upload ingredients (text or image), and get AI-curated recipes, nutritional analysis, and cooking instructions – all personalized and interactive.

---

## 📚 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [CI/CD & Docker](#cicd--docker)
- [Code Structure](#code-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

---

## 🍳 Features

- 🥕 **Ingredient Input**: Add items via text or image (fridge snapshot).
- 🤖 **AI Recipe Generation**: Uses LLMs with retrieval & fallback logic to suggest cooking options.
- 🍽️ **Step-by-Step Instructions**: Easy-to-follow cooking directions.
- 🔍 **Nutrition Breakdown**: Per-ingredient and total dish analysis.
- 🛠️ **Fallback-Resilient Agents**: Built-in backup tools for reliability.
- 🔐 **Google OAuth2 + JWT Login**: Secure, personalized access and future favorites tracking.
- 🐳 **Dockerized App**: Ready-to-deploy backend & frontend containers.
- ⚙️ **CI/CD Pipeline**: GitHub Actions automates linting, building, and pushing Docker images to GHCR.

---

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- pip
- Node.js (for frontend enhancements, optional)
- A `.env` file with API keys (see below)
- Docker (optional but recommended)

### Clone the repo
```bash
git clone https://github.com/Skateslavasker/Intelligent_Pantry_Chef.git
cd Intelligent_Pantry_Chef
```

### Create virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Add `.env` file
Create a `.env` file in the root directory with the following:

```env
TOGETHER_API_KEY=your_together_api_key
OPENAI_API_KEY=your_openai_api_key
NINJAS_RECIPE_API_KEY=your_ninjas_key
EDAMAM_API_KEY=your_edamam_key
EDAMAM_API_HOST=edamam_host_url
IMGBB_API_KEY=your_imgbb_key
GOOGLE_CLIENT_ID=your_google_oauth_client_id
GOOGLE_CLIENT_SECRET=your_google_oauth_secret
JWT_SECRET=your_custom_jwt_secret
FRONTEND_URL=http://localhost:8501
```

---

## 💻 Usage

### 1. Run the Auth Server (FastAPI)
```bash
uvicorn auth_server:app --reload --port 8000
```

### 2. Start the Streamlit App
```bash
streamlit run app.py
```

### 3. Log in and Explore
- Visit [http://localhost:8501](http://localhost:8501)
- Log in with Google
- Input ingredients or upload a fridge image
- Browse recipes and nutrition breakdowns

---

## 🔁 CI/CD & Docker

### 🧪 Continuous Integration (CI)
Every push or pull request automatically triggers:
- Python linting via `flake8`
- Docker build check for both backend and frontend

### 📦 Continuous Delivery (CD)
On every push to `main`, GitHub Actions:
- Logs into GitHub Container Registry (GHCR)
- Builds & pushes:
  - `ghcr.io/<username>/pantry-auth:latest`
  - `ghcr.io/<username>/pantry-frontend:latest`

> Images are always ready for deployment via Docker or cloud hosting platforms.

### 🐳 Local Docker Build (Optional)
```bash
docker build -t pantry-auth -f backend/Dockerfile .
docker build -t pantry-frontend -f Dockerfile .
```

---

## 🧾 Code Structure

```
├── app.py                   # Streamlit UI and user logic
├── auth_server.py          # FastAPI server for Google OAuth + JWT
├── pantry_agent.py         # LangChain agent orchestration
├── llm_tool.py             # LLM wrappers and tool interfaces
├── vision_tool.py          # Image-to-ingredient logic
├── nutrition_tool.py       # Nutrition API wrapper
├── recipe_tool.py          # Recipe API wrapper
├── fallback_handlers.py    # Fallback logic for LLM agents
├── recipe_schema.py        # JSON Schema for output validation
├── generate_recipe.py      # Recipe generation logic
├── image_to_ingr.py        # Image processing pipeline
├── nutrition_api.py        # Nutrition query interface
├── recipe_api.py           # REST hooks for recipe retrieval
├── .env                    # Environment variables (not committed)
├── Dockerfile              # Frontend Docker build
├── backend/Dockerfile      # Backend Docker build
└── requirements.txt        # Project dependencies
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/awesome`).
3. Commit your changes (`git commit -m 'Add something amazing'`).
4. Push to the branch (`git push origin feature/awesome`).
5. Open a Pull Request.

Please follow [PEP8](https://peps.python.org/pep-0008/) and use clear commit messages. Testing and documentation are highly appreciated.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software with attribution.

---

## 🙌 Acknowledgements

- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)
- [Together AI](https://www.together.ai/)
- [Edamam API](https://developer.edamam.com/)
- [API Ninjas](https://api-ninjas.com/)
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [GitHub Actions](https://github.com/features/actions)
- [GHCR (GitHub Container Registry)](https://ghcr.io)

---

## 📬 Contact

Feel free to reach out:

- GitHub Issues: [Open an issue](https://github.com/Skateslavasker/Intelligent_Pantry_Chef/issues)
- Email: revanthnaik12@gmail.com
