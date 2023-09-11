from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from app.serializers.user import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from sklearn.metrics.pairwise import cosine_similarity
from app.models import User
from app.constants.global_constants import DATA
import random

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

class UserLoginView(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.is_online = True
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk}, status=status.HTTP_200_OK)
    
class OnlineUserListView(generics.ListAPIView):
    queryset = User.objects.filter(is_online=True)
    serializer_class = UserSerializer


class RecommendedListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    def get_queryset(self):
        user_id = self.kwargs['user_id']

        try:
            user = User.objects.get(id=user_id)

            user_interests = user.interests

            all_users = User.objects.exclude(id=user_id)
            similarities = []

            for other_user in all_users:
                other_user_interests = other_user.interests

                user_interests_values = [user_interests.get(key, 0) for key in user_interests.keys()]
                other_user_interests_values = [other_user_interests.get(key, 0) for key in user_interests.keys()]

                similarity = cosine_similarity([user_interests_values], [other_user_interests_values])[0][0]
                similarities.append((other_user, similarity))

            similar_users = sorted(similarities, key=lambda x: x[1], reverse=True)[:5]

            return [user for user, similarity in similar_users]
        except User.DoesNotExist:
            return []         


def register_multiple_users():

    registered_users = []

    for user_data in DATA:
        if 'id' in user_data:
            user_data.pop('id')
        user_data['password'] = 'password'
        user_data['is_online'] = random.choice([True, False])

        serializer = UserRegistrationSerializer(data=user_data)

        if serializer.is_valid():
            serializer.save()
            registered_users.append(serializer.instance)
        else:
            print('error')

    return registered_users
