import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH_TO_PHANTOM = os.getenv("path_to_phantom")

target_URL = "http://atomicboard.devman.org/"

create_user_URL = "http://atomicboard.devman.org/create_test_user/"

jquery_url = "http://code.jquery.com/jquery-1.11.2.min.js"


def find_elements(driver, method, element):
    if method == "css_selector":
        return driver.find_elements_by_css_selector(element)
    if method == "class_name":
        return driver.find_elements_by_class_name(element)
    if method == "tag_name":
        return driver.find_elements_by_tag_name(element)


class AtomicBoardTest(unittest.TestCase):

    @classmethod
    def setUpClass(AtomicBoardTest):
        AtomicBoardTest.driver = webdriver.PhantomJS(PATH_TO_PHANTOM)
        AtomicBoardTest.driver.set_window_size(1120, 550)
        AtomicBoardTest.driver.implicitly_wait(5)
        AtomicBoardTest.css_selector_for_ticket = "div.js-ticket"
        AtomicBoardTest.class_for_add_ticket_btn = "add-ticket-block_button"
        AtomicBoardTest.class_for_add_ticket_input = "editable-has-buttons"
        AtomicBoardTest.class_for_ticket_text = "panel-heading_text"
        AtomicBoardTest.class_name_for_eddit_ticket_input = "editable-input"
        AtomicBoardTest.class_name_for_ticket_status = "ticket_status"
        AtomicBoardTest.css_selector_for_ticket_column = "span.tickets-column"
        driver = AtomicBoardTest.driver
        driver.get(create_user_URL)
        button = find_elements(driver, "tag_name", "button")[0]
        button.click()

    def setUp(self):
        self.driver.get(target_URL)

    def test_if_page_served(self):
        self.assertIn(
            "AtomicBoard",
            self.driver.title,
            msg="Не удалось загрузить страницу")

    def test_if_tickets_present(self):
        driver = self.driver
        tickets = find_elements(driver, "css_selector",
                                AtomicBoardTest.css_selector_for_ticket)
        self.assertTrue(tickets, msg="Не удалось загрузить список задач")

    def test_create_new_ticket(self):
        driver = self.driver
        num_tickets = len(find_elements(
            driver,
            "css_selector",
            AtomicBoardTest.css_selector_for_ticket))
        elem = find_elements(driver, "class_name",
                             AtomicBoardTest.class_for_add_ticket_btn)[0]
        elem.click()
        input_elem = find_elements(
            driver,
            "class_name",
            AtomicBoardTest.class_for_add_ticket_input)[0]
        input_elem.clear()
        input_elem.send_keys("Go to Pycon")
        input_elem.send_keys(Keys.RETURN)
        time.sleep(5)
        new_num_of_tickets = len(find_elements(
            driver, "css_selector", AtomicBoardTest.css_selector_for_ticket))
        self.assertGreater(new_num_of_tickets, num_tickets,
                           msg="Не удалось создать новую задачу")

    def test_edit_ticket(self):
        driver = self.driver
        ticket_text = find_elements(
            driver, "class_name", AtomicBoardTest.class_for_ticket_text)[0]
        ticket_text.click()
        new_ticket_text = "go to meetup"
        input_field = find_elements(
            driver,
            "class_name",
            AtomicBoardTest.class_name_for_eddit_ticket_input
        )[0]
        input_field.clear()
        input_field.send_keys(new_ticket_text)
        input_field.send_keys(Keys.RETURN)
        ticket_text = find_elements(
            driver, "class_name", AtomicBoardTest.class_for_ticket_text)[0]
        self.assertEqual(ticket_text.text, new_ticket_text,
                         msg="Не удалось отредактировать задачу")

    def test_mark_ticket_complete(self):
        driver = self.driver
        ticket_status = find_elements(
            driver,
            "class_name",
            AtomicBoardTest.class_name_for_ticket_status
        )[0]
        ticket_status.click()
        time.sleep(5)
        button_close_ticket = find_elements(
            driver, "class_name", "btn-primary")[0]
        ticket_new_status = button_close_ticket.text
        button_close_ticket.click()
        ticket_status = find_elements(
            driver,
            "class_name",
            AtomicBoardTest.class_name_for_ticket_status
        )[0].text
        self.assertEqual(ticket_status, ticket_new_status,
                         msg="Не удалось изменить статус задачи")

    def test_drag_and_drop(self):
        driver = self.driver
        driver.set_script_timeout(30)
        tickets_columns = find_elements(
            driver,
            "css_selector",
            AtomicBoardTest.css_selector_for_ticket_column
        )
        tickets_second_column = tickets_columns[1]
        tickets_in_second_column = tickets_second_column.\
            find_elements_by_css_selector(
                AtomicBoardTest.css_selector_for_ticket
            )
        num_tickets_in_second_column = len(tickets_in_second_column)
        with open("jquery_load_helper.js") as f:
            load_jquery_js = f.read()
        with open("drag_and_drop_helper.js") as f:
            drag_and_drop_js = f.read()
        driver.execute_async_script(load_jquery_js, jquery_url)
        driver.execute_script(
            drag_and_drop_js +
            "$('div.js-ticket:eq(0)')."
            "simulateDragDrop({ dropTarget:"
            "'span.tickets-column:eq(1)'});"
        )
        new_tickets_in_second_column = tickets_second_column.\
            find_elements_by_css_selector(
                AtomicBoardTest.css_selector_for_ticket
            )
        new_num_of_tickets_in_second_column = len(new_tickets_in_second_column)
        self.assertEqual(
            new_num_of_tickets_in_second_column,
            num_tickets_in_second_column + 1,
            msg="Не удалось перетащить задачу в другую колонку")

    @classmethod
    def tearDownClass(AtomicBoardTest):
        AtomicBoardTest.driver.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
