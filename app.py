from flask import Flask, render_template, redirect, url_for, request, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# ------------------ ROUTES ------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Replace with real authentication
        if email and password:
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!", "danger")
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']
        if password == confirm:
            # Here you'd save to DB
            flash("Signup successful. Please log in.", "success")
            return redirect(url_for('login'))
        else:
            flash("Passwords do not match!", "danger")
    return render_template('signup.html')


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Simulate sending email
        flash(f"Password reset link sent to {email}.", "info")
        return redirect(url_for('login'))
    return render_template('forgot_password.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/about-us')
def about_us():
    return render_template('about_us.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        date = request.form['date']
        type = request.form['type']

        # Dummy price logic
        pricing = {
            "Wedding": 12000,
            "Events": 9000,
            "Birthday": 7500,
            "Tour": 10000,
            "Wildlife": 18000,
            "Adventure": 15000
        }
        price = pricing.get(type, 10000)

        return render_template('booking.html', message="✅ Booking Confirmed!", name=name, location=location, date=date, type=type, price=price)
    
    return render_template('booking.html')


@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')


@app.route('/booking-history')
def booking_history():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('booking_history.html')


@app.route('/user-reviews')
def user_reviews():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('user_reviews.html')


@app.route('/photographer-categories')
def photographer_categories():
    return render_template('photographer_categories.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# ------------------ RUN APP ------------------

if __name__ == '__main__':
    app.run(debug=True)
