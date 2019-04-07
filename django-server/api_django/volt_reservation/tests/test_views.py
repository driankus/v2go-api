from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from main.serializers import ChargingStationSerializer
from main.models import ChargingStation, EV

from volt_reservation.models import EventCS, EventEV
from datetime import datetime as dt
from volt_reservation.services import ReservationService
import json


""" HELPER FUNC """
PASSWORD = 'pAssw0rd?XD'
USERNAME = 'user@example.com'
U_DRIVER = 'EV_DRIVER'
U_OWNER  = 'CS_HOST'

def create_user(username=USERNAME, password=PASSWORD):
    return get_user_model().objects.create_user(
        username=username, password=password)

def filter_by_cs_event_nk(cs_event, query):
    return list(filter(lambda event_cs: event_cs['cs_event_nk'] == cs_event.cs_event_nk, query))

class TestEventCS(APITestCase):
    def setUp(self):
        self.cs_host = create_user()
        Group.objects.get_or_create(name=U_OWNER)
        # self.cs_host.groups.add(Group.objects.get_or_create(name=U_OWNER))
        self.client = APIClient()
        self.client.login(username=self.cs_host.username, password=PASSWORD)   

        self.cs_t1 = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = -73.5651293,
            cs_host  = self.cs_host,
        )

        self.cs_event_1 = EventCS.objects.create(
        	startDateTime	= dt.strptime('2019-09-25 12:00:00', '%Y-%m-%d %H:%M:%S'),
			endDateTime		= dt.strptime('2019-09-25 12:30:00', '%Y-%m-%d %H:%M:%S'),
			cs 				= self.cs_t1,
			status 			= 'RESERVED'
        )

        self.cs_event_2 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-25 15:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-25 15:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = self.cs_t1,
            status          = 'AVAILABLE'
        )
 
        self.cs_event_3 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-27 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-27 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = self.cs_t1,
            status          = 'AVAILABLE'
        )

        self.cs_event_4 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-28 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-28 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = self.cs_t1,
            status          = 'RESERVED'
        )

    def test_host_can_filter_available_between_certain_time(self):
        response = self.client.get(reverse('volt_reservation:available'), data={
            'start_datetime': '2019-09-25 12:00:00',
            'end_datetime': '2019-09-28 15:30:00'
        })
        
        result = response.data

        self.assertEqual(len(result), 2)
        self.assertFalse(filter_by_cs_event_nk(self.cs_event_1, result))
        self.assertTrue(filter_by_cs_event_nk(self.cs_event_2, result))
        self.assertTrue(filter_by_cs_event_nk(self.cs_event_3, result))
        self.assertFalse(filter_by_cs_event_nk(self.cs_event_4, result))


class TestEventEV(APITestCase):
    def setUp(self):
        self.cs_host = create_user()
        Group.objects.get_or_create(name=U_OWNER)
        # self.cs_host.groups.add(Group.objects.get_or_create(name=U_OWNER))
        
        self.cs_t1 = ChargingStation.objects.create( 
            name     = 'Panthere 1',
            address  = '1251 Rue Jeanne-Mance, Montréal, QC H2X, Canada', 
            lat      = 45.5070394,
            lng      = -73.5651293,
            cs_host  = self.cs_host,
        )

        self.cs_event_1 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-25 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-25 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = self.cs_t1,
            status          = 'AVAILABLE'
        )

        self.cs_event_2 = EventCS.objects.create(
            startDateTime   = dt.strptime('2019-09-28 12:00:00', '%Y-%m-%d %H:%M:%S'),
            endDateTime     = dt.strptime('2019-09-28 12:30:00', '%Y-%m-%d %H:%M:%S'),
            cs              = self.cs_t1,
            status          = 'RESERVED'
        )

        self.ev_driver = create_user(username='test@v2go.io')
        Group.objects.get_or_create(name=U_DRIVER)

        self.ev = EV.objects.create(
            model='Roadster',
            manufacturer='Tesla',
            year=2019, charger_type='A',
            ev_owner=self.ev_driver
        )

        self.client = APIClient()
        self.client.login(username=self.ev_driver.username, password=PASSWORD) 

    def test_driver_can_reserve_available_charging_station(self):
        response = self.client.post(reverse('volt_reservation:reserve_cs'), data={
            'event_cs_nk': self.cs_event_1.nk,
            'ev_nk': self.ev.nk
        })

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['event_cs'], self.cs_event_1.nk)
        self.assertEqual(response.data['ev'], self.ev.nk)

    def test_driver_cannot_reserve_reserved_charging_station(self):
        response = self.client.post(reverse('volt_reservation:reserve_cs'), data={
            'event_cs_nk': self.cs_event_2.nk,
            'ev_nk': self.ev.nk
        })

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)





# class AuthenticationTest(APITestCase):

#     def setUp(self):
#         self.client = APIClient()



#             def test_annon_user_can_not_retrive_cs_detail(self):
#         """ Attempt to access endpoints that require login as annon user (no-login) """
#         cs = ChargingStation.objects.create(
#             address='1735 Rue Saint-Denis, Montréal, QC H2X 3K4, Canada', name='test_cs')
#         response = self.client.get(cs.get_absolute_url())
#         self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
    
#     def test_annon_user_can_not_retrive_cs_list(self):
#         """ Attempt to access endpoints that require login as annon user (no-login) """
#         response = self.client.get(reverse('main:cs_list'))
#         self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)