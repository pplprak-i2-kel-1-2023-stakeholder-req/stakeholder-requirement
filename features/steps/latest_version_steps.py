from behave import *
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dateutil import parser

@given('I am on "/history/major" page')
def step_given(context):
    context.browser.get('http://127.0.0.1:8000/history/major') 

@when('I press "{major}"')
def step_when_click_major(context, major):
    major_button = context.browser.find_element(By.XPATH, f'//li[contains(text(), "{major}")]')
    major_button.click()

@when('I see "last updated date"')
def step_when_sees_date(context):
    last_updated_text = context.browser.find_element(By.CLASS_NAME, "last_up").text
    last_updated_datetime = parser.parse(last_updated_text, fuzzy=True)
    context.last_updated_timestamp = time.mktime(last_updated_datetime.timetuple())

@when('I press "see new version"')
def step_when_click_latest_version(context):
    # Get the initial timestamp before submitting the form
    initial_timestamp = get_current_timestamp(context)

    # Find the form element and submit it
    search_form = context.browser.find_element(By.ID, "search-form")
    search_form.submit()

    # Wait for the timestamp to change
    WebDriverWait(context.browser, timeout=240).until(
        lambda browser: get_current_timestamp(context) > initial_timestamp
    )

def get_current_timestamp(context):
    last_updated_text = context.browser.find_element(By.CLASS_NAME, "last_up").text
    last_updated_datetime = parser.parse(last_updated_text, fuzzy=True)
    return time.mktime(last_updated_datetime.timetuple())

@then('I should see "the latest stakeholder requirements" in the output page')
def step_then_latest_requirements(context):
    assert "the latest stakeholder requirements" in context.browser.page_source, "Latest requirements not found on the page"

@then('the current date of requirement terms is newer than the previous one')
def step_then_newer_date(context):
    new_timestamp = get_current_timestamp(context)
    assert new_timestamp > context.last_updated_timestamp, "New timestamp is not newer than the stored timestamp, requirements are not updated!"