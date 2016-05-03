from django import forms
from django.utils.translation import ugettext_lazy as _
from member.models import *


class ClientBasicInformation (forms.Form):

    firstname = forms.CharField(max_length=100, label=_("First Name"))
    lastname = forms.CharField(max_length=100, label=_("Last Name"))

    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    birthdate = forms.DateField(label=_("Birthday"))

    contact_type = forms.ChoiceField(choices=CONTACT_TYPE_CHOICES,
                                     label=_("Contact Type"))

<<<<<<< 5371f4f624cc4e097f76456ba4d3d4e45aa795e6
    alert = forms.CharField()
=======

    contact_value = forms.CharField(label=_("Contact information"))

    alert = forms.CharField(label=_("Alert"))
>>>>>>> Fix #51


class ClientAddressInformation(forms.Form):

    number = forms.IntegerField(label=_("Street Number"))

<<<<<<< 5371f4f624cc4e097f76456ba4d3d4e45aa795e6
    apartment_number = forms.IntegerField()

    floor_number = forms.IntegerField()
=======
    apartment = forms.IntegerField(label=_("Apartment Number"))
    apartment.required = False

    floor = forms.IntegerField(label=_("Floor"))
    floor.required = False
>>>>>>> Fix #51

    street = forms.CharField(max_length=100, label=_("Street Name"))

    city = forms.CharField(max_length=50, label=_("City Name"))

    postal_code = forms.CharField(max_length=6, label=_("Postal Code"))


class MemberRestrictionsInformation(forms.Form):
    pass

    # Suppose to be many to many
    # client_restriction = forms


class ClientAllergyInformation(forms.Form):
    pass


class ClientReferentInformation(forms.Form):

<<<<<<< 5371f4f624cc4e097f76456ba4d3d4e45aa795e6
    referent_first_name = forms.CharField(max_length=100)
    referent_last_name = forms.CharField(max_length=100)

    gender = forms.CheckboxInput()
=======
    firstname = forms.CharField(max_length=100, label=_("First Name"))
    lastname = forms.CharField(max_length=100, label=_("Last Name"))
    referral_reason = forms.CharField(label=_("Referral Reason"))
    date = forms.DateField(label=_("Referral Date"))
>>>>>>> Fix #51


class ClientPaymentInformation(forms.Form):

<<<<<<< 5371f4f624cc4e097f76456ba4d3d4e45aa795e6
    billing_type = forms.ChoiceField()
=======
    facturation = forms.ChoiceField(label=_("Billing Type"),
                                    choices=FACTURATION_TYPE
                                    )
>>>>>>> Fix #51

    firstname = forms.CharField(label=_("First Name"))

    lastname = forms.CharField(label=_("Last Name"))

    number = forms.IntegerField(label=_("Street Number"))

<<<<<<< 5371f4f624cc4e097f76456ba4d3d4e45aa795e6
    billing_apartment_number = forms.IntegerField()

    billing_floor_number = forms.IntegerField()
=======
    apartement = forms.CharField(label=_("Apartement Number"))
    apartement.required = False

    floor = forms.IntegerField(label=_("Floor"))
    floor.require = False
>>>>>>> Fix #51

    street = forms.CharField(label=_("Street Name"))

    city = forms.CharField(label=_("City Name"))

<<<<<<< 5371f4f624cc4e097f76456ba4d3d4e45aa795e6
    billing_postal_code = forms.CharField()
=======
    postal_code = forms.CharField(label=_("Postal Code"))


class ClientEmergencyContactInformation(forms.Form):

    firstname = forms.CharField(label=_("First Name"))

    lastname = forms.CharField(label=_("Last Name"))

    contact_type = forms.ChoiceField(label=_("Contact Type"),
                                     choices=CONTACT_TYPE_CHOICES)

    contact_value = forms.CharField(label=_("Contact"))
>>>>>>> Fix #51
