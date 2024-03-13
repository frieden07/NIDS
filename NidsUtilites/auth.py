"""In this module utility function are stored"""

import traceback
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission

AUTH_STRING_MICROSERVICE = "TEAMMAITRI"


class IsFromMicroservice(BasePermission):
    def has_permission(self, request, view):
        if request.headers.get("nids-key") == AUTH_STRING_MICROSERVICE:
            return True
        else:
            return False


class ModelAPIView(APIView):
    """
    Base class for custom API views that handle models.

    This class extends the Django Rest Framework's APIView and provides
    common functionality for handling responses and exceptions related to models.

    Attributes:
    - permission_classes (list): List of permission classes required for access.
    - logger: The logger used for logging information and errors.

    Methods:
    - finalize_response: Finalizes the response, modifying it based on the
      response status value. Removes the "status" key from the response and sets
      the appropriate HTTP status code.
    - handle_exception: Handles exceptions that occur during the processing of
      the view, logging the exception and returning an HTTP response with an
      error message and status code.
    """

    permission_classes = [IsAuthenticated | IsFromMicroservice]

    def finalize_response(self, request, response, *args, **kwargs):
        """Finalizes the response for the ModelAPIView.

        Args:
            request (HttpRequest): The HTTP request object.
            response (dict or Response): The response object to be finalized.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The finalized response object.

        Description:
            This method is responsible for finalizing the response for the
            ModelAPIView. It checks the type of the response object and
            performs necessary modifications based on the status value present
            in the response. If the status is 1, it removes
            the "status" key from the response dictionary and returns a
            Response object with HTTP status code 200 (OK). If the status is
            not 1, it also removes the "status" key from the response
            dictionary but returns a Response object with HTTP status code
            400 (Bad Request). The finalized response object is then passed to
            the parent class's finalize_response method for further processing.
        """
        if isinstance(response, dict):
            if response["status"] == 1:
                del response["status"]
                response = Response(response, status=status.HTTP_200_OK)
            else:
                del response["status"]
                response = Response(response, status=status.HTTP_400_BAD_REQUEST)
        return super(ModelAPIView, self).finalize_response(
            request, response, *args, **kwargs
        )

    def handle_exception(self, exc):
        """
        Handle exceptions that occur during the processing of the view.

        Args:
            exc (Exception): The exception object raised during view
                             processing.

        Returns:
            Response: The HTTP response containing an error message and status
                      code.
        """
        try:
            return super(ModelAPIView, self).handle_exception(exc)
        except Exception as ex:
            tb = traceback.format_exc()
            print("Traceback", f"{tb} {ex}")
            return Response(
                {"msg": str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
