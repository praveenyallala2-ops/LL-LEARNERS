# 🎓 Curriculum Generator Dashboard

An AI-powered web application that generates comprehensive, semester-wise educational curricula using the Groq API. Built with Flask, this tool helps educators create structured learning plans tailored to specific educational levels, skills, and industry focuses.

## ✨ Features

- 🤖 **AI-Powered Generation**: Uses Groq's LLaMA 3.1 model for intelligent curriculum planning
- 📅 **Semester-Wise Planning**: Generate complete multi-semester curricula with weekly breakdowns
- 🔒 **User Authentication**: Secure login and registration system with bcrypt password hashing
- 📄 **PDF Export**: Generate professional PDF documents with custom branding and logos
- 🎨 **Modern UI**: Clean and intuitive interface for curriculum generation
- 🏢 **Industry Alignment**: Customize curricula based on specific industry requirements

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Groq API key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/praveenyallala2-ops/LL-LEARNERS.git
   cd LL-LEARNERS
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-bcrypt python-dotenv groq reportlab
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## 📖 Usage

1. **Register/Login**: Create an account or log in to access the dashboard
2. **Generate Curriculum**: Fill in the form with:
   - Educational Level (e.g., Undergraduate, Graduate)
   - Skill/Course Name (e.g., Data Science, Web Development)
   - Number of Semesters
   - Weekly Hours
   - Industry Focus
3. **View Results**: The AI will generate a complete week-by-week curriculum
4. **Export to PDF**: Add your institution's branding and download as PDF

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Authentication**: Flask-Bcrypt
- **Database**: SQLite3
- **AI Model**: Groq API (LLaMA 3.1)
- **PDF Generation**: ReportLab
- **Environment Management**: python-dotenv

## 📁 Project Structure

```
LL-LEARNERS/
├── app.py                  # Main Flask application
├── templates/              # HTML templates
│   ├── index.html         # Main dashboard
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   └── branding.html      # PDF branding page
├── static/                # Static assets (images)
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🔐 Security Notes

- Never commit your `.env` file to version control
- The `.gitignore` file is configured to exclude sensitive data
- If you accidentally expose your API key, revoke it immediately and generate a new one
- Change the `app.secret_key` in production to a secure random string

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Praveen Yallala**
- GitHub: [@praveenyallala2-ops](https://github.com/praveenyallala2-ops)

## 🙏 Acknowledgments

- Groq API for providing the AI model
- Flask community for the excellent web framework
- ReportLab for PDF generation capabilities

---

**Note**: This application requires an active internet connection to communicate with the Groq API for curriculum generation.
