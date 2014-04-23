from types import MethodType

from django.test import TestCase
from django.contrib.auth.models import User
from django_twilio.models import Caller, Credential, Twiml


class CallerTestCase(TestCase):
    """Run tests against the :class:`django_twilio.models.Caller` model ."""

    def setUp(self):
        self.caller = Caller.objects.create(
            phone_number='12223334444', blacklisted=False)

    def test_has_unicode(self):
        self.assertTrue(isinstance(self.caller.__unicode__, MethodType))

    def test_unicode_returns_str(self):
        self.assertTrue(isinstance(self.caller.__unicode__(), str))

    def test_unicode_doesnt_contain_blacklisted(self):
        self.assertFalse('blacklisted' in self.caller.__unicode__())

    def test_unicode_contains_blacklisted(self):
        self.caller.blacklisted = True
        self.caller.save()
        self.assertTrue('blacklisted' in self.caller.__unicode__())

    def tearDown(self):
        self.caller.delete()


class CredentialTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test', password='pass')
        self.creds = Credential.objects.create(
            name='Test Creds',
            account_sid='XXX',
            auth_token='YYY',
            user=self.user,
        )

    def test_unicode(self):
        ''' Assert that unicode renders how we'd like it too '''
        self.assertEquals(self.creds.__unicode__(), 'Test Creds - XXX')

    def test_credentials_fields(self):
        ''' Assert the fields are working correctly '''
        self.assertEquals(self.creds.name, 'Test Creds')
        self.assertEquals(self.creds.account_sid, 'XXX')
        self.assertEquals(self.creds.auth_token, 'YYY')
        self.assertEquals(self.creds.user, self.user)


class TwimlTests(TestCase):

    def setUp(self):
        self.twiml_1 = '<Response><Dial>+123456789</Dial></Response>'
        self.twiml_2 = '<Response><Message>Hello reply</Message></Response>'
        self.t_1 = Twiml.objects.create(
            name='call forwarding',
            twiml=self.twiml_1,
            url='forwarding',
            public=True)
        self.t_2 = Twiml.objects.create(
            name='sms reply',
            twiml=self.twiml_2,
            url='messaging',
            public=False)

    def test_unicode(self):
        ''' Assert the unicode looks how we'd like it to '''
        self.assertEquals(self.t_1.__unicode__(), 'TwiML - call forwarding')
        self.assertEquals(self.t_2.__unicode__(), 'TwiML - sms reply')

    def test_twiml_fields(self):
        ''' Assert all fields return how we'd like them to '''

        self.assertEquals(self.t_1.url, 'forwarding')
        self.assertEquals(self.t_1.public, True)
        self.assertEquals(self.t_1.twiml, self.twiml_1)
        self.assertEquals(self.t_2.url, 'messaging')
        self.assertEquals(self.t_2.public, False)
        self.assertEquals(self.t_2.twiml, self.twiml_2)

    def test_twiml_functions(self):
        ''' Assert the model functions work properly '''

        twiml1 = '<?xml version="1.0" encoding="UTF-8"?><Response><Dial>+123456789</Dial></Response>'
        twiml2 = '<?xml version="1.0" encoding="UTF-8"?><Response><Message>Hello reply</Message></Response>'

        self.assertEquals(self.t_1.generated_url(), '/twiml/forwarding/')
        self.assertEquals(self.t_2.generated_url(), '/twiml/messaging/')
        self.assertEquals(self.t_1.to_xml(), twiml1)
        self.assertEquals(self.t_2.to_xml(), twiml2)
