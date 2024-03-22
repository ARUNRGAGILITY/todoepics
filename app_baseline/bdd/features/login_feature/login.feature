Feature: User Login

  Scenario: Logging in
    Given I am on the login page
    When I enter email "test1@none.com" and password "test@456"
    And I click the login "Login" button
    Then I should see login "Login successful"
    Then I close the browser
