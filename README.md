## CampusLoop — CrackTheCode

## About the Project

CampusLoop is a student marketplace built to help students buy, sell, and exchange items within their campus community. It encourages reuse, affordability, and a more sustainable campus environment.

## Live Demo

* **Deployed App:** https://campusloop.streamlit.app/
* **YouTube Demo:** [[Insert your unlisted YouTube video link here](https://youtu.be/FvJ7wbj68KM?si=2bYmTY0e6tvIjLS5)]

## Features

* Browse available campus listings
* Search listings by keywords
* Filter listings by category
* Sort listings by newest or price
* Create marketplace listings
* Submit exchange requests
* Track listing status, including Available, Reserved, and Completed
* Persistent data storage using Supabase

## Tech Stack

* **Language:** Python
* **Frontend / App Framework:** Streamlit
* **Database:** Supabase
* **Environment Configuration:** python-dotenv
* **Version Control:** Git and GitHub

## Installation and Local Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/YOUR-GITHUB-USERNAME/CrackTheCode.git
   ```
2. Enter the project folder:

   ```bash
   cd CrackTheCode
   ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root and add your Supabase credentials:

   ```dotenv
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```
5. Start the app:

   ```bash
   streamlit run APP.py
   ```

## Security Note

Never commit `.env` or expose Supabase credentials publicly. Configure secrets securely when deploying.

## Team

**Team Name:** CrackTheCode