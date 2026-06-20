from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, Destination, Booking

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    destinations = Destination.query.limit(3).all()
    return render_template('index.html', destinations=destinations)

@app.route('/destinations')
def destinations():
    all_destinations = Destination.query.all()
    return render_template('destinations.html', destinations=all_destinations)

@app.route('/add_destination', methods=['GET', 'POST'])
def add_destination():
    if request.method == 'POST':
        destination = Destination(
            name=request.form['name'],
            country=request.form['country'],
            price=float(request.form['price']),
            duration=request.form['duration'],
            description=request.form['description'],
            image_url=request.form.get('image_url', '')
        )
        db.session.add(destination)
        db.session.commit()
        flash('Destination added successfully!', 'success')
        return redirect(url_for('destinations'))
    return render_template('add_destination.html')

@app.route('/edit_destination/<int:id>', methods=['GET', 'POST'])
def edit_destination(id):
    destination = Destination.query.get_or_404(id)
    if request.method == 'POST':
        destination.name = request.form['name']
        destination.country = request.form['country']
        destination.price = float(request.form['price'])
        destination.duration = request.form['duration']
        destination.description = request.form['description']
        destination.image_url = request.form.get('image_url', '')
        db.session.commit()
        flash('Destination updated successfully!', 'success')
        return redirect(url_for('destinations'))
    return render_template('edit_destination.html', destination=destination)

@app.route('/delete_destination/<int:id>')
def delete_destination(id):
    destination = Destination.query.get_or_404(id)
    db.session.delete(destination)
    db.session.commit()
    flash('Destination deleted successfully!', 'warning')
    return redirect(url_for('destinations'))

@app.route('/book/<int:destination_id>', methods=['GET', 'POST'])
def book(destination_id):
    destination = Destination.query.get_or_404(destination_id)
    if request.method == 'POST':
        booking = Booking(
            destination_id=destination_id,
            customer_name=request.form['name'],
            email=request.form['email'],
            travel_date=request.form['date'],
            travelers=int(request.form['travelers'])
        )
        db.session.add(booking)
        db.session.commit()
        flash(f'Booking confirmed for {destination.name}!', 'success')
        return redirect(url_for('destinations'))
    return render_template('booking.html', destination=destination)

@app.route('/bookings')
def bookings():
    all_bookings = Booking.query.all()
    return render_template('bookings.html', bookings=all_bookings)

if __name__ == '__main__':
    app.run(debug=True)