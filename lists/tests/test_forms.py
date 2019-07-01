from django.test import TestCase
from lists.forms import (ItemForm, EMPTY_ITEM_ERROR,
                         ExistingListItemForm, DUPLICATE_ITEM_ERROR)
from lists.models import List, Item


class ItemFormTest(TestCase):
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a To-Do Item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        form = ItemForm(data={'text': 'Sample text', })
        list_ = List.objects.create()
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'Sample text')
        self.assertEqual(new_item.list, list_)


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
        list_=List.objects.create()
        form=ExistingListItemForm(for_list=list_, data={'text':'test'})
        new_item=form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
