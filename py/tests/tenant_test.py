import unittest

from davidkhala.azure.ci import credentials
from davidkhala.azure.subscription import Subscription


class SubscriptionTestCase(unittest.TestCase):
    def test_default(self):
        auth = credentials()
        sub = Subscription(auth)
        one = sub.get_one()
        print(type(one))
