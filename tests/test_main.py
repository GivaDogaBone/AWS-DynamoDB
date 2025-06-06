# tests/test_main.py
import unittest
import sys
import os

# Add the parent directory to sys.path to import the main module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models for testing
from main import VenueCreate, Venue

class TestVenueModels(unittest.TestCase):
    def test_venue_create_model(self):
        """Test that the VenueCreate model can be instantiated with the required fields"""
        venue_data = {
            "venueDescription": "Test Venue",
            "accountID": "acc123",
            "accountDenomination": "Test Account",
            "accountDescription": "A test account"
        }
        venue = VenueCreate(**venue_data)
        self.assertEqual(venue.venueDescription, "Test Venue")
        self.assertEqual(venue.accountID, "acc123")
        self.assertEqual(venue.accountDenomination, "Test Account")
        self.assertEqual(venue.accountDescription, "A test account")
        
    def test_venue_model(self):
        """Test that the Venue model can be instantiated with the required fields"""
        venue_data = {
            "venueID": "venue123",
            "venueDescription": "Test Venue",
            "accountID": "acc123",
            "accountDenomination": "Test Account",
            "accountDescription": "A test account"
        }
        venue = Venue(**venue_data)
        self.assertEqual(venue.venueID, "venue123")
        self.assertEqual(venue.venueDescription, "Test Venue")
        
if __name__ == '__main__':
    unittest.main()