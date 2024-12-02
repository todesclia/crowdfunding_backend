import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, PledgeDetailSerializer
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly

def upload_to_s3(file):
    s3 = boto3.client('s3', region_name=settings.AWS_REGION)

    try:
        # Upload the file to the S3 bucket
        s3_key = f"images/{file.name}"
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, s3_key)
        print("File uploaded successfully!")
        s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_keye}"
        return s3_url
    except NoCredentialsError:
        print("AWS credentials not found.")
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")


class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        # use the project model to get a list of all projects in the db
        projects = Project.objects.all()
        # use the project serializer to convert that list to JSON
        serializer = ProjectSerializer(projects, many=True)
        #return a response containing the serialized data
        return Response(serializer.data)
    
    def post(self, request):
        print(f"Request Data: {request.data}")
        print(f"Request Files: {request.FILES}")

        # Handle file upload
        file = request.FILES.get('image')  # 'image' is the key in your form data
        image_url = None
        if file:
            # Upload the file to S3
            image_url = upload_to_s3(file)

        # Prepare the request data for the serializer
        # If the image URL was returned, we include it in the data
        if image_url:
            request.data['image'] = image_url  # Include the image URL in the request data

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            print("Project created successfully!")

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        print(f"Serializer Errors: {serializer.errors}")
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )

class ProjectDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(
            instance=project,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )

class PledgeDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSupporterOrReadOnly
    ]

    def get_object(self, pk):
        try:
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(pledge)
        return Response(serializer.data)
    
    def put(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(
            instance=pledge,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )