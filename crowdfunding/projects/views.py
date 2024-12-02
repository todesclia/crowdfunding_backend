from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, PledgeDetailSerializer
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly
import boto3
import logging
from django.conf import settings
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from django.http import JsonResponse

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,  # Ensure you have region configured in settings
)

logger = logging.getLogger(__name__)

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
        logger.info(f"Request Data: {request.data}")
        logger.info(f"Request Files: {request.FILES}")

        project_image = request.FILES.get('image') 
        if project_image:
            try:
                # Log the start of the upload process
                logger.info(f"Uploading {project_image.name} to S3...")

                # Upload file to S3
                s3.upload_fileobj(
                    project_image, 
                    settings.AWS_STORAGE_BUCKET_NAME,  # Your S3 bucket name
                    f'projects/{project_image.name}'   # Path within your S3 bucket
                )

                # Log success
                logger.info(f"File {project_image.name} uploaded successfully to S3.")

            except NoCredentialsError:
                logger.error("AWS credentials not found.")
                return JsonResponse({"error": "AWS credentials not found."}, status=400)
            except PartialCredentialsError:
                logger.error("Incomplete AWS credentials.")
                return JsonResponse({"error": "Incomplete AWS credentials."}, status=400)
            except ClientError as e:
                logger.error(f"Client error: {e}")
                return JsonResponse({"error": f"Client error: {str(e)}"}, status=400)

        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)

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