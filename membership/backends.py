from django.contrib.auth.models import User


# Allow users to login using either their
# username OR email address
class EmailOrUsernameModelBackend(object):

    # Login the user
    def authenticate(self, username=None, password=None):

        # if there is a '@' in the username field it's the email address
        if '@' in username:
            kwargs = {'email': username}
        # if there is no '@' then the check for the username
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


    # Get the user object if it exists
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
