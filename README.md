# Recipe App

Welcome to the Recipe App! This Django-based web application allows users to browse, search, and add recipes while providing data visualizations to enhance user experience.

## Features

- **User Authentication**: Secure login and logout functionality for users.
- **Recipe Management**:
  - View all recipes.
  - Add new recipes (authenticated users only).
  - Search recipes by name or ingredients.
- **Data Visualizations**:
  - Bar chart: Displays recipes by cooking time.
  - Pie chart: Shows recipes categorized by difficulty.
  - Line chart: Tracks recipes created over time.
- **About Me Page**: A dedicated page with developer information and portfolio links.

## Installation

### Prerequisites

- Python 3.8+
- Django 4.2.16
- pip

### Setup Steps

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd recipe-app
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

## Usage

### Adding Recipes
- Log in to the application.
- Click on the "Add Recipe" button.
- Fill in the form and submit your recipe.

### Viewing Data Visualizations
- Use the search functionality to filter recipes by name or ingredient.
- Select a chart type to generate visual insights.

### About Me Page
Visit the "About Me" page for information about the developer and links to the portfolio, GitHub, and contact details.

## Folder Structure

```plaintext
recipe-app/
├── recipes/              # Main app containing views, models, and templates
│   ├── migrations/       # Database migrations
│   ├── templates/        # HTML templates
│   │   ├── recipes/      # Templates for the recipes app
│   │       ├── recipes_list.html
│   │       ├── add_recipe.html
│   │       └── about_me.html
│   ├── static/           # Static files (CSS, images, JS)
│   ├── forms.py          # Django forms for user input
│   ├── views.py          # Application views
│   └── tests.py          # Unit tests
├── manage.py             # Django's CLI utility
└── requirements.txt      # Python dependencies
```

## Running Tests

To run the unit tests:

```bash
python manage.py test
```

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS
- **Charts**: Matplotlib
- **Database**: SQLite (default, can be configured for other DBs)

## Contributing

Contributions are welcome! Feel free to submit a pull request or create an issue.

## License

This project is licensed under the MIT License.

## Contact

- Developer: Shareif Jones
- GitHub: [https://github.com/shareifjones](https://github.com/shareifjones)
- Portfolio: [https://github.com/shareifjones/portfolio-website.git](https://github.com/shareifjones/portfolio-website.git)
