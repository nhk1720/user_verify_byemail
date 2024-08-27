
# import random
# from django.conf import settings
# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializer import *
# from .emails import send_otp_via_email
# from django.core.mail import send_mail
# class RegisterAPI(APIView):
#     def post(self,request):
#         try:
#             data=request.data
#             serializer=UserSerializer(data=data)
#             print(serializer,'0000000000000000000000')
#             if serializer.is_valid():
#                 serializer.save()
#                 subject='Your account verification email'
#                 otp=random.randint(1000,9999)
#                 message=f'Your otp is {otp}'
#                 email_from=settings.EMAIL_HOST_USER
#                 msg_html =None
#                 user_obj=User.objects.filter(email=serializer.data['email'])
#                 user_obj.otp=otp
#                 user_obj.save()
#                 send_mail(subject,message,email_from,[serializer.data['email']],html_message=msg_html)
#                 # send_otp_via_email(serializer.data['email'])
#                 return Response(({
#                     'status':200,
#                     'msg':'Registration successfully check email',
#                     'data':serializer.data
#                 }))
#             return Response({
#                 'status':400,
#                 'msg':'Something went wrong',
#                 'data':serializer.errors
#             })
            
#         except Exception as e:
#             print(e)
            
            
            
            
            
            
            
            
            
import random
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from .models import User
from django.core.mail import send_mail

class RegisterAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                user = serializer.save()
                otp = random.randint(1000, 9999)
                user.otp = str(otp)
                user.save()

                subject = 'Your account verification email'
                message = f'Your OTP is {otp}'
                email_from = settings.EMAIL_HOST_USER
                send_mail(subject, message, email_from, [user.email], fail_silently=False)
                return Response({
                    'status': status.HTTP_201_CREATED,
                    'msg': 'Registration successful. Check your email for the OTP.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'msg': 'Invalid data',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'msg': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class VerifyOtp(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyOtpSerializer(data=data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                user = User.objects.filter(email=email).first()

                if not user:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'msg': 'Invalid email',
                        'data': 'The provided email does not exist in our records.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                if user.otp != otp:
                    return Response({
                        'status': status.HTTP_400_BAD_REQUEST,
                        'msg': 'Wrong OTP',
                        'data': 'The OTP you provided is incorrect.'
                    }, status=status.HTTP_400_BAD_REQUEST)

                user.is_verified = True
                user.save()
                return Response({
                    'status': status.HTTP_200_OK,
                    'msg': 'Account verified successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'msg': 'Invalid data',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'msg': str(e),
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)