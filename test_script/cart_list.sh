#!/bin/bash
Athorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzQsImV4cCI6MTY0MTM1MDY5N30.1KtsmgxHsUYqhBKUaEUbR-iOFhCFpmkPMeBBC8v9fGI"
http -v GET 127.0.0.1:8080/carts "Authorization:${Athorization}"
