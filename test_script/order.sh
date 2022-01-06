#!/bin/bash
Athorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzQsImV4cCI6MTY0MTQ1MDgxOH0.FUg_ARmb3ZI8ta0RfZGjI33kD7vYazswAP618v8jYbc"

http -v POST 127.0.0.1:8080/orders "Authorization:${Athorization}" cart_id:=${1} 
