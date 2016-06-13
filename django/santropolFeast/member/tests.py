from django.test import TestCase, Client
from member.models import Member, Client, Note, User, Address, Referencing
from member.models import Contact, Option, Client_option, Restriction
from meal.models import Restricted_item
from datetime import date
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy


class MemberTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        member = Member.objects.create(
            firstname='Katrina', lastname='Heide')
        Contact.objects.create(
            type='Home phone', value='514-456-7890', member=member)

    def test_str_is_fullname(self):
        """A member must be listed using his/her fullname"""
        member = Member.objects.get(firstname='Katrina')
        str_member = str(member)
        self.assertEqual(str_member, 'Katrina Heide')

    def test_get_home_phone(self):
        """The home phone is properly stored"""
        katrina = Member.objects.get(firstname='Katrina')
        self.assertTrue(katrina.get_home_phone().value.startswith('514'))


class NoteTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Member.objects.create(firstname='Katrina',
                              lastname='Heide')
        User.objects.create(username="admin")

    def test_attach_note_to_member(self):
        """Create a note attached to a member"""
        member = Member.objects.get(firstname='Katrina')
        admin = User.objects.get(username='admin')
        note = Note.objects.create(member=member, author=admin)
        self.assertEqual(str(member), str(note.member))

    def test_mark_as_read(self):
        """Mark a note as read"""
        member = Member.objects.get(firstname='Katrina')
        admin = User.objects.get(username='admin')
        note = Note.objects.create(member=member, author=admin)
        self.assertFalse(note.is_read)
        note.mark_as_read()
        self.assertTrue(note.is_read)

    def test_str_includes_note(self):
        """An note listing must include the note text"""
        member = Member.objects.get(firstname='Katrina')
        admin = User.objects.get(username='admin')
        note = Note.objects.create(member=member, author=admin, note='x123y')
        self.assertTrue('x123y' in str(note))


class ReferencingTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        professional_member = Member.objects.create(firstname='Dr. John',
                                                    lastname='Taylor')
        billing_address = Address.objects.create(
            number=123, street='De Bullion',
            city='Montreal', postal_code='H3C4G5')
        beneficiary_member = Member.objects.create(firstname='Angela',
                                                   lastname='Desousa',
                                                   address=billing_address)
        client = Client.objects.create(
            member=beneficiary_member, billing_member=beneficiary_member)
        Referencing.objects.create(referent=professional_member, client=client,
                                   date=date(2015, 3, 15))

    def test_str_includes_all_names(self):
        """A reference listing shows by which member for which client"""
        professional_member = Member.objects.get(firstname='Dr. John')
        beneficiary_member = Member.objects.get(firstname='Angela')
        reference = Referencing.objects.get(referent=professional_member)
        self.assertTrue(professional_member.firstname in str(reference))
        self.assertTrue(professional_member.lastname in str(reference))
        self.assertTrue(beneficiary_member.firstname in str(reference))
        self.assertTrue(beneficiary_member.lastname in str(reference))


class ContactTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        member = Member.objects.create(
            firstname='Katrina', lastname='Heide')
        Contact.objects.create(
            type='Home phone', value='514-456-7890', member=member)

    def test_str_is_fullname(self):
        """A contact must be listed using his/her fullname"""
        member = Member.objects.get(firstname='Katrina')
        contact = Contact.objects.get(member=member)
        self.assertTrue(member.firstname in str(contact))
        self.assertTrue(member.lastname in str(contact))


class AddressTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        address = Address.objects.create(
            number=123, street='De Bullion',
            city='Montreal', postal_code='H3C4G5')
        member = Member.objects.create(
            firstname='Katrina', lastname='Heide',
            address=address)

    def test_str_includes_street(self):
        """An address listing must include the street name"""
        member = Member.objects.get(firstname='Katrina')
        # address = Address.objects.get(member=member)
        self.assertTrue('De Bullion' in str(member.address))


class ClientTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        address = Address.objects.create(
            number=123, street='De Bullion',
            city='Montreal', postal_code='H3C4G5')
        member = Member.objects.create(firstname='Angela',
                                       lastname='Desousa',
                                       address=address)
        client = Client.objects.create(
            member=member, billing_member=member,
            birthdate=date(1980, 4, 19))

    def test_str_is_fullname(self):
        """A client must be listed using his/her fullname"""
        member = Member.objects.get(firstname='Angela')
        client = Client.objects.get(member=member)
        self.assertTrue(member.firstname in str(client))
        self.assertTrue(member.lastname in str(client))

    def test_age_on_date(self):
        """The age on given date is properly computed"""
        member = Member.objects.get(firstname='Angela')
        angela = Client.objects.get(member=member)
        self.assertEqual(angela.age_on_date(date(2016, 4, 19)), 36)
        self.assertEqual(angela.age_on_date(date(1950, 4, 19)), 0)
        self.assertEqual(angela.age_on_date(angela.birthdate), 0)


class OptionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        option = Option.objects.create(
            name='PUREE ALL', option_group='preparation')

    def test_str_is_fullname(self):
        """Option's string representation is its name"""
        name = 'PUREE ALL'
        option = Option.objects.get(name=name)
        self.assertEqual(name, str(option))


class Client_optionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        address = Address.objects.create(
            number=123, street='De Bullion',
            city='Montreal', postal_code='H3C4G5')
        member = Member.objects.create(firstname='Angela',
                                       lastname='Desousa',
                                       address=address)
        client = Client.objects.create(
            member=member, billing_member=member,
            birthdate=date(1980, 4, 19))
        option = Option.objects.create(
            name='PUREE ALL', option_group='preparation')
        Client_option.objects.create(client=client, option=option)

    def test_str_includes_all_names(self):
        """A Client_option's string representation includes the name
        of the client and the name of the option.
        """
        member = Member.objects.get(firstname='Angela')
        client = Client.objects.get(member=member)
        name = 'PUREE ALL'
        option = Option.objects.get(name=name)
        client_option = Client_option.objects.get(
            client=client, option=option)
        self.assertTrue(client.member.firstname in str(client_option))
        self.assertTrue(client.member.lastname in str(client_option))
        self.assertTrue(option.name in str(client_option))


class RestrictionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        address = Address.objects.create(
            number=123, street='De Bullion',
            city='Montreal', postal_code='H3C4G5')
        member = Member.objects.create(firstname='Angela',
                                       lastname='Desousa',
                                       address=address)
        client = Client.objects.create(
            member=member, billing_member=member,
            birthdate=date(1980, 4, 19))
        restricted_item = Restricted_item.objects.create(
            name='pork', restricted_item_group='meat')
        Restriction.objects.create(client=client,
                                   restricted_item=restricted_item)

    def test_str_includes_all_names(self):
        """A restriction's string representation includes the name
        of the client and the name of the restricted_item.
        """
        member = Member.objects.get(firstname='Angela')
        client = Client.objects.get(member=member)
        name = 'pork'
        restricted_item = Restricted_item.objects.get(name=name)
        restriction = Restriction.objects.get(
            client=client, restricted_item=restricted_item)
        self.assertTrue(client.member.firstname in str(restriction))
        self.assertTrue(client.member.lastname in str(restriction))
        self.assertTrue(restricted_item.name in str(restriction))


class FormTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username='admin@example.com',
            email='admin@example.com',
            password='test1234'
        )

    def test_acces_to_form(self):
        """Test if the form is accesible from its url"""
        self.client.login(
            username=self.admin.username,
            password=self.admin.password
        )
        result = self.client.get(
            reverse_lazy(
                'member:member_step'
            ), follow=True
        )
        self.assertEqual(result.status_code, 200)

    def test_acces_to_form_by_url_basic_info(self):

        result = self.client.get('/member/create/basic_info', follow=True)

        self.assertEqual(result.status_code, 200)

    def test_acces_to_form_by_url_adress_information(self):

        result = self.client.get(
            '/member/create/address_information', follow=True
        )

        self.assertEqual(result.status_code, 200)

    def test_acces_to_form_by_url_referent_information(self):

        result = self.client.get(
            '/member/create/referent_information', follow=True
        )

        self.assertEqual(result.status_code, 200)

    def test_acces_to_form_by_url_payment_information(self):

        result = self.client.get(
            '/member/create/referent_infomation', follow=True
        )
        self.assertEqual(result.status_code, 200)

    def test_acces_to_form_by_url_dietary_restriction(self):

        result = self.client.get(
            '/member/create/dietary_restriction', follow=True
        )

        self.assertEqual(result.status_code, 200)

    def test_acces_to_form_by_url_emergency_contact(self):

        result = self.client.get(
            '/member/create/emergency_contact', follow=True
        )

        self.assertEqual(result.status_code, 200)

    def test_form_save_data(self):

        basic_information_request = {
            "client_wizard-current_step": "basic_info",
            "basic_info-firstname": "Testing",
            "basic_info-lastname": "User",
            "basic_info-languages": "fr",
            "basic_info-gender": "M",
            "basic_info-birthdate": "12/12/1995",
            "basic_info-contact_type": "Home phone",
            "basic_info-contact_value": "555-555-5555",
            "basic_info-alert": "Testing alert message",
            "wizard_goto_step": ""

        }

        address_information_request = {
            "client_wizard-current_step": "address_information",
            "address_information-street": "555 rue clark",
            "address_information-apartement": "222",
            "address_information-city": "montreal",
            "address_information-postal_code": "H3C2C2",
            "wizard_goto_step": "",
        }

        referent_information_request = {
            "client_wizard-current_step": "referent_information",
            "referent_information-firstname": "Referent",
            "referent_information-lastname": "Testing",
            "referent_information-work_information": "CLSC",
            "referent_information-date": "12/12/2012",
            "referent_information-referral_reason": "Testing referral reason",
            "wizard_goto_step": "",
        }

        billing_information_request = {
            "client_wizard-current_step": "billing_information",
            "billing_information-firstname": "Testing",
            "billing_information-lastname": "Billing",
            "billing_information-billing_payment_type": "check",
            "billing_information-facturation": "default",
            "billing_information-street": "111 rue clark",
            "billing_information-apartement": "222",
            "billing_information-city": "Montreal", "postal_code": "H2C3G4",
            "wizard_goto_step": "",
        }

        restriction_information_request = {
            "client_wizard-current_step": "dietary_restriction",
            "dietary_restriction-status": "on",
            "dietary_restriction-delivery_type": "O",
            "wizard_goto_step": ""
        }

        emergency_contact_request = {
            "client_wizard-current_step": "emergency_contact",
            "emergency_contact-firstname": "Emergency",
            "emergency_contact-lastname": "User",
            "emergency_contact-contact_type": "Home phone",
            "emergency_contact-contact_value": "555-444-5555"
        }

        self.client.post(
            '/member/create/basic_information', basic_information_request
        )

        self.client.post(
            '/member/create/address_information', address_information_request,
        )

        self.client.post(
            '/member/create/referent_information',
            referent_information_request
        )

        self.client.post(
            '/member/create/billing_information', billing_information_request,
        )

        self.client.post(
            '/member/create/dietary_restriction',
            restriction_information_request
         )

        self.client.post(
            '/member/create/emergency_contact', emergency_contact_request,
        )

        print (Member.objects.all)
        member = Member.objects.get(firstname="Testing")

    def test_member_name(self):

        member = Member.objets.get(firstname="Testing")
        self.assertTrue(member.firstname, "Testing")
        self.assertTrue(member.lastname, "User")

    def test_home_phone_member(self):

        member = Member.objects.get(firstname="Testing")
        self.assertTrue(member.get_home_phone().value.startswith('555'))

    def test_member_alert(self):

        member = Member.objects.get(firstname="Testing")
        self.assertTrue(member.alert, "Testing alert message")

    def test_client_languages(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)
        self.assertTrue(client.language, "fr")

    def test_client_birthdate(self):

        member = Member.objets.get(firstname="Testing")
        client = Client.objects.get(Member=member)
        self.assertTrue(client.birthdate, "12/12/1995")

    def test_client_gender(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)
        self.assertTrue(client.gender, "M")

    def test_client_contact_type(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)
        self.assertTrue(member.contact.contact_type, "Home phone")

    def test_client_address(self):

        member = Member.objects.get(firstname="Testing")
        self.assertTrue(member.address.street, "555 rue clark")
        self.assertTrue(member.address.postal_code, "H3C2C2")
        self.assertTrue(member.address.apartment, "222")
        self.assertTrue(member.address.city, "montreal")

    def test_referent_name(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)

        self.assertTrue(client.client_referent.referent.firstname, "Referent")
        self.assertTrue(client.client_referent.referent.lastname, "Testing")

    def test_referent_work_information(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)

        self.assertTrue(client.client_referent.work_information, "CLSC")

    def test_referral_date(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)

        self.assertTrue(client.client_referent.date, "12/12/2012")

    def test_referral_reason(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)

        self.assertTrue(
            client.client_referent.referral_reason, "Testing referral reason"
        )

    def test_billing_name(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)

        self.assertTrue(client.billing_member.firstname, "Testing")
        self.assertTrue(client.billing_member.lastname, "Billing")

    def test_billing_type(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)

        self.assertTrue(client.billing_payment_type, "check")

    def test_billing_address(self):
        # missing models for billing address
        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)

    def test_billing_rate_type(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)

        self.assertTrue(client.rate_type, "default")

    def test_emergency_contact_name(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)

        self.assertTrue(client.emergency_contact.firstname, "Emergency")
        self.assertTrue(client.emergency_contact.lastname, "User")

    def test_emergency_contact_value(self):

        member = Member.objects.get(firstname="Testing")
        client = Client.objects.get(Member=member)

        self.assertTrue
        (
            client.emergency_contact.get_home_phone, "555-444-5555"
        )

    def tear_down(self):
        self.client.logout()
