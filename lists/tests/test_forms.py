from django.test import TestCase
from lists.forms import (ItemForm, EMPTY_ITEM_ERROR,
                         ExistingListItemForm, DUPLICATE_ITEM_ERROR, NewListForm)
from lists.models import List, Item
import unittest
from unittest.mock import Mock, patch


class ItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a To-Do Item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])


class ExistingItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a To-Do Item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validaiton_for_duplicate_items(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_, text="duplicate")
        form = ExistingListItemForm(
            for_list=list_, data={'text': 'duplicate', })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [
                         "You've already got that on your list"])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'test'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])


class NewListFormTest(unittest.TestCase):

    @patch('lists.forms.List.create_new')
    def test_save_creates_list_from_POST_data_if_user_is_not_authenticated(self, mock_List_create_new):
        user = Mock(is_authenticated=False)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text')

    @patch('lists.forms.List.create_new')
    def test_save_creates_list_with_owner_if_user_is_authenticated(self, mock_List_create_new):
        user = Mock(is_autheticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        form.save(owner=user)
        mock_List_create_new.assert_called_once_with(
            first_item_text='new item text', owner=user)

    @patch('lists.forms.List.create_new')
    def test_form_save_returns_new_List_object(self, mock_List_create_new):
        user = Mock(is_autheticated=True)
        form = NewListForm(data={'text': 'new item text'})
        form.is_valid()
        response = form.save(owner=user)
        self.assertEqual(response, mock_List_create_new.return_value)
