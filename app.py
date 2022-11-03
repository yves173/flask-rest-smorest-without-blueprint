from flask import Flask,request
from flask_smorest import abort
from db import stores,items
import uuid

app=Flask(__name__)



@app.get('/store')
def get_allStores():
    return {'stores':list(stores.values())}


@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404,'store can not be found!')


@app.post('/store')
def createStore():
    storedata=request.get_json()
    storeID=uuid.uuid4().hex
    new_store={**storedata,'store_id':storeID}
    stores[storeID]=new_store
    return new_store,201


@app.put('/store/<string:store_id>')
def update_store(store_id):
    
    storedata= request.get_json()
    try:
        store=stores[store_id]
        store |=storedata
        return store,201
    except KeyError:
       abort(404,'store can not be found!')


@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {'message':f'store {store_id} is deleted'},201
    except KeyError:
        abort(404,'store can not be found!')


##############################################################################
##############################################################################


@app.get('/item')
def allItems():
    return {'items':list(items.values())}


@app.get('/item/<string:item_id>')
def get_item(item_id):
    
    try:
        return items[item_id]
    except KeyError:
        abort(404,'item can not be found!')


@app.post('/item')
def createItem():
    
    itemdata=request.get_json()
    if itemdata['store_id'] not in stores:
        abort(404,'store can not be found!')

    itemId=uuid.uuid4().hex
    newItem={**itemdata,'item_id':itemId}
    items[itemId]=newItem
    return newItem,201


@app.put('/item/<string:item_id>')
def update_item(item_id):
    itemdata=request.get_json()
    try:
        item=items[item_id]
        item |=itemdata
        return item,201
    except KeyError:
        abort(404,'store can not be found!')


@app.delete('/item/<string:item_id>')
def delete_item(item_id):

    try:
        del items[item_id]
        return {'message':f'item {item_id} is deleted'}
    except KeyError:
        abort(404,'store can not be found!')
