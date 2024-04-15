from flask import Flask, make_response, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import datetime
import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token
from flask_bcrypt import Bcrypt



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for Flask session management

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)  # Set the expiration time for token
app.config["JWT_ALGORITHM"] = "HS256"  # Set the algorithm
jwt = JWTManager(app)    # Initialize JWT 
bcrypt = Bcrypt(app)


db = SQLAlchemy(app)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Define the models for the database tables
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    book_type = db.Column(db.Integer, nullable=False)
    loans = relationship('Loan', backref='book', lazy=True)
    
@app.route('/add_book', methods=['POST'])
def add_book():
    request_data = request.get_json()
    name = request_data['name']
    author = request_data['author']
    year_published = request_data['year_published']
    book_type = request_data['book_type']

    new_book = Book(name=name, author=author, year_published=year_published, book_type=book_type)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "New book added successfully"})

@app.route('/books')
def show_all_books():
    books = Book.query.all()
    book_list = [{"id": book.id, "name": book.name, "author": book.author, "year_published": book.year_published, "book_type": book.book_type} for book in books]
    return jsonify(book_list)

@app.route('/loan_book', methods=['POST'])
def loan_book():
    request_data = request.get_json()
    customer_name = request_data['customer_name']
    book_name = request_data['book_name']
    current_datetime = datetime.datetime.now().date()  # Get current date

    # Retrieve customer and book IDs based on names
    customer = Customer.query.filter_by(name=customer_name).first()
    book = Book.query.filter_by(name=book_name).first()

    if customer and book:
        # Calculate return date based on book type
        if book.book_type == 1:  # Regular book
            return_date = current_datetime + datetime.timedelta(days=10)  # Return in up to 10 days
        elif book.book_type == 2:  # Reference book
            return_date = current_datetime + datetime.timedelta(days=5)  # Return in up to 5 days
        elif book.book_type == 3:  # Special book
            return_date = current_datetime + datetime.timedelta(days=2)  # Return in up to 2 days
        else:
            return jsonify({"error": "Invalid book type"}), 400

        # Perform the loan operation using the retrieved IDs and calculated return date
        new_loan = Loan(cust_id=customer.id, book_id=book.id, loan_date=current_datetime, return_date=return_date)
        db.session.add(new_loan)
        db.session.commit()
        return jsonify({"message": "Book loaned successfully"})
    else:
        return jsonify({"message": "Customer or book not found"}), 404

    
    # Route to fetch all loans
@app.route('/loans')
def show_all_loans():
    loans = Loan.query.all()
    loan_list = [{
        "id": loan.id,
        "customer_id": loan.customer.id,
        "customer_name": loan.customer.name,  # Accessing the customer's name via relationship
        "book_id": loan.book.id,
        "book_name": loan.book.name,  # Accessing the book's name via relationship
        "loan_date": loan.loan_date,
        "return_date": loan.return_date
    } for loan in loans]
    return jsonify(loan_list)

# Route to fetch late loans
@app.route('/late_loans')
def show_late_loans():
    current_date = datetime.datetime.now().date()
    late_loans = Loan.query.filter(Loan.return_date < current_date).all()
    late_loan_list = [{
        "id": loan.id,
        "customer_id": loan.customer.id,
        "customer_name": loan.customer.name,  # Accessing the customer's name via relationship
        "book_id": loan.book.id,
        "book_name": loan.book.name,  # Accessing the book's name via relationship
        "loan_date": loan.loan_date,
        "return_date": loan.return_date
    } for loan in late_loans]
    return jsonify(late_loan_list)

# Route to delete a loan
@app.route('/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    try:
        loan = Loan.query.get(loan_id)
        if loan:
            db.session.delete(loan)
            db.session.commit()
            return jsonify({"message": "Loan deleted successfully"}), 200
        else:
            return jsonify({"error": "Loan not found"}), 404
    except Exception as e:
        # Log the exception or print it for debugging
        print("Error deleting loan:", e)
        return jsonify({"error": "An error occurred while deleting the loan"}), 500



class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    loans = relationship('Loan', backref='customer', lazy=True)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)

    

# Routes for Customer operations
@app.route('/customers')
def show_all_customers():
    customers = Customer.query.all()
    customer_list = [{"id": customer.id, "name": customer.name, "city": customer.city, "age": customer.age} for customer in customers]
    return jsonify(customer_list)

# Route for adding a new customer
@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.json
    name = data.get('name')
    city = data.get('city')
    age = data.get('age')

    new_customer = Customer(name=name, city=city, age=age)
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({'message': 'Customer added successfully'}), 201


# Route for searching books by name
@app.route('/search_books', methods=['GET'])
def search_books():
    search_query = request.args.get('query')  # Get the search query from the request
    if not search_query:
        return jsonify({"error": "Please provide a search query"}), 400

    # Perform a case-insensitive search for books containing the search query in their name
    books = Book.query.filter(Book.name.ilike(f"%{search_query}%")).all()
    
    # Prepare the response data
    book_list = [{"id": book.id, "name": book.name, "author": book.author, "year_published": book.year_published, "book_type": book.book_type} for book in books]
    return jsonify(book_list)

# Route for searching customers by name
@app.route('/search_customers', methods=['GET'])
def search_customers():
    search_query = request.args.get('query')  # Get the search query from the request
    if not search_query:
        return jsonify({"error": "Please provide a search query"}), 400

    # Perform a case-insensitive search for customers containing the search query in their name
    customers = Customer.query.filter(Customer.name.ilike(f"%{search_query}%")).all()
    
    # Prepare the response data
    customer_list = [{"id": customer.id, "name": customer.name, "city": customer.city, "age": customer.age} for customer in customers]
    return jsonify(customer_list)

# Defining Users Table
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    user_role = db.Column(db.String(50), default='user') 
    
    
    
    
    # route for registering new user
    
@app.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user')  # Default to 'user' if role is not provided

    if not username or not password or not role:
        return jsonify({"error": "Missing required fields"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, password=hashed_password, user_role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/user/login', methods=['POST'])              
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token
    expires = datetime.timedelta(days=7)  # Token expiration time
    access_token = create_access_token(identity=user.user_id, expires_delta=expires)

    # Store the token in localStorage
    response = make_response(jsonify({"access_token": access_token}), 200)
    response.set_cookie('access_token', access_token)  # Set the token in a cookie
    return response
#logout

@app.route("/logout")           
@jwt_required
def logout():
    # Clear the access token cookie
    response = make_response(jsonify({"message": "You have been logged out."}), 200)
    response.set_cookie('access_token', '', expires=0)  # Clear the access token cookie
    return response

# Define the root route to serve the frontend
# Define routes to serve HTML files from the frontend folder
@app.route('/')
def home():
    # Serve the index.html file from the frontend folder
    return send_from_directory('../frontend', 'home.html')

@app.route('/books.html')
def books():
    # Serve the books.html file from the frontend folder
    return send_from_directory('../frontend', 'books.html')

@app.route('/customers.html')
def customers():
    # Serve the books.html file from the frontend folder
    return send_from_directory('../frontend', 'customers.html')

@app.route('/loans.html')
def loans():
    # Serve the books.html file from the frontend folder
    return send_from_directory('../frontend', 'loans.html')

@app.route('/login.html')
def login_page():  # Renamed the function to avoid conflict
    # Serve the books.html file from the frontend folder
    return send_from_directory('../frontend', 'login.html')

@app.route('/search.html')
def search():
    # Serve the books.html file from the frontend folder
    return send_from_directory('../frontend', 'search.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
