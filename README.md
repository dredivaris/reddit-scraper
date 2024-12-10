# Reddit Data Scraper 📊

![Screenshot 2024-12-10 162954](https://github.com/user-attachments/assets/65a9c7be-359b-48aa-9104-55b43fe0d351)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io)
[![PRAW](https://img.shields.io/badge/PRAW-7.7.1-orange.svg)](https://praw.readthedocs.io)
[![Pandas](https://img.shields.io/badge/Pandas-2.1.1-150458.svg)](https://pandas.pydata.org)

A powerful Reddit data scraping tool with a user-friendly Streamlit interface. Extract posts and comments from subreddits or specific posts with ease.

## 🚀 Features

- 📱 User-friendly web interface
- 🔍 Scrape posts from any subreddit
- 💬 Extract comments from specific posts
- 📊 Export data to CSV
- ⏱️ Time-based filtering
- 🔄 Caching for better performance

## 🛠️ Tech Stack

- **Python** - Core programming language
- **Streamlit** - Web interface framework
- **PRAW** - Reddit API wrapper
- **Pandas** - Data manipulation and analysis
- **python-dotenv** - Environment variable management

## 📋 Prerequisites

- Python 3.9 or higher
- Reddit API credentials ([Get them here](https://www.reddit.com/prefs/apps))

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/pakagronglb/reddit-scraper.git
cd reddit-scraper
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

## 🚀 Usage

1. Start the application:
```bash
streamlit run main.py
```

2. Access the web interface at `http://localhost:8501`

3. Choose your scraping option:
   - **Subreddit Posts**: Enter subreddit name, post limit, and time filter
   - **Specific Post**: Enter the Reddit post URL

4. Click "Scrape" and download the results as CSV

## 🌐 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add your Reddit API credentials in Streamlit secrets

### Heroku

1. Create a Heroku app:
```bash
heroku create your-app-name
```

2. Set environment variables:
```bash
heroku config:set REDDIT_CLIENT_ID=your_client_id
heroku config:set REDDIT_CLIENT_SECRET=your_client_secret
heroku config:set REDDIT_USER_AGENT=your_user_agent
```

3. Deploy:
```bash
git push heroku main
```

## 📝 Configuration

- `requirements.txt` - Project dependencies
- `.env` - Local environment variables
- `Procfile` - Heroku deployment configuration
- `runtime.txt` - Python runtime specification

## 🔒 Security

- Never commit your `.env` file or `.streamlit/secrets.toml`
- Use environment variables for sensitive data
- Keep your Reddit API credentials secure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [PRAW Documentation](https://praw.readthedocs.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Reddit API Documentation](https://www.reddit.com/dev/api/)

## 📧 Contact

Your Name - [@pakagronglb](https://twitter.com/pakagronglb)

Project Link: [https://github.com/pakagronglb/reddit-scraper](https://github.com/pakagronglb/reddit-scraper)
