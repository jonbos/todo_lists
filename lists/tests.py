import sys

from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_POST_request(self):
        response = self.client.post(
            path='/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_only_saves_items_when_necessary(self):
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_redirects_after_POST(self):
        response = self.client.post(
            path='/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_displays_all_list_items(self):
        item_one=Item.objects.create(text='Pee')
        item_two=Item.objects.create(text='Poop')

        response=self.client.get('/')

        self.assertIn('Pee', response.content.decode())
        self.assertIn('Poop', response.content.decode())


class ListItemTest(TestCase):

    def test_saving_and_retreiving_items(self):
        first_item = Item()
        first_item.text = "The first ever list item"
        first_item.save()

        second_item = Item()
        second_item.text = "The second list item"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, "The first ever list item")
        self.assertEqual(second_saved_item.text, "The second list item")
