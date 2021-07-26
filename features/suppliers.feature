Feature: The supplier service back-end
    As a shopping website manager
    I need a RESTful catalog service
    So that I can keep track of all my suppliers

Background: 
    Given the following suppliers
        | name | phone | address | available | product_list | rating |
        | Graves, Thompson and Pena | 620-179-7652 | 5312 Danielle Spurs Apt. 017\nNorth James, SD 47183 | True | 1,2,4,5 | 3.5 |
        | Rogers, Cabrera and Lee | 011-526-6218 | 59869 Padilla Stream Apt. 194\nWest Tanyafort, KY 73107 | False | 1,2,3,5 | 4.8 |
        | Perez LLC | 6574-477-5210 | 41570 Ashley Manors\nNorth Kevinchester, FL 68266 | True | 1,2,3 | 2.7 |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Supplier RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Update a Supplier
    When I visit the "Home Page"
    And I set the "Name" to "Perez LLC"
    And I press the "Search" button
    Then I should see "Perez LLC" in the "Name" field
    And I should see "6574-477-5210" in the "Phone" field
    When I change "Phone" to "6574-477-5212"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "6574-477-5212" in the "Phone" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "6574-477-5212" in the results
    Then I should not see "6574-477-5210" in the results

Scenario: Delete a Supplier
    When I visit the "Home Page"
    And I set the "Name" to "Perez LLC"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Perez LLC" in the results
    When I press the "Delete" button
    Then I should see the message "Supplier has been Deleted!"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should not see "Perez LLC" in the results