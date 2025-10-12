from .models import UserProfile

def user_context(request):
    user_data = None
    user_id = request.session.get('user_id')

    if user_id:
        try:
            user = UserProfile.objects.get(id=user_id)
            user_data = {
                'fullname': user.fullname,
                'username': user.username,
                'role': user.role,
            }
        except UserProfile.DoesNotExist:
            pass

    return {'session_user': user_data}
