from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _

from member.views import *
from member.forms import *

<<<<<<< 5371f4f624cc4e097f76456ba4d3d4e45aa795e6
urlpatterns = patterns(
    '', url(r'^create/$',
            ClientWizard.as_view(
                    [ClientBasicInformation, ClientAddressInformation,
                     ClientReferentInformation, ClientPaymentInformation]
            )),
    url(_(r'^list/$'),
        ClientList.as_view(), name='list'),
)
=======
create_member_forms = (
    ('basic_info', ClientBasicInformation),
    ('address_information', ClientAddressInformation),
    ('referent_information', ClientReferentInformation),
    ('payment_information', ClientPaymentInformation),
    ('dietary_restriction', ClientRestrictionsInformation),
    ('emergency_contact', ClientEmergencyContactInformation)
)

member_wizard = ClientWizard.as_view(create_member_forms,
                                     url_name='member:member_step')

urlpatterns = patterns('',
                       url(r'^create/$', member_wizard, name='member_step'),
                       url(r'^create/(?P<step>.+)/$', member_wizard,
                           name='member_step'),
                       url(_(r'^list/$'), ClientList.as_view(), name='list'),
                       )
>>>>>>> Fix #51
