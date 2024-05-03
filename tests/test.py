import unittest
from fastapi.testclient import TestClient
from server import app
from models import Book, Base, engine


class TestModel(unittest.TestCase):
    """Test the book model"""

    def test_attributes(self):
        """test that book has correct attributes"""

        book = Book()
        self.assertTrue(hasattr(book, "title"))
        self.assertTrue(hasattr(book, "year"))
        self.assertTrue(hasattr(book, "author"))
        self.assertTrue(hasattr(book, "isbn"))

    def test_name(self):
        """test for correct table name"""

        book = Book()
        self.assertEqual(book.__class__.__name__, "Book")


class TestApp(unittest.TestCase):
    """Test seamless run of API"""

    @classmethod
    def setUpClass(cls):
        """base setup for test class"""

        cls.client = TestClient(app)
        cls.client.post("/books",
                        json={"title": "A new Book",
                              "year": 2024,
                              "author": "The Author",
                              "isbn": "ISBN-NUMBER"},
                        headers={"accept": "application/json",
                                 "Content-Type": "application/json"})

    def setUp(self):
        """simple test instance setup"""

        res = self.client.get("/books")
        self.id = res.json()[0].get("id")

    def test_create_route(self):
        """test to create a new book"""

        res = self.client.post("/books",
                               json={"title": "A new Book",
                                     "year": 2024,
                                     "author": "The Author",
                                     "isbn": "ISBN-NUMBER"},
                               headers={"accept": "application/json",
                                        "Content-Type": "application/json"})

        self.assertEqual(res.status_code, 200)
        data = res.json()
        del data['id']
        self.assertEqual(data, {"title": "A new Book",
                                "year": 2024,
                                "author": "The Author",
                                "isbn": "ISBN-NUMBER"})

    def test_get_all(self):
        """test to get all books"""

        res = self.client.get("/books")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(isinstance(res.json(), list))

    def test_get_one(self):
        """test to get a book detail"""

        res = self.client.get(f"/books/{self.id}")

        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(isinstance(data, dict))
        self.assertTrue(data["id"], self.id)
        self.assertTrue(data.get("title"))
        self.assertTrue(data.get("year"))
        self.assertTrue(data.get("author"))
        self.assertTrue(data.get("isbn"))

    def test_update(self):
        """test to update a book by id"""

        res = self.client.put(f"/books/{self.id}",
                              json={"year": 2000},
                              headers={"accept": "application/json",
                                       "Content-Type": "application/json"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json().get("year"), 2000)

    def test_delete(self):
        """test to delete a book"""

        res = self.client.delete(f"/books/{self.id}")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json(),
                         {f"Message": f"Book with {self.id} deleted"})

        new_res = self.client.get(f"/books/{self.id}")
        self.assertEqual(new_res.json(),
                         {"detail": f"No data found for book with Id {self.id}"})


class TestAppError(unittest.TestCase):
    """test basic response for app error"""

    @classmethod
    def setUpClass(cls):
        """base setup for test class"""
        cls.client = TestClient(app)

    def test_create_type_error(self):
        """test incorrect data type"""

        res = self.client.post("/books",
                               json={"title": "A new Book",
                                     "year": "A new year",
                                     "author": "The Author",
                                     "isbn": "ISBN-NUMBER"},
                               headers={"accept": "application/json",
                                        "Content-Type": "application/json"})
        self.assertEqual(res.status_code, 422)

    def test_create_incomplete_data_error(self):
        """test for incomplete data to create book"""

        res = self.client.post("/books",
                               json={"title": "A new Book",
                                     "isbn": "ISBN-NUMBER"},
                               headers={"accept": "application/json",
                                        "Content-Type": "application/json"})
        self.assertEqual(res.status_code, 422)

    def test_404_error(self):
        """test for not found"""

        res = self.client.get(f"/books")
        last = len(res.json())

        res1 = self.client.get(f"/books/{last}")
        self.assertEqual(res1.status_code, 404)

        res2 = self.client.put(f"/books/{last}",
                               json={"title": "A new Book"},
                               headers={"accept": "application/json",
                                        "Content-Type": "application/json"})
        self.assertEqual(res2.status_code, 404)

        res3 = self.client.delete(f"/books/{last}")
        self.assertEqual(res3.status_code, 404)


if __name__ == "__main__":
    unittest.main()
