from django.shortcuts import render

# Create your views here.

from django.contrib.auth import get_user_model

from .models import (ChatSession, ChatSessionMember, ChatSessionMessage, deserialize_user)

from rest_framework import APIView
from rest_framework.response import Response
from rest_framework import permissions

class ChatSessionView(APIView):
    # Manage chat sessions

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # create a new chat session

        user = request.user

        chat_session = ChatSession.objects.create(owner=user)

        return Response ({
            'status': 'SUCCESS', 'uri': chat_session.uri,
            'message': 'New chat session was created'
        })
    
    def patch(self, request, *args, **kwargs):
        # Add a user to a chat session

        User = get_user_model()

        uri = kwargs['uri']
        username = request.data['username']

        user = User.objects.get(username=username)
        chat_session = ChatSession.object.get(uri=uri)
        owner = chat_session.owner

        if owner != user:
            """Only allow non owner join the room"""
            chat_session.members.get_or_create(
                user=user, chat_session=chat_session
            )

        owner = deserialize_user(owner)
        members = [
            deserialize_user(chat_session.users)
        ]            