import MySQLdb
import unittest
import os


class TestCreateState(unittest.TestCase):
    def setUp(self):
        # Establish connection to the MySQL database
        self.connection = MySQLdb.connect(

            host=os.getenv('HBNB_MYSQL_HOST'),
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )

        self.cursor = self.connection.cursor()

    def tearDown(self):
        # Close the cursor and database connection after each test
        self.cursor.close()
        self.connection.close()

    def test_create_state(self):
        # Get the initial count of records in the 'states' table
        self.cursor.execute("SELECT COUNT(*) FROM states")
        initial_count = self.cursor.fetchone()[0]

        # Execute the command to create a new state (e.g., 'California')
        # For demonstration purposes, let's assume 'California' is added with ID 50
        self.cursor.execute("INSERT INTO states (id, name) VALUES (50, 'California')")

        # Get the count of records in the 'states' table after insertion
        self.cursor.execute("SELECT COUNT(*) FROM states")
        final_count = self.cursor.fetchone()[0]

        # Assert that the difference in counts is +1
        self.assertEqual(final_count - initial_count, 1)

if __name__ == '__main__':
    unittest.main()
