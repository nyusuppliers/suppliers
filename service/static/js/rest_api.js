$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#supplier_id").val(res.id);
        $("#supplier_name").val(res.name);
        $("#supplier_rating").val(res.rating);
        $("#supplier_address").val(res.address);
        $("#supplier_product_list").val(JSON.stringify(res.product_list));
        $("#supplier_phone").val(res.phone);
        if (res.available == true) {
            $("#supplier_available").val("true");
        } else {
            $("#supplier_available").val("false");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#supplier_name").val("");
        $("#supplier_phone").val("");
        $("#supplier_rating").val("");
        $("#supplier_address").val("");
        $("#supplier_available").val("");
        $("#supplier_product_list").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Supplier
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#supplier_name").val();
        var phone = $("#supplier_phone").val();
        var rating = $("#supplier_rating").val();
        var address = $("#supplier_address").val();
        var available = $("#supplier_available").val() == "true";
        var product_list = $("#supplier_product_list").val();
        var data = {
            "name": name,
            "address": address,
            "phone": phone,
            "rating": rating,
            "available": available,
            "product_list":JSON.parse(product_list)
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/suppliers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Supplier
    // ****************************************

    $("#update-btn").click(function () {

        var supplier_id = $("#supplier_id").val();
        var name = $("#supplier_name").val();
        var phone = $("#supplier_phone").val();
        var rating = $("#supplier_rating").val();
        var address = $("#supplier_address").val();
        var available = $("#supplier_available").val() == "true";
        var product_list = $("#supplier_product_list").val();

        var data = {
            "name": name,
            "address": address,
            "phone": phone,
            "rating": rating,
            "available": available,
            "product_list":JSON.parse(product_list)
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/suppliers/" + supplier_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Supplier
    // ****************************************

    $("#retrieve-btn").click(function () {

        var supplier_id = $("#supplier_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/suppliers/" + supplier_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Supplier
    // ****************************************

    $("#delete-btn").click(function () {

        var supplier_id = $("#supplier_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/suppliers/" + supplier_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Supplier has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#supplier_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Supplier
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#supplier_name").val();
        var rating = $("#supplier_rating").val();
        var phone = $("#supplier_phone").val();
        var address = $("#supplier_address").val();
        var available = $("#supplier_available").val() == "true";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (phone) {
            if (queryString.length > 0) {
                queryString += '&phone=' + phone
            } else {
                queryString += 'phone=' + phone
            }
        }
        if (address) {
            if (queryString.length > 0) {
                queryString += '&address=' + address
            } else {
                queryString += 'address=' + address
            }
        }
        if (rating) {
            if (queryString.length > 0) {
                queryString += '&rating=' + rating
            } else {
                queryString += 'rating=' + rating
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&available=' + available
            } else {
                queryString += 'available=' + available
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/suppliers?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10"></table');
            var header = `<thead>
            <tr>
                <th class="col-md-1 p-0 m-0">ID</th>
                <th class="col-md-2">Name</th>
                <th class="col-md-2">Phone</th>
                <th class="col-md-2">Address</th>
                <th class="col-md-1">Available</th>
                <th class="col-md-2">Rating</th>
                <th class="col-md-2">Product List</th>
            </tr>
            </thead><tbody></tbody>`;
            $("#search_results table").append(header);
            var firstSupplier = "";
            for(var i = 0; i < res.length; i++) {
                var supplier = res[i];
                var row = "<tr><td class='col-md-1'>"+supplier.id+"</td><td class='col-md-2'>"+supplier.name+"</td><td class='col-md-2'>"+supplier.phone+"</td><td class='col-md-2'>"+supplier.address+"</td><td class='col-md-1'>"+supplier.available+"</td><td class='col-md-2'>"+supplier.rating+"</td><td class='col-md-2'>"+JSON.stringify(supplier.product_list)+"</td></tr>";
                $("#search_results table tbody").append(row);
                if (i == 0) {
                    firstSupplier = supplier;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstSupplier != "") {
                update_form_data(firstSupplier)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
