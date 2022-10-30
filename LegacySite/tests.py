from django.test import TestCase
from LegacySite.models import Card
from django.test import Client

# Create your tests here.

class MyTest(TestCase):
    # Django's test run with an empty database. We can populate it with
    # data by using a fixture. You can create the fixture by running:
    #    mkdir LegacySite/fixtures
    #    python manage.py dumpdata LegacySite > LegacySite/fixtures/testdata.json
    # You can read more about fixtures here:
    #    https://docs.djangoproject.com/en/4.0/topics/testing/tools/#fixture-loading
    #fixtures = ["testdata.json"]

    # Assuming that your database had at least one Card in it, this
    # test should pass.
    # def test_get_card(self):
    #    allcards = Card.objects.all()
    #    self.assertNotEqual(len(allcards), 0)
        
    def test_xss_invalidinput(self):
        c = Client()
        response = c.get('/buy/', {'director': 'test<script>alert("hello")</script>'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
    def test_sql_invalidinput(self):
        c = Client()
        card = "{\"merchant_id\": \"NYU Apparel Card\", \"customer_id\": \"test@test.com\", \"total_value\": \"10\", \"records\": [{\"record_type\": \"amount_change\", \"amount_added\": 2000, \"signature\": \"a%%\' UNION SELECT password FROM LegacySite_user where username = \'admin\'; --%%\'\"}]}"
        
        with open('newcard.gftcrd', 'rb') as f:
            data = {"card_supplied" : f,}
        response = c.post('/use/', data=data)
        self.assertEqual(response.status_code, AttributeError)
        
    def test_csrf_invalidinput(self):
        c = Client()
        response = c.get('/buy/', {'director': 'test<script>var xhr = new XMLHttpRequest(); xhr.open(\'POST\', \'/gift\', true); var data= new FORMData(); data.append(\'username\', \'test\'); data.append(\'amount\', \'10\'); xhr.send(data); </script>'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200) 
        
