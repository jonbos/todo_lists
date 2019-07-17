import unittest
from django.contrib.auth import get_user_model
from unittest.mock import patch, Mock
User = get_user_model()
from django.test import TestCase
from unittest import skip
from lists.models import Item, List
from lists.forms import (ItemForm, EMPTY_ITEM_ERROR,
                         DUPLICATE_ITEM_ERROR, ExistingListItemForm)
from django.utils.html import escape
from django.http import HttpRequest
from lists.views import new_list


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class NewListViewIntegratedTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirect_after_POST(self):
        response = self.client.post(
            '/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_invalid_input_renders_home_template(self):
        response = self.client.post(
            '/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_shown_on_home_page(self):
        response = self.client.post(
            '/lists/new', data={'text': ''})
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_form_passed_in_response_after_validation_error(self):
        response = self.client.post(
            '/lists/new', data={'text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved_but_show_error(self):
        self.client.post(
            '/lists/new', data={'text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)



    def test_list_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/lists/new', data={'text': 'a new item'})
        list_ = List.objects.first()
        self.assertEqual(list_.owner, user)


@patch('lists.views.NewListForm')
class NewListViewUnitTest(unittest.TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['text'] = 'a new list item'
        self.request.user = Mock()

    def test_passes_POST_data_to_NewListForm(self, mockNewListForm):

        new_list(self.request)
        mockNewListForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_with_owner_if_form_valid(self, mockNewListForm):
        mockForm = mockNewListForm.return_value
        mockForm.is_valid.return_value = True
        new_list(self.request)
        mockForm.save.assert_called_once_with(owner=self.request.user)

    @patch('lists.views.redirect')
    def test_redirects_to_form_returned_object_if_valid(self, mock_redirect, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = True

        response = new_list(self.request)

        self.assertEqual(response, mock_redirect.return_value)

        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('lists.views.render')
    def test_renders_home_template_if_form_is_invalid(self, mock_render, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False

        response = new_list(self.request)

        self.assertEqual(response, mock_render.return_value)

        mock_render.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form})

    def test_does_not_save_if_form_is_invalid(self, mockNewListForm):
        mock_form = mockNewListForm.return_value
        mock_form.is_valid.return_value = False
        new_list(self.request)
        self.assertFalse(mock_form.save.called)


class ListViewTest(TestCase):

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/', data={'text': ''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, 'list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, 'list.html')

    def test_only_displays_list_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='Number one', list=correct_list)
        Item.objects.create(text='Number two', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(
            text='Other list number one', list=other_list)
        Item.objects.create(
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

    def test_can_save_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            path=f'/lists/{correct_list.id}/', data={'text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):

        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            path=f'/lists/{correct_list.id}/',
            data={'text': 'A new list item'})
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        response = self.client.post(
            f'/lists/{list_.id}/', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="test")

        response = self.client.post(
            path=f'/lists/{list1.id}/', data={'text': 'test'})
        expected_error = escape(DUPLICATE_ITEM_ERROR)

        self.assertTemplateUsed(response, 'list.html')
        self.assertContains(response, expected_error)
        self.assertEqual(Item.objects.all().count(), 1)


class MyListTests(TestCase):
    def test_my_list_url_renders_my_list_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertTemplateUsed(response, 'my_lists.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='wrong@wrong.wrong')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/lists/users/a@b.com/')
        self.assertEqual(response.context['owner'], correct_user)
