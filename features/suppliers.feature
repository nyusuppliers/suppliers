Feature: The supplier service back-end
    As a shopping website manager
    I need a RESTful catalog service
    So that I can keep track of all my suppliers

Background: 
    Given the following suppliers
        | name | phone | address | available | product_list | rating |
        | Graves, Thompson and Pena | 620-179-7652 | 5312 Danielle Spurs Apt. 017\nNorth James, SD 47183 | True | 1,2,4,5 | 3.5 |
        | Rogers, Cabrera and Lee | 011-526-6218 | 59869 Padilla Stream Apt. 194\nWest Tanyafort, KY 73107 | False | 1,2,3,5 | 4.8 |
        | Perez LLC | 6574-477-5210 | 41570 Ashley Manors\nNorth Kevinchester, FL 68266 | True | 1,2,3 | 1.7 |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Supplier RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Supplier
    When I visit the "Home Page"
    And I set the "Name" to "Perez LLC"
    And I set the "Phone" to "657-477-5265"
    And I select "False" in the "Available" dropdown
    And I set the "Address" to "221B Baker Street London"
    And I set the "Product_List" to "[1,2,3]"
    And I set the "Rating" to "4"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Phone" field should be empty
    And the "Address" field should be empty
    And the "Product_List" field should be empty
    And the "Rating" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Perez LLC" in the "Name" field
    And I should see "657-477-5265" in the "Phone" field
    And I should see "False" in the "Available" dropdown
    And I should see "221B Baker Street London" in the "Address" field
    And I should see "[1,2,3]" in the "Product_List" field
    And I should see "4" in the "Rating" field

Scenario: Retrieve a Supplier
    When I visit the "Home Page"
    And I set the "name" to "Perez LLC"
    And I press the "Retrieve" button
    Then I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Phone" field should be empty
    And the "Address" field should be empty
    And the "Product_List" field should be empty
    And the "Rating" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Perez LLC" in the "Name" field
    And I should see "657-477-5265" in the "Phone" field
    And I should see "False" in the "Available" dropdown
    And I should see "221B Baker Street London" in the "Address" field
    And I should see "[1,2,3]" in the "Product_List" field
    And I should see "1.7" in the "Rating" field

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

Scenario: Penalize a Supplier
    When I visit the "Home Page"
    And I set the "Name" to "Perez LLC"
    And I press the "Search" button
    Then I should see "Perez LLC" in the "Name" field
    And I should see "1.7" in the "Rating" field
    When I press the "Penalize" button
    Then I should see the message "Supplier has been Penalized!"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "0.7" in the "Rating" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "0.7" in the results

    When I press the "Clear" button
    And I set the "Name" to "Perez LLC"
    And I press the "Search" button
    Then I should see "Perez LLC" in the "Name" field
    And I should see "0.7" in the "Rating" field
    When I press the "Penalize" button
    Then I should see the message "Supplier has been Penalized!"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "0" in the "Rating" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "0" in the results

Scenario: List all suppliers
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see "Graves, Thompson and Pena" in the results
    And I should see "Rogers, Cabrera and Lee" in the results
    And I should see "Perez LLC" in the results

Scenario: Query suppliers
    When I visit the "Home Page"
    And I set the "Name" to "Perez LLC"
    And I press the "Search" button
    Then I should see "Perez LLC" in the "Name" field
    Then I should see "Perez LLC" in the results
    When I press the "Clear" button
    And I set the "Phone" to "011-526-6218"
    And I press the "Search" button
    Then I should see "Rogers, Cabrera and Lee" in the results
    Then I should not see "Perez LLC" in the results
    When I press the "Clear" button
    And I set the "Address" to "59869 Padilla Stream Apt. 194\nWest Tanyafort, KY 73107"
    And I press the "Search" button
    Then I should see "59869 Padilla Stream Apt. 194\nWest Tanyafort, KY 73107" in the results
    Then I should not see "Perez LLC" in the results
    When I press the "Clear" button
    And I set the "Rating" to "3.4"
    And I press the "Search" button
    Then I should see "Rogers, Cabrera and Lee" in the results
    Then I should see "Graves, Thompson and Pena" in the results
    Then I should not see "Perez LLC" in the results
    When I press the "Clear" button
    And I select "True" in the "Available" dropdown
    And I press the "Search" button
    Then I should not see "Rogers, Cabrera and Lee" in the results
    Then I should see "Graves, Thompson and Pena" in the results
    Then I should see "Perez LLC" in the results
    When I press the "Clear" button
    And I set the "Product_List" to "1"
    And I press the "Search" button
    Then I should see "Rogers, Cabrera and Lee" in the results
    Then I should see "Graves, Thompson and Pena" in the results
    Then I should see "Perez LLC" in the results
