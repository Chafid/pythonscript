from datetime import datetime

import zeep
from lxml import etree
from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.wsse.username import UsernameToken

# wsdl_url = "https://b2g-disc.ppsr.gov.au/PpsrB2GService/2011/02/CollateralRegistrationSearch.svc/soap11?WSDL"
wsdl_file = 'schemas.ppsr.gov.au.2015.02.services.wsdl'
service_url = "https://b2g-disc.ppsr.gov.au/PpsrB2GService/2011/02/CollateralRegistrationSearch.svc/soap12"
method_url = "https://b2g-disc.ppsr.gov.au/PpsrB2GService/2011/02/SearchByGrantor/soap11"
username = "bra195"
password = "OurPPSRp/w1"

session = Session()
session.auth = HTTPBasicAuth(username, password)

# create the header element

#your_pretty_xml = etree.tostring (header, encoding="unicode", pretty_print=True)
#print (your_pretty_xml)

# set the header value from header element
# header_value = header(Action=method_url, To=service_url)
client = zeep.Client(wsdl=wsdl_file, wsse=UsernameToken(username, password))
header = {'TargetEnvironment': 'Discovery'}

# make the service call

request_data = {
    'SearchByGrantorRequest': {
        'CustomersRequestMessageId': 'ABC123',
        'CustomersUserDefinedFields': [],
        'AcceptGrantorIndividualSearchDeclaration': True,
        'SearchCriteria': {
            'CollateralClassSearchCriteria': [],
            'GrantorIndividualSearchCriteria': {
                'DateOfBirth': '1970-07-07',
                'FamilyName': 'Smith',
                'GivenNames': 'John'
            },
            'GrantorOrganisationSearchCriteria': {
                'OrganisationName': 'Club Transport Finance Pty Ltd',
                'OrganisationNumber': '119232825',
                'OrganisationNumberType': 'ACN'
            },
            'GrantorType': 'Organisation',
            'IncludeArchived': False,
            'IncludeCurrent': True,
            'IncludeExpired': False,
            'IncludeMigratedTransitional': False,
            'IncludeNonMigratedTransitional': False,
            'IncludeNonTransitional': False,
            'IncludeRemoved': False,
            'IsPMSISearchCriteria': 'Unsupported',
            'PointInTimeDateTime': '2022-12-10',
            'RegistrationNumberSortOrder': 'Ascending',
            'SecurityInterestsOnly': False
        }
    }
}

clientSearch = client.bind('Ppsr_2015_02','CollateralRegistrationSearchSoap12')

result = clientSearch.SearchByGrantor(
    _soapheaders={'TargetEnvironment': 'Discovery'},
    **request_data
)

# set the WSDL URL
#wsdl_url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"

# set method URL
#method_url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryIntPhoneCode"

# set service URL
#service_url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"