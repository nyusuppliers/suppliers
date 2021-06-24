Introduction

This project is the back end for an eCommerce web site as a RESTful microservice for the suppliers.
 An supplier is a vendor from whom we get products from. This microservice 
supports the complete Create, Read, Update, & Delete (CRUD) lifecycle.


VENDOR Model Attributes:
	=> ID (primary key, auto incremented)
	=> NAME
	=> EMAIL
	=> PHONE
	=> ADDRESS
	=> GENDER
	=> AVAILABLE
	=> PRODUCTS(reference table)
====================================================================================================================================
VENDOR API Routes:
------------------------------------------------------------------------------------------------------------------------------------
	API           METHOD      URL              PARAMS                                           
------------------------------------------------------------------------------------------------------------------------------------
	List all      GET        /vendors

	Get Single    GET        /vendors/<id>

	Search        GET        /vendors/search   name, phone or email in query

	Create        POST       /vendors          name, phone, email, available, gender, and address

	Update        PUT        /vendors/<id>     name, phone, email, available, gender, and address

	Delete        DELETE     /vendors/<id>     none

	Make Available GET       /vendors/<id>/make-available
====================================================================================================================================
PRODUCT Model Attributes:
	=> ID (primary key, auto inc)
	=> NAME
	=> PRICE
	=> VENDOR_ID
====================================================================================================================================
PRODUCT API Routes:
------------------------------------------------------------------------------------------------------------------------------------
	API                METHOD      URL                 PARAMS
------------------------------------------------------------------------------------------------------------------------------------
	List all           GET         /products   

	Get single         GET         /products/<id>

	Search             GET         /products/search     by name or price or vendor_id

	Create             POST        /products            name, price, vendor_id

	Update             PUT         /products/<id>       name, price, vendor_id

	Delete             DELETE      /products/<id>

	Find by vendorid   GET         /products/find-by-vendor/<vendor_id>
====================================================================================================================================