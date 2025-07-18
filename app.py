from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime

app = Flask(__name__)
# Generate a strong secret key for session management.
# In a production environment, this should be loaded from an environment variable
# or a configuration file, not hardcoded.
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

# --- Dummy Data (for demonstration purposes) ---
# In a real application, this data would be stored in a database (e.g., SQLite, PostgreSQL).
# For simplicity, we're using in-memory dictionaries and lists.

# User data: email -> {password, name}
users = {
    "user@example.com": {"password": "password123", "name": "Demo User"},
    "sandeep@capture.com": {"password": "admin", "name": "Sandeep"}
}

# Booking history data for a logged-in user (simulated)
# In a real app, this would be associated with a specific user ID.
bookings = [
    {
        "event_type": "Wedding",
        "booking_date": "2023-10-26",
        "booking_time": "14:00",
        "photographer_name": "Sana",
        "status": "Confirmed",
        "price": 12000
    },
    {
        "event_type": "Birthday",
        "booking_date": "2023-11-15",
        "booking_time": "10:30",
        "photographer_name": "Krithin",
        "status": "Pending",
        "price": 7500
    }
]

# Feedback/Review data
feedback_reviews = [
    {"name": "Alice Smith", "email": "alice@example.com", "message": "Amazing service! The photos were beyond my expectations."},
    {"name": "Bob Johnson", "email": "bob@example.com", "message": "Very professional and friendly team. Highly recommend Capture Moments."},
    {"name": "Charlie Brown", "email": "charlie@example.com", "message": "Good experience overall, minor delay but quality was great."},
]

# Gallery images data: (filename, caption)
gallery_images = [
    ("wed1.jpg", "Golden Hour Magic"),
    ("wed2.jpg", "Joyful Celebration"),
    ("wed3.jpg", "Serene Landscape"),
    ("wed4.jpg", "Candid Laughter"),
    ("wed5.jpg", "Wildlife in Action"),
    ("wed6.jpg", "Urban Exploration"),
    ("tour2.jpg", "Fashion Forward"),
    ("tour3.jpg", "Intimate Moments"),
    ("tour4.jpg", "Adventure Awaits"),
]

# --- Routes ---

@app.route('/')
def index():
    return render_template('MultipleFiles/index.html')

