from unittest import TestCase
from stack import Stack

class TestStack(TestCase):
    """Test cases for Stack"""

    def setUp(self):
        """Setup before each test"""
        self.stack = Stack()

    def tearDown(self):
        """Tear down after each test"""
        self.stack = None

    def test_push(self):
        """Test pushing an item into the stack"""
        self.stack.push("Hello")
        self.stack.push("World")
        self.assertEqual(self.stack.peek(), "World")
        self.assertEqual(self.stack.pop(), "World")

    def test_pop(self):
        """Test popping an item of off the stack"""
        self.stack.push("Hello")
        self.stack.push("World")
        self.assertEqual(self.stack.pop(), "World")
        self.assertEqual(self.stack.peek(), "Hello")
        self.assertEqual(self.stack.pop(), "Hello")
        self.assertTrue(self.stack.is_empty())

    def test_peek(self):
        """Test peeking at the top the stack"""
        self.stack.push("Magic")
        self.stack.push("Mike")
        self.assertEqual(self.stack.peek(), "Mike")

    def test_is_empty(self):
        """Test if the stack is empty"""
        self.assertTrue(self.stack.is_empty())
        self.stack.push("Hello")
        self.assertFalse(self.stack.is_empty())
