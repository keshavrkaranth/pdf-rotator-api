import os

from PyPDF2.utils import PdfReadError, PyPdfError
from django.core.files import File
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
import PyPDF2
from api.helper import pdf_rotator


@api_view(['POST'])
@permission_classes([AllowAny])
def rotate_pdf(request):
    file_path = request.FILES.get('file_path')
    angle_of_rotation = request.POST.get('angle_of_rotation', 0)
    page_number = request.POST.get('page_number')

    if angle_of_rotation is not None and not int(angle_of_rotation) % 90 == 0:
        return Response({'success': False, 'error': "Angle of rotation should be multiples of 90"},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        pdf_reader = PyPDF2.PdfFileReader(file_path)
    except Exception as e:
        return Response({'success': False, 'error': 'only pdf file accepted'}, status=status.HTTP_400_BAD_REQUEST)
    pdf_writer = PyPDF2.PdfFileWriter()
    if not int(page_number) <= pdf_reader.getNumPages():
        return Response({'success': False, 'error': f"Enter page number between 1-{pdf_reader.getNumPages()}"},
                        status=status.HTTP_400_BAD_REQUEST)

    pdf_rotator(pdf_reader, pdf_writer, page_number, int(angle_of_rotation))
    return Response({'success': True, 'data': {
        "file_path": os.getcwd()+'\rotated.pdf',
    }}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def rotate_pdf_with_attachment(request):
    file_path = request.FILES.get('file_path')
    angle_of_rotation = request.POST.get('angle_of_rotation', 0)
    page_number = request.POST.get('page_number')

    if not int(angle_of_rotation) % 90 == 0:
        return Response({'success': False, 'error': "Angle of rotation should be multiples of 90"},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        pdf_reader = PyPDF2.PdfFileReader(file_path)
    except Exception as e:
        print(e)
        return Response({'success': False, 'error': 'only pdf file accepted'}, status=status.HTTP_400_BAD_REQUEST)

    pdf_writer = PyPDF2.PdfFileWriter()
    if not int(page_number) <= pdf_reader.getNumPages():
        return Response({'success': False, 'error': f"Enter page number between 1-{pdf_reader.getNumPages()}"},
                        status=status.HTTP_400_BAD_REQUEST)

    pdf_rotator(pdf_reader, pdf_writer, page_number, int(angle_of_rotation))

    return FileResponse(open('rotated.pdf', 'rb'), as_attachment=True, content_type='application/pdf')
