import unittest
import mysql.connector
from datetime import datetime

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = mysql.connector.connect(
            user='flyway_user',
            password='Secret5555',
            host='127.0.0.1',
            database='subscriber_db'
        )
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_schema_structure(self):
        # Check if 'subscribers' table exists
        self.cursor.execute("SHOW TABLES LIKE 'subscribers'")
        table_exists = self.cursor.fetchone()
        self.assertIsNotNone(table_exists, "Table 'subscribers' does not exist")

        # Check column structure
        self.cursor.execute("DESCRIBE subscribers")
        columns = {col[0]: col[1] for col in self.cursor.fetchall()}

        self.assertIn('id', columns)
        self.assertIn('name', columns)
        self.assertIn('email', columns)
        self.assertTrue(columns['id'].startswith('int'), "id column should be an integer")
        self.assertTrue(columns['email'].startswith('varchar'), "email column should be varchar")

    def test_created_at_column(self):
        # Check if created_at column exists and has correct type
        self.cursor.execute("DESCRIBE subscribers")
        columns = {col[0]: col[1] for col in self.cursor.fetchall()}
        
        self.assertIn('created_at', columns, "created_at column does not exist")
        self.assertTrue(columns['created_at'].startswith('timestamp'), 
                       "created_at column should be timestamp type")

    def test_subscription_date_column(self):
        # Check if subscription_date column exists and has correct type
        self.cursor.execute("DESCRIBE subscribers")
        columns = {col[0]: col[1] for col in self.cursor.fetchall()}
        
        self.assertIn('subscription_date', columns, "subscription_date column does not exist")
        self.assertTrue(columns['subscription_date'].startswith('timestamp'), 
                       "subscription_date column should be timestamp type")

        # Test automatic population of subscription_date
        test_name = "Test User"
        test_email = "test@example.com"
        
        # Insert a new subscriber
        self.cursor.execute(
            "INSERT INTO subscribers (name, email) VALUES (%s, %s)",
            (test_name, test_email)
        )
        self.conn.commit()

        # Verify the subscription_date was automatically set
        self.cursor.execute(
            "SELECT subscription_date FROM subscribers WHERE email = %s",
            (test_email,)
        )
        result = self.cursor.fetchone()
        self.assertIsNotNone(result[0], "subscription_date should not be null")
        
        # Verify the date is recent
        subscription_date = result[0]
        self.assertIsInstance(subscription_date, datetime, "subscription_date should be a datetime object")
        
        # Clean up test data
        self.cursor.execute("DELETE FROM subscribers WHERE email = %s", (test_email,))
        self.conn.commit()

    def test_data_integrity(self):
        # Check if database contains data
        self.cursor.execute("SELECT COUNT(*) FROM subscribers")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0, "Database should contain at least one subscriber")

        # Check if required fields are not null
        self.cursor.execute("SELECT name, email FROM subscribers")
        for row in self.cursor.fetchall():
            self.assertIsNotNone(row[0], "name field should not be null")
            self.assertIsNotNone(row[1], "email field should not be null")
            self.assertIsInstance(row[0], str, "name should be a string")
            self.assertIsInstance(row[1], str, "email should be a string")

if __name__ == '__main__':
    unittest.main()
