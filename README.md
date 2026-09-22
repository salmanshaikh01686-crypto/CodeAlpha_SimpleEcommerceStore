# Simple E-commerce Store

A beginner-friendly e-commerce website built with:

- Frontend: HTML, CSS, JavaScript
- Backend: Django / Python
- Database: SQLite
- Features:
  - Product listing
  - Product details
  - Shopping cart
  - User registration/login/logout
  - Checkout/order processing
  - Order history
  - Django admin for product management

## Run locally

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
source venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Create database:
```bash
python manage.py migrate
```

Create admin:
```bash
python manage.py createsuperuser
```

Start:
```bash
python manage.py runserver
```

Open:
- Store: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

The checkout is a demo order-processing flow. It stores orders in SQLite and does not charge real money.
