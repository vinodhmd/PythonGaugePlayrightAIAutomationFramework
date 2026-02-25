# fixtures/data_generator.py
"""
Data Generator module for creating dynamic test data.
Useful for generating unique test data for each test run.
"""
import random
import string
from datetime import datetime, timedelta

class DataGenerator:
    """Generate dynamic test data for automation tests."""    
    @staticmethod
    def random_string(length=10):
        """Generate a random string of specified length."""
        return ''.join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def random_email(domain="test.com"):
        """Generate a random email address."""
        username = DataGenerator.random_string(8).lower()
        timestamp = datetime.now().strftime("%H%M%S")
        return f"{username}_{timestamp}@{domain}"
    
    @staticmethod
    def random_phone(country_code="1"):
        """Generate a random phone number."""
        number = ''.join(random.choices(string.digits, k=10))
        return f"+{country_code}{number}"
    
    @staticmethod
    def random_number(min_val=1, max_val=1000):
        """Generate a random number within range."""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def random_name():
        """Generate a random full name."""
        first_names = ["John", "Jane", "Alex", "Emma", "Michael", "Sarah", "David", "Lisa"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    @staticmethod
    def random_password(length=12, include_special=True):
        """Generate a random secure password."""
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += "!@#$%^&*"
        password = ''.join(random.choices(chars, k=length))
        return password
    
    @staticmethod
    def future_date(days=30, format="%Y-%m-%d"):
        """Generate a future date."""
        future = datetime.now() + timedelta(days=days)
        return future.strftime(format)
    
    @staticmethod
    def past_date(days=30, format="%Y-%m-%d"):
        """Generate a past date."""
        past = datetime.now() - timedelta(days=days)
        return past.strftime(format)
    
    @staticmethod
    def timestamp():
        """Generate current timestamp string."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def unique_id(prefix="ID"):
        """Generate a unique ID with prefix."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"{prefix}_{timestamp}"

# Example usage:
# from fixtures.data_generator import DataGenerator
# 
# email = DataGenerator.random_email()
# name = DataGenerator.random_name()
# order_id = DataGenerator.unique_id("ORD")
