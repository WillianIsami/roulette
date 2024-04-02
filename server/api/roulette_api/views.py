from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Bet
from .serializers import BetSerializer, UserSerializer

class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BetListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        bets = Bet.objects.filter(user = request.user.id)
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'bet': request.data.get('bet'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = BetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BetDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, bet_id, user_id):
        try:
            return Bet.objects.get(id=bet_id, user = user_id)
        except Bet.DoesNotExist:
            return None

    def get(self, request, bet_id, *args, **kwargs):
        bet_instance = self.get_object(bet_id, request.user.id)
        if not bet_instance:
            return Response(
                {"res": "Object with bet id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BetSerializer(bet_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, bet_id, *args, **kwargs):
        bet_instance = self.get_object(bet_id, request.user.id)
        if not bet_instance:
            return Response(
                {"res": "Object with bet id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'bet': request.data.get('bet'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = BetSerializer(instance = bet_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, bet_id, *args, **kwargs):
        bet_instance = self.get_object(bet_id, request.user.id)
        if not bet_instance:
            return Response(
                {"res": "Object with bet id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        bet_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
