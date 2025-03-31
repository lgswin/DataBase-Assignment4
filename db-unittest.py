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

if __name__ == '__main__':
    unittest.main()
