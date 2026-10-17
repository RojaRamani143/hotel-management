import os
import sqlite3
from datetime import date, datetime
from pathlib import Path
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'local-demo-only-change-me')
DB_PATH = Path(os.environ.get('DATABASE_PATH', '/app/data/hotel.db'))

HOTELS = [
    {'id': 1, 'name': 'The Azure Palace', 'city': 'Goa', 'type': 'Beachfront escape', 'price': 6200, 'rating': '4.9', 'image': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1000&q=85', 'badge': 'Guest favorite'},
    {'id': 2, 'name': 'Luna Grand', 'city': 'Jaipur', 'type': 'Heritage luxury', 'price': 4800, 'rating': '4.8', 'image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1000&q=85', 'badge': 'Best value'},
    {'id': 3, 'name': 'Cloud Nine Retreat', 'city': 'Manali', 'type': 'Mountain hideaway', 'price': 5400, 'rating': '4.9', 'image': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=1000&q=85', 'badge': 'Popular'},
    {'id': 4, 'name': 'The Urban Nest', 'city': 'Hyderabad', 'type': 'City sophistication', 'price': 3900, 'rating': '4.7', 'image': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1000&q=85', 'badge': 'New arrival'},
]


def connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name TEXT NOT NULL,
            email TEXT NOT NULL,
            hotel_id INTEGER NOT NULL,
            checkin TEXT NOT NULL,
            checkout TEXT NOT NULL,
            guests INTEGER NOT NULL,
            total INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )''')


@app.route('/')
def home():
    city = request.args.get('city', '').strip()
    results = [h for h in HOTELS if not city or city.lower() in h['city'].lower()]
    return render_template('index.html', hotels=results, all_hotels=HOTELS, city=city, today=date.today().isoformat())


@app.post('/book')
def book():
    try:
        hotel_id = int(request.form.get('hotel_id', ''))
        guests = int(request.form.get('guests', ''))
        hotel = next((h for h in HOTELS if h['id'] == hotel_id), None)
        name = request.form.get('guest_name', '').strip()
        email = request.form.get('email', '').strip()
        checkin = date.fromisoformat(request.form.get('checkin', ''))
        checkout = date.fromisoformat(request.form.get('checkout', ''))
        if not hotel or not (2 <= len(name) <= 100) or '@' not in email or len(email) > 254:
            raise ValueError('Please enter valid guest and hotel details.')
        if not 1 <= guests <= 4 or checkin < date.today() or checkout <= checkin:
            raise ValueError('Choose valid dates and 1–4 guests.')
        nights = (checkout - checkin).days
        if nights > 30:
            raise ValueError('A stay can be at most 30 nights.')
        total = nights * hotel['price']
    except (ValueError, TypeError) as error:
        flash(str(error) if str(error) else 'Please check your booking details.', 'error')
        return redirect(url_for('home') + '#booking')

    with connection() as conn:
        cur = conn.execute('''INSERT INTO bookings
            (guest_name, email, hotel_id, checkin, checkout, guests, total, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, email, hotel_id, checkin.isoformat(), checkout.isoformat(), guests, total, datetime.now().isoformat()))
        booking_id = cur.lastrowid
    return redirect(url_for('confirmation', booking_id=booking_id, email=email))


@app.get('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    email = request.args.get('email', '')
    with connection() as conn:
        booking = conn.execute('SELECT * FROM bookings WHERE id = ? AND email = ?', (booking_id, email)).fetchone()
    if booking is None:
        return render_template('not_found.html'), 404
    hotel = next(h for h in HOTELS if h['id'] == booking['hotel_id'])
    return render_template('confirmation.html', booking=booking, hotel=hotel)


@app.get('/health')
def health():
    return {'status': 'ok'}


init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
