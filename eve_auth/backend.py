from django.contrib.auth.models import User
from .models import EveData


class EsiBackend:
    def authenticate(self, request, CharacterID, CharacterName, **_):
        try:
            ed = EveData.objects.get(character_id=CharacterID)
        except EveData.DoesNotExist:
            user = User.objects.create_user(CharacterName)
            user.save()

            ed = EveData(user=user, character_id=CharacterID, full_name=CharacterName)
            ed.save()

        return ed.user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
