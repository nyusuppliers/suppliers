"""
Supplier Steps

Steps file for Suppliers.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import json
import requests
from behave import given
from compare import expect 

@given('the following suppliers')
def step_impl(context):
    """ Delete all suppliers and load new ones"""
    headers = {"Content-Type": "application/json", "X-Api-Key":"API_KEY"}
    context.resp = requests.get(context.base_url + '/api/suppliers')
    expect(context.resp.status_code).to_equal(200)
    for supplier in context.resp.json():
        context.resp = requests.delete(context.base_url + '/api/suppliers/' + str(supplier["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)
    
    # load the database with new pets
    create_url = context.base_url + '/api/suppliers'
    for row in context.table:
        print(row)
        product_list = [int(product) for product in row['product_list'].split(",")]
        data = {
            "name": row['name'],
            "phone": row['phone'],
            "address": row['address'],
            "available": row['available'] in ['True', 'true', '1'],
            "product_list": product_list,
            "rating": float(row['rating'])
            }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)