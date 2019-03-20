from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from volt_finder.serializers import ChargingStationSerializer, UserSerializer, GeoCStationSerializer
from volt_finder.models import ChargingStation


""" HELPER FUNC """
PASSWORD = 'pAssw0rd?XD'
USERNAME = 'user@example.com'
U_DRIVER = 'DRIVER'
U_OWNER  = 'OWNER'

def create_user(username=USERNAME, password=PASSWORD, group=U_DRIVER):
    return get_user_model().objects.create_user(
        username=username, password=password)
        #TODO add group=group


""" TESTS """
class AuthenticationTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_can_sign_up(self):
        # photo_file = create_photo_file() #TODO: enable user photo
        response = self.client.post(reverse('sign_up'), data={
            'username': USERNAME,
            'first_name': 'Test_name',
            'last_name': 'Test_last',
            'password1': PASSWORD,
            'password2': PASSWORD,
            'group': 'driver',
            # 'photo': photo_file,
        })
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['username'], user.username)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        #self.assertEqual(response.data['group'], user.group) #TODO: enable user gorup (driver or cs_owner)
        #self.assertIsNotNone(user.photo) #TODO: enable user photo ID

    def test_user_can_log_in(self):
        user = create_user()
        response = self.client.post(reverse('log_in'), data={
            'username': user.username,
            'password': PASSWORD,
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['username'], user.username)

    def test_user_can_log_out(self):
        user = create_user()
        self.client.login(username=user.username, password=PASSWORD)
        response = self.client.post(reverse('log_out'))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


class ChargingStationHostTest(APITestCase):
    """ Test all Model-backed API views for CS (only available for cs Owner """
    def setUp(self):
        user = create_user(group=U_OWNER)
        self.client = APIClient()
        self.client.login(username=user.username, password=PASSWORD)   
    
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.cs_t1 = ChargingStation.objects.create(
            address='432 Rue Rachel E, Montreal, QC H2J 2G7, Canada', name='Panthere 1')
        cls.cs_t2 = ChargingStation.objects.create(
            address='1735 Rue Saint-Denis, Montreal, QC H2X 3K4, Canada', name='Panthere 2')
    
    def test_host_can_retrive_cs_list(self):
        """CS creation"""
        response = self.client.get(reverse('main:host_cs_list'))
        # response = self.client.get(reverse('host_cs_list'))
        print('# Response Data', response)

        exp_cs_nks = [self.cs_t1.nk, self.cs_t2.nk]
        print('# exp_cs_nks', exp_cs_nks)
        act_cs_nks = [cs.get('nk') for cs in response.data]
        print('# act_cs_nks', act_cs_nks)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertCountEqual(exp_cs_nks, act_cs_nks)

		# self.assertIsNotNone(self.cs.nk)
		# self.assertIsNotNone(self.cs.created)
		# self.assertIsNotNone(self.cs.updated)
		# self.assertIsNotNone(self.cs.calendar)
		# self.assertEquals(self.cs.owner, self.cs_owner)
    
    # def test_user_can_retrieve_cs_detail_by_nk(self):
    #     cStation = ChargingStation.objects.create(
    #         address='160 Rue Saint Viateur E, Montreal, QC H2T 1A8', name='Panthere 1')
    #     response = self.client.get(cStation.get_absolute_url())
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertEqual(cStation.nk, response.data.get('nk'))

    # def test_host_can_create_cs(self):
	# 	"""CS creation"""