


# CampusLoop

CampusLoop is a student-powered marketplace for buying, exchanging, or giving
away pre-owned college items. The Streamlit app connects to Supabase to store
marketplace listings and exchange requests.

## Features

- Browse listings with text search, category filtering, and price sorting.
- Publish an item with its description, category, condition, price, display
  name, and optional image URL.
- Send an exchange request to a listing's owner.
- Change a listing's status to **Available**, **Reserved**, or **Completed**.
- View requests for a selected listing.

## Requirements

- Python 3.9 or newer
- A Supabase project with the tables described below

## Setup

1. Clone or download this repository, then open a terminal in the project
   directory.
2. (Recommended) Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your Supabase project URL and
   API key:

   ```dotenv
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your-supabase-api-key
   ```

   Use the appropriate key for your Supabase setup. Never commit secrets or
   expose a `service_role` key in a client-facing app.

5. In Supabase, create the tables and columns expected by the app:

   **`listings`**

   | Column | Expected value |
   | --- | --- |
   | `id` | Unique identifier |
   | `title` | Text |
   | `description` | Text |
   | `category` | Text |
   | `condition` | Text |
   | `price` | Numeric |
   | `owner_name` | Text |
   | `image_url` | Text; nullable |
   | `status` | Text |
   | `created_at` | Timestamp, used to sort listings |

   **`exchange_requests`**

   | Column | Expected value |
   | --- | --- |
   | `id` | Unique identifier |
   | `listing_id` | Identifier for the related listing |
   | `requester_name` | Text |
   | `message` | Text |
   | `status` | Text |
   | `created_at` | Timestamp, used to sort requests |

   Configure the tables' permissions and Row Level Security policies to match
   your deployment. The app expects access to read listings and requests,
   create listings and requests, and update listing statuses.

6. Start the app:

   ```powershell
   streamlit run APP.py
   ```

## Database and access notes

This is a prototype without user authentication. The app does not associate
listings or requests with authenticated owners, and its interface can display
exchange requests to visitors. Carefully restrict Supabase access before
deploying it with real users or data; do not enable unrestricted public access
to private information.

## Dependencies

The project dependencies are listed in [`requirements.txt`](requirements.txt):
Streamlit, the Supabase Python client, and `python-dotenv`.