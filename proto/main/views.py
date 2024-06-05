from django.shortcuts import render
from django.views import View

# Create your views here.
import shibboleth

class ShibbolethAuthView(View):
    def get(self, request):
        # Set the Shibboleth SP entityID and entityID URL
        sp_entity_id = 'https://idp.scc.kit.edu'
        sp_entity_id_url = 'https://your-sp-entity-id.com/Shibboleth.sso'

        # Set the Shibboleth IdP entityID
        idp_entity_id = 'https://your-idp-entity-id.com'

        # Create a Shibboleth authentication request
        auth_request = shibboleth.AuthenticationRequest(
            sp_entity_id,
            sp_entity_id_url,
            idp_entity_id,
            request.GET.get('target', '/')
        )

        # Send the authentication request to the Shibboleth server
        response = requests.post(auth_request.get_url(), data=auth_request.get_data())

        # Check the response status code
        if response.status_code == 302:
            # Redirect the user to the Shibboleth login page
            return HttpResponseRedirect(response.headers['Location'])
        elif response.status_code == 200:
            # Parse the Shibboleth response
            response_data = response.content.decode('utf-8')
            attributes = shibboleth.parse_attributes(response_data)

            # Authenticate the user using the Shibboleth attributes
            user = authenticate(username=attributes.get('eppn', ''), password='')

            # Log the user in
            login(request, user)

            # Redirect the user to the target URL
            return HttpResponseRedirect(request.GET.get('target', '/'))

        return HttpResponseServerError('Authentication failed')