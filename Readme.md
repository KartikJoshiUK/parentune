# Personalized Parent Onboarding System

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `flask db upgrade`
4. Start the server: `flask run`

## API Endpoints

### Parent

- **Create Parent**: `POST /parent`
- **Get All Parents**: `GET /parent`
- **Update Parent**: `PUT /parent/<id>`
- **Delete Parent**: `DELETE /parent/<id>`

### Child

- **Create Child**: `POST /child`
- **Get All Children**: `GET /child`
- **Update Child**: `PUT /child/<id>`
- **Delete Child**: `DELETE /child/<id>`

### Blog

- **Create Blog**: `POST /blog`
- **Get All Blogs**: `GET /blog`
- **Update Blog**: `PUT /blog/<id>`
- **Delete Blog**: `DELETE /blog/<id>`

### Home Feed

- **Get Home Feed**: `GET /feed/<parent_id>`
- **Customize Home Feed**: `POST /feed/<parent_id>`

## Testing

Use Postman or curl to test the API endpoints.
