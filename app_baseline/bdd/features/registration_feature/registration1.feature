Feature: User Registration

  Scenario Outline: Registering a new user
    Given I am on the registration page
    When I enter username "<username>" and email "<email>" and password1 "<password1>" and password2 "<password2>" and RegistrationCode "<registration_code>"
    And I click the registration "Register" button
    Then I should see registration "Your account <email> has been created"

    Given I am on the login page
    When I enter email "<email>" and password "<password1>"
    And I click the login "Login" button
    Then I should see login "Welcome <username>"
    
    Then I close the browser

    Examples:
      | username  | email       | password1 | password2 | registration_code |
      | new_user121  | user121@one.com | test2@456 | test2@456 | abcd1             |

