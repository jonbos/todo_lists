from django.test import TestCase
from lists.models import Item, List
from django.utils.html import escape

class HomePageTest(TestCase):

    def test_uses_home_template(self):

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirect_after_POST(self):
        response = self.client.post(
            '/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post(
            '/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        response = self.client.post(
            '/lists/new', data={'item_text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)



class NewItemTest(TestCase):

    def test_can_save_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            path=f'/lists/{correct_list.id}/add_item', data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_after_POST(self):

        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            path=f'/lists/{correct_list.id}/add_item', data={'item_text': 'A new list item'})

        self.assertRedirects(response, f'/lists/{correct_list.id}/')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, 'list.html')

    def test_only_displays_list_items_for_that_list(self):
        correct_list = List.objects.create()
        item_one = Item.objects.create(text='Number one', list=correct_list)
        item_two = Item.objects.create(text='Number two', list=correct_list)

        other_list = List.objects.create()
        other_item_one = Item.objects.create(
            text='Other list number one', list=other_list)
        other_item_two = Item.objects.create(
            text='Other list number two', list=other_list)
        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'Number one')
        self.assertContains(response, 'Number two')
        self.assertNotContains(response, 'Other list number one')
        self.assertNotContains(response, 'Other list number two')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context['list'], correct_list)