from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Bet
from .serializers import BetSerializer

class BetListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Bet items for given requested user
        '''
        bets = Bet.objects.filter(user = request.user.id)
        serializer = BetSerializer(bets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Bet with given Bet data
        '''
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
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, bet_id, user_id):
        '''
        Helper method to get the object with given bet_id, and user_id
        '''
        try:
            return Bet.objects.get(id=bet_id, user = user_id)
        except Bet.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, bet_id, *args, **kwargs):
        '''
        Retrieves the Bet with given bet_id
        '''
        bet_instance = self.get_object(bet_id, request.user.id)
        if not bet_instance:
            return Response(
                {"res": "Object with bet id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BetSerializer(bet_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, bet_id, *args, **kwargs):
        '''
        Updates the bet item with given bet_id if exists
        '''
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

    # 5. Delete
    def delete(self, request, bet_id, *args, **kwargs):
        '''
        Deletes the bet item with given bet_id if exists
        '''
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