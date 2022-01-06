#!/bin/bash
Athorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzQsImV4cCI6MTY0MTUyMDI0NH0.2qLf-fKTaAl3ZvhbiEODeyEVKTkdIj7dQnnfrY4_jG4"
http -v GET 127.0.0.1:8080/carts "Authorization:${Athorization}"
