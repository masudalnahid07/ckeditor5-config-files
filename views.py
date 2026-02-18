from django.shortcuts import render
import os
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Create your views here.

def home(request):
    return render(request, 'garden-index.html')
@csrf_exempt
def custom_upload_function(request):
    if request.method == "POST" and request.FILES.get("upload"):
        upload = request.FILES["upload"]

        # Optional: file type/type validation
        if not upload.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            return JsonResponse({"error": "Only image files are allowed."}, status=400)

        # Optional: file size validation (5MB limit)
        if upload.size > 5 * 1024 * 1024:
            return JsonResponse({"error": "File size must be under 5MB."}, status=400)

        # Save file to MEDIA_ROOT/uploads/
        upload_folder = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, upload.name)
        path = default_storage.save(file_path, ContentFile(upload.read()))

        # Return URL to CKEditor
        file_url = os.path.join(settings.MEDIA_URL, "uploads", upload.name)
        return JsonResponse({"url": file_url})

    return JsonResponse({"error": "Invalid request"}, status=400)