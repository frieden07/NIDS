from NidsUtilites.auth import ModelAPIView
from rest_framework.response import Response
from NidsModels.models.system import Charts, Intrusions, Alerts
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status


class ChartView(ModelAPIView):
    @swagger_auto_schema(
        manual_parameters=[],
        responses={200: "OK", 400: "No data found."},
        operation_summary="Dashboard chart details",
        operation_description="""API for dashboard charts which shows detected count vs acanned count graph.
        """,
    )
    def get(self, request):
        """
        Handle GET request for retrieving dashboard charts details.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response containing dashboard charts details.
        """
        user = request.user

        chart_objs = Charts.objects.filter(user=user)
        response_data = []

        for obj in chart_objs:
            data = {
                "id": obj.chartId,
                "userName": obj.user.username,
                "year": obj.year,
                "month": obj.month,
                "scannedCount": obj.scannedCount,
                "detectedCount": obj.detectedCount,
            }

            response_data.append(data)

        return Response(data=response_data, status=200)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "userName": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User name",
                ),
                "month": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="month",
                ),
                "year": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="year",
                ),
                "scannedCount": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="scanned count",
                ),
                "detectedCount": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="detected count",
                ),
            },
            required=["userName", "month", "year", "scannedCount", "detectedCount"],
        ),
        responses={
            status.HTTP_201_CREATED: "Chart update/save successfully",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
            status.HTTP_400_BAD_REQUEST: "NOT FOUND",
        },
        operation_summary="Save/Update chart details",
        operation_description="""Save/Update chart details for dashboard chart.
        """,
    )
    def post(self, request):
        """
        Handle POST request for storing details of Charts.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response containing status of save operation.
        """
        request_data = request.data
        user_name = request_data["userName"]
        month = request_data["month"]
        year = request_data["year"]

        if User.objects.filter(username=user_name).exists():
            user_obj = User.objects.get(username=user_name)

            if Charts.objects.filter(
                user=user_obj, month=month, year=year
            ).exists():
                chart_obj = Charts.objects.get(
                    user=user_obj, month=month, year=year
                )

                chart_obj.scannedCount = request_data["scannedCount"]
                chart_obj.detectedCount = request_data["detectedCount"]

                chart_obj.save()

                msg = "Successfully updated to chart details."
            else:
                Charts.objects.create(
                    user=user_obj,
                    month=month,
                    year=year,
                    detectedCount=request_data["detectedCount"],
                    scannedCount=request_data["scannedCount"]
                )

                msg = "Successfully created charts details."

            response_data = {
                "msg": msg,
            }
            status = 200
        else:
            response_data = {"msg": f"No user exist with name {user_name}"}
            status = 404

        return Response(data=response_data, status=status)


class AllIntrusionView(ModelAPIView):
    @swagger_auto_schema(
        manual_parameters=[],
        responses={200: "OK", 400: "No data found."},
        operation_summary="All Intrusion details",
        operation_description="""API for details of all Intrusion for specific user.
        """,
    )
    def get(self, request):
        """
        Handle GET request for retrieving details of all Intrusion for specific user.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response containing details of all Intrusion for specific user.
        """
        user = request.user
        intrusion_objs = Intrusions.objects.filter(user=user)
        response_data = []

        for obj in intrusion_objs:
            data = {
                "userNname": obj.user.username,
                "id": obj.intrusionId,
                "packetDetails": obj.packetDetails,
                "intrusionType": obj.intrusionType,
                "timestamp": obj.timestamp,
                "severity": obj.severity,
                "description": obj.description,
                "notificationDetail": obj.notificationDetail,
            }

            response_data.append(data)
        return Response(data=response_data, status=200)