@app.route('/home')
def home():
    """
    Renders the home page (home.html) which provides options to login, signup, etc.
    """
    return render_template('MultipleFiles/home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login functionality.
    - GET: Displays the login form.
    - POST: Processes the submitted login credentials.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in users and users[email]['password'] == password:
            session['logged_in'] = True
            session['user_email'] = email
            session['user_name'] = users[email]['name']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('MultipleFiles/login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles user registration functionality.
    - GET: Displays the signup form.
    - POST: Processes the submitted registration details.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not all([name, email, password, confirm_password]):
            flash('All fields are required!', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match!', 'danger')
        elif email in users:
            flash('Email already registered. Please try logging in or use a different email.', 'warning')
        else:
            users[email] = {"password": password, "name": name}
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login')) # Redirect to login page after successful signup
    return render_template('MultipleFiles/signup.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """
    Handles the forgot password request.
    - GET: Displays the forgot password form.
    - POST: Processes the email to send a reset link (simulated).
    """
    if request.method == 'POST':
        email = request.form.get('email')
        if email in users:
            # In a real application, you would generate a token and send an email
            flash(f'If {email} is registered, a password reset link has been sent (simulated).', 'success')
        else:
            flash('Email not found.', 'danger')
    return render_template('MultipleFiles/forgot_password.html')

@app.route('/dashboard')
def dashboard():
    """
    Renders the user dashboard. Requires the user to be logged in.
    """
    if not session.get('logged_in'):
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    user_name = session.get('user_name', 'Guest') # Default to 'Guest' if name not in session
    return render_template('MultipleFiles/dashboard.html', user_name=user_name)

@app.route('/logout')
def logout():
    """
    Logs out the current user by clearing session data.
    """
    session.pop('logged_in', None)
    session.pop('user_email', None)
    session.pop('user_name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/about_us')
def about_us():
    """
    Renders the 'About Us' page.
    """
    return render_template('MultipleFiles/about_us.html')

@app.route('/terms')
def terms():
    """
    Renders the 'Terms & Conditions' page.
    """
    return render_template('MultipleFiles/terms.html')

@app.route('/feedback')
def feedback():
    """
    Renders the 'Feedback' page, displaying existing user reviews.
    Note: The HTML file is named feedback.html but displays reviews.
    If you want a form to submit feedback, you'd add POST method logic here.
    """
    return render_template('MultipleFiles/feedback.html', reviews=feedback_reviews)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Handles the 'Contact Us' form submission.
    - GET: Displays the contact form.
    - POST: Processes the submitted contact message.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not all([name, email, subject, message]):
            flash('All fields are required for the contact form.', 'danger')
        else:
            # In a real application, you would:
            # 1. Save this message to a database.
            # 2. Send an email to your support team.
            print(f"--- New Contact Message ---")
            print(f"From: {name} <{email}>")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            print(f"---------------------------")
            flash('Your message has been sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('contact')) # Redirect to clear the form
    return render_template('MultipleFiles/contact.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    """
    Handles the photographer booking process.
    - GET: Displays the booking form.
    - POST: Processes the booking details and confirms.
    """
    if not session.get('logged_in'):
        flash('Please log in to book a photographer.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        date_str = request.form.get('date')
        booking_type = request.form.get('type')

        # Basic validation
        if not all([name, location, date_str, booking_type]):
            flash('All booking fields are required.', 'danger')
            return render_template('MultipleFiles/booking.html')

        try:
            # Attempt to parse the date to ensure it's valid
            booking_date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            # You might want to add logic to ensure the date is in the future
            if booking_date_obj < datetime.now():
                flash('Booking date cannot be in the past.', 'danger')
                return render_template('MultipleFiles/booking.html')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return render_template('MultipleFiles/booking.html')

        # Dummy price calculation based on type
        price_map = {
            "Wedding": 15000,
            "Events": 10000,
            "Birthday": 7000,
            "Tour": 12000,
            "Wildlife": 18000,
            "Adventure": 20000,
        }
        price = price_map.get(booking_type, 5000) # Default price if type not found

        # Simulate storing the booking (in a real app, this goes to a DB)
        new_booking = {
            "name": name, # User's name for the booking
            "location": location,
            "date": date_str,
            "type": booking_type,
            "price": price,
            # Additional fields for booking history display
            "event_type": booking_type,
            "booking_date": date_str,
            "booking_time": "Flexible", # Or allow user to input time
            "photographer_name": "Assigned Soon", # Placeholder
            "status": "Pending Confirmation",
        }
        bookings.append(new_booking) # Add to our dummy list

        flash('Your booking request has been received!', 'success')
        # Render the booking page again, but with confirmation message
        return render_template('MultipleFiles/booking.html',
                               message="Booking Confirmed!",
                               name=name, location=location, date=date_str,
                               type=booking_type, price=price)
    return render_template('MultipleFiles/booking.html')

@app.route('/booking_history')
def booking_history():
    """
    Displays the user's booking history. Requires the user to be logged in.
    """
    if not session.get('logged_in'):
        flash('Please log in to view your booking history.', 'warning')
        return redirect(url_for('login'))
    # In a real application, you would filter bookings specific to the logged-in user.
    # For this demo, we're showing all dummy bookings.
    return render_template('MultipleFiles/booking_history.html', bookings=bookings)

@app.route('/profile')
def profile():
    """
    Displays the photographer profiles.
    """
    return render_template('MultipleFiles/profile.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/photographer_categories')
def photographer_categories():
    """
    Displays the different photographer categories/styles.
    """
    return render_template('MultipleFiles/photographer_categories.html')

# --- Error Handlers (Optional but good practice) ---
@app.errorhandler(404)
def page_not_found(e):
    """Handles 404 Not Found errors."""
    return render_template('404.html'), 404 # You would need to create a 404.html template

# --- Run the Application ---
if __name__ == '__main__':
    # Ensure the 'static/images' directory exists for gallery and category images
    # In a real deployment, static files are usually served by a web server (e.g., Nginx)
    # and this check might not be necessary.
    static_images_path = os.path.join(app.root_path, 'static', 'images')
    if not os.path.exists(static_images_path):
        os.makedirs(static_images_path)
        print(f"Created directory: {static_images_path}")
        print("Please place your image files (e.g., wedding.jpg, gallery_image1.jpg) inside this folder.")

    # Run the Flask development server.
    # debug=True enables:
    # 1. Debugger (for detailed error messages)
    # 2. Auto-reloader (restarts server on code changes)
    # Set debug=False in production.
    app.run(debug=True)
