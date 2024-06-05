from oauth2_provider.oauth2_validators import OAuth2Validator


class CustomOAuth2Validator(OAuth2Validator):
    # def get_additional_claims(self, request):
    #     return {
    #         # "given_name": request.user.first_name,
    #         # "family_name": request.user.last_name,
    #         # "name": ' '.join([request.user.first_name, request.user.last_name]),
    #         # "preferred_username": request.user.username,
    #         # "email": request.user.email,
    #     }