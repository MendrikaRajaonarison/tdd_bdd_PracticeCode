"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(0, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_create_an_account(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_representing_an_account(self):
        """Test the account's representing"""
        account = Account()
        account.name = "Aina"
        self.assertEqual(str(account), "<Account 'Aina'>")

    def test_data_to_dict(self):
        """Test the data go to dict"""
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        result = account.to_dict()
        self.assertEqual(account.name, result["name"])
        self.assertEqual(account.email, result["email"])
        self.assertEqual(account.phone_number, result["phone_number"])
        self.assertEqual(account.disabled, result["disabled"])
        self.assertEqual(account.date_joined, result["date_joined"])

    def test_data_from_dict(self):
        """Test the data from dict"""
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account()
        account.from_dict(data)
        self.assertEqual(account.name, data["name"])
        self.assertEqual(account.email, data["email"])
        self.assertEqual(account.phone_number, data["phone_number"])
        self.assertEqual(account.disabled, data["disabled"])

    def test_updating_an_account(self):
        """Test updating an account"""
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertIsNotNone(account.id)
        account.name = "Aina"
        account.update()
        found = Account.find(account.id)
        self.assertEqual(found.name, "Aina")

    def test_updating_with_no_id(self):
        """Test updating an account with no id"""
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.id = None
        self.assertRaises(DataValidationError, account.update)

    def test_delete_an_account(self):
        """Test deletion of an account"""
        for i in [0, 1]:
            data = ACCOUNT_DATA[self.rand] # get a random account
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), 2)
        account.delete()
        self.assertEqual(len(Account.all()), 1)
