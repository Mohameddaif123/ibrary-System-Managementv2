import unittest
import json
from app import app, db, Book, Customer, Loan

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'  # Use the same database as app.py
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Remove the session
        with app.app_context():
            db.session.remove()
            # Comment out or remove the line below to retain database tables after tests
            # db.drop_all()

    # Test adding a new book
    def test_add_book(self):
        book_data = {
            'name': 'Test Book',
            'author': 'Test Author',
            'year_published': 2023,
            'book_type': 1
        }
        response = self.app.post('/add_book', json=book_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'New book added successfully')

        # Check if the book is added to the database
        with app.app_context():
            book = Book.query.filter_by(name='Test Book').first()
            self.assertIsNotNone(book)
            self.assertEqual(book.author, 'Test Author')
            self.assertEqual(book.year_published, 2023)
            self.assertEqual(book.book_type, 1)

    # Test adding a new customer
    def test_add_customer(self):
        customer_data = {
            'name': 'Test Customer',
            'city': 'Test City',
            'age': 30
        }
        response = self.app.post('/add_customer', json=customer_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Customer added successfully')

        # Check if the customer is added to the database
        with app.app_context():
            customer = Customer.query.filter_by(name='Test Customer').first()
            self.assertIsNotNone(customer)
            self.assertEqual(customer.city, 'Test City')
            self.assertEqual(customer.age, 30)

    # Test adding a loan
    def test_loan_book(self):
        # Add a book
        book_data = {
            'name': 'Test Book',
            'author': 'Test Author 2',
            'year_published': 2023,
            'book_type': 2
        }
        self.app.post('/add_book', json=book_data)

        # Add a customer
        customer_data = {
            'name': 'Test Customer 2',
            'city': 'Test City',
            'age': 30
        }
        self.app.post('/add_customer', json=customer_data)

        loan_data = {
            'customer_name': 'Test Customer',
            'book_name': 'Test Book'
        }
        response = self.app.post('/loan_book', json=loan_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Book loaned successfully')

        # Check if the loan is added to the database
        with app.app_context():
            customer = Customer.query.filter_by(name='Test Customer').first()
            book = Book.query.filter_by(name='Test Book').first()
            loan = Loan.query.filter_by(cust_id=customer.id, book_id=book.id).first()
            self.assertIsNotNone(loan)
            self.assertIsNotNone(loan.loan_date)
            self.assertIsNotNone(loan.return_date)

if __name__ == '__main__':
    unittest.main()
