from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer
from .decoretors import required_api_key
import os

@api_view(['GET', 'POST'])
def books_list_create(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        api_key = request.headers.get('X-API-Key')
        if api_key != 'valid-key':
            return Response({"error": "INVALID_API_KEY"}, status=401)
        
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail_update_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        api_key = request.headers.get('X-API-Key')
        if api_key != 'valid-key':
            return Response({"error": "INVALID_API_KEY"}, status=401)

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        api_key = request.headers.get('X-API-Key')
        if api_key != 'valid-key':
            return Response({"error": "INVALID_API_KEY"}, status=401)

        book.delete()
        return Response(status=204)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
@required_api_key
def upload_cover(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if 'cover' not in request.FILES:
        return Response({"error": "NO_FILE", "message": "Cover image file is missing"}, status=400)

    cover = request.FILES['cover']
    if cover.size > 2 * 1024 * 1024:
        return Response({"error": "FILE_TOO_LARGE", "message": "Max file size is 2MB"}, status=413)

    ext = os.path.splitext(cover.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        return Response({
            "error": "INVALID_FILE_TYPE",
            "message": "Only JPG, PNG, and WEBP files are allowed",
            "allowed_types": ["jpg", "png", "webp"],
            "received_type": ext[1:]
        }, status=400)

    book.cover_image = cover
    book.save()

    return Response({
        "id": book.id,
        "title": book.title,
        "cover_url": request.build_absolute_uri(book.cover_image.url),
        "message": "Cover uploaded successfully"
    }, status=200)