class IntrusionView(ModelAPIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "intrusionId",
                openapi.IN_QUERY,
                description="Intrusion Id",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: "OK", 400: "No data found."},
        operation_summary="Intrusion details",
        operation_description="""API for details of Intrusion for specific id.
        """,
    )
    def get(self, request):
        """
        Handle GET request for retrieving details of Intrusion for specific id.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response containing details of Intrusion for specific id.
        """
        intrusion_id = request.GET.get("intrusionId")

        if Intrusions.objects.filter(intrusionId=intrusion_id).exists():
            intrusion_obj = Intrusions.objects.get(intrusionId=intrusion_id)

            response_data = {
                "userNname": intrusion_obj.user.username,
                "id": intrusion_obj.intrusionId,
                "packetDetails": intrusion_obj.packetDetails,
                "intrusionType": intrusion_obj.intrusionType,
                "timestamp": intrusion_obj.timestamp,
                "severity": intrusion_obj.severity,
                "description": intrusion_obj.description,
                "notificationDetail": intrusion_obj.notificationDetail,
            }

            status = 200
        else:
            status = 404
            response_data = {"msg": f"No Intrusion details exists for id {id}."}

        return Response(data=response_data, status=status)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "userName": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="User name",
                ),
                "packetDetails": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Details of packet",
                ),
                "intrusionType": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Type of intrusion",
                ),
                "severity": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="severity status",
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Description",
                ),
                "notificationDetail": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Notification details",
                ),
            },
            required=["userName", "packetDetails", "intrusionType", "severity", "description", "notificationDetail"],
        ),
        responses={
            status.HTTP_201_CREATED: "Intrusion saved successfully",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
            status.HTTP_400_BAD_REQUEST: "NOT FOUND",
        },
        operation_summary="Save Intrusion details",
        operation_description="""Save intrusion details and through django signal alert will be created automatically.
        """,
    )
    def post(self, request):
        """
        Handle POST request for storing details of Intrusion.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response containing status of save operation.
        """
        request_data = request.data
        user_name = request_data["userName"]

        if User.objects.filter(username=user_name).exists():
            user_obj = User.objects.get(username=user_name)

            intruion_obj = Intrusions.objects.create(
                user=user_obj,
                packetDetails=request_data["packetDetails"],
                intrusionType=request_data["intrusionType"],
                severity=request_data["severity"],
                description=request_data["description"],
                notificationDetail=request_data["notificationDetail"],
            )

            status = 200
            response_data = {
                "msg": f"Intrusion store successfully with id {intruion_obj.intrusionId}"
            }
        else:
            status = 404
            response_data = {"msg": f"No user exist with name {user_name}"}

        return Response(data=response_data, status=status)


class AllAlertView(ModelAPIView):
    @swagger_auto_schema(
        manual_parameters=[],
        responses={200: "OK", 400: "No data found."},
        operation_summary="All Alert details",
        operation_description="""API for details of all Alert for specific user.
        """,
    )
    def get(self, request):
        """
        Handle GET request for retrieving details of all alert for specific user.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response containing details of all alert for specific user.
        """
        user = request.user

        alert_objs = Alerts.objects.filter(user=user)
        response_data = []

        for alert_obj in alert_objs:

            data = {
                "id": alert_obj.alertId,
                "userName": alert_obj.user.username,
                "intrusionId": alert_obj.intrusion.intrusionId,
                "timestamp": alert_obj.timestamp,
                "severity": alert_obj.severity,
            }

            response_data.append(data)

        return Response(data=response_data, status=200)


class AlertView(ModelAPIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "alertId",
                openapi.IN_QUERY,
                description="Alert Id",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: "OK", 400: "No data found."},
        operation_summary="Alert details",
        operation_description="""API for details of Alert for specific id.
        """,
    )
    def get(self, request):
        """
        Handle GET request for retrieving details of Alert for specific id.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response containing details of Alert for specific id.
        """
        alert_id = request.GET.get("alertId")

        if Alerts.objects.filter(alertId=alert_id).exists():
            alert_obj = Alerts.objects.get(alertId=alert_id)

            response_data = {
                "alertId": alert_obj.alertId,
                "userName": alert_obj.user.username,
                "intrusionId": alert_obj.intrusion.intrusionId,
                "timestamp": alert_obj.timestamp,
                "severity": alert_obj.severity,
            }

            status = 200
        else:
            response_data = {"msg": f"No alert with id {alert_id} exists."}

            status = 404

        return Response(data=response_data, status=status)
