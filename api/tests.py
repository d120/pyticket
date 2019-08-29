from django.urls import reverse, path, include
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient
from rest_framework.authtoken.models import Token

from ticket.models import Ticket


class APITests(APITestCase, URLPatternsTestCase):
    urlpatterns = [path("api/", include("api.urls"))]

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="apiuser", password="apitest"
        )
        self.token = Token.objects.create(user=self.user)
        self.apiclient = APIClient()
        self.apiclient.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_unauthorized(self):
        """
        Check whether no api endpoint is accesible without authorization
        """
        overviews = ["api:all_tickets", "api:all_users", "api:all_groups"]
        for url in overviews:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 403)

        specifics = ["api:specific_ticket", "api:specific_user", "api:specific_group"]
        for url in specifics:
            response = self.client.get(reverse(url, args=[1]))
            self.assertEqual(response.status_code, 403)

    def test_tickets(self):
        """
        Create and retrieve tickets
        """
        ticket_json = {"name": "API Test Ticket"}
        response = self.apiclient.post(
            reverse("api:all_tickets"), ticket_json, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ticket.objects.get(id=1).name, "API Test Ticket")

        response = self.apiclient.get(
            reverse("api:specific_ticket", args=[1]), format="json"
        )
        self.assertEqual(response.data["name"], "API Test Ticket")

    def test_groups(self):
        """
        Retrieve groups
        """

        group = Group.objects.create(name="apitestgroup")

        response = self.apiclient.get(
            reverse("api:specific_group", args=[group.id]), format="json"
        )
        self.assertEqual(response.data["name"], "apitestgroup")

    def test_users(self):
        """
        Retrieve users
        """
        response = self.apiclient.get(
            reverse("api:specific_user", args=[self.user.id]), format="json"
        )
        self.assertEqual(response.data["username"], "apiuser")
