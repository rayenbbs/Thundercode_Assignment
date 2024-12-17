# Web QA Analyzer

An interactive web application for analyzing the quality of web pages from a QA perspective. The application evaluates various aspects of a webpage, including performance, accessibility, SEO, HTML structure, and security, providing actionable insights and recommendations.

Built with **Streamlit** and **CrewAI**.

---


## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

**Add your `API Keys` into the `.env` file following .env.example**

## Running the Project

Execute the following command to launch the Streamlit app:

```bash
streamlit run app.py  
```

