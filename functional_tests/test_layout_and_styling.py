from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edith visits the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)

        # She starts a new list and notices that the box is nicely centered there also
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10)