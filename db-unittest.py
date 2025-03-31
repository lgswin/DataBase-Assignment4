import unittest
import mysql.connector

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = mysql.connector.connect(
            user='flyway_user',
            password='Secret5555',
            host='localhost',
            database='subscriber_db'
        )
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_schema_structure(self):
        # Check if 'subscribers' table exists
        self.cursor.execute("SHOW TABLES LIKE 'subscribers'")
        table_exists = self.cursor.fetchone()
        self.assertIsNotNone(table_exists, "❌ Table 'subscribers' does not exist")

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
        
        self.assertIn('created_at', columns, "❌ created_at column does not exist")
        self.assertTrue(columns['created_at'].startswith('timestamp'), 
                       "❌ created_at column should be timestamp type")

    def test_data_integrity(self):
        # Check if database contains data
        self.cursor.execute("SELECT COUNT(*) FROM subscribers")
        count = self.cursor.fetchone()[0]
        self.assertGreater(count, 0, "❌ Database should contain at least one subscriber")

        # Check if required fields are not null
        self.cursor.execute("SELECT name, email FROM subscribers")
        for row in self.cursor.fetchall():
            self.assertIsNotNone(row[0], "❌ name field should not be null")
            self.assertIsNotNone(row[1], "❌ email field should not be null")
            self.assertIsInstance(row[0], str, "❌ name should be a string")
            self.assertIsInstance(row[1], str, "❌ email should be a string")

if __name__ == '__main__':
    unittest.main()
