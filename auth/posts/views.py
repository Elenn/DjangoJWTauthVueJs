from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from .models import Post  

class ShowPostsViewSet(viewsets.ModelViewSet): 
    serializer_class = PostSerializer
    queryset = Post.objects.all()  
    permission_classes = [IsAuthenticated]	
