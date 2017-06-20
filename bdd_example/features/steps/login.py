from behave import given, when, Then
from django.contrib.auth.models import User
from test.factories.user import UserFactory


@given('an anonymous user')
def step_impl(context):
    # Creates a dummy user for our tests (user is not authenticated at this point)
    user = UserFactory(username='foo', email='foo@example.com')
    user.set_password('bar')
    user.save()


@when('I submit a valid login page')
def step_impl(context):
    browser = context.browser
    browser.get(context.base_url + '/login/')

    # Checks for Cross-Site Request Forgery protection input
    assert browser.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    # Fill login form and submit it (valid  version)
    browser.find_element_by_name('username').send_keys('foo')
    browser.find_element_by_name('password').send_keys('bar')
    browser.find_element_by_name('submit').click()


@when('I submit an invalid login page')
def step_impl(context):
    browser = context.browser

    browser.get(context.base_url + '/login/')

    # Checks for Cross-Site Request Forgery protection input (once again)
    assert browser.find_element_by_name('csrfmiddlewaretoken').is_enabled()

    # Fill login form and submit it (invalid version)
    browser.find_element_by_name('username').send_keys('foo')
    browser.find_element_by_name('password').send_keys('bar-is-invalid')
    browser.find_element_by_name('submit').click()


@then('I am redirected to the login success page')
def step_impl(context):
    browser = context.browser

    # Check success status
    assert browser.current_url.endswith('/login/success/')
    assert browser.find_element_by_id('main_title').text == 'Login success'


@then('I am redirected to the login fail page')
def step_impl(context):
    browser = context.browser

    # Checks redirection URL
    assert browser.current_url.endswith('/login/fail/')
    assert browser.find_element_by_id('main_title').text == 'Login failure'
