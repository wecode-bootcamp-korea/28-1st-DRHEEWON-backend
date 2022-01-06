#!/bin/bash
http -v OPTIONS http://062c-211-106-114-186.ngrok.io/carts "Authorization:${Athorization}"
Athorization="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzQsImV4cCI6MTY0MTUyMDI0NH0.2qLf-fKTaAl3ZvhbiEODeyEVKTkdIj7dQnnfrY4_jG4"
http -v GET http://062c-211-106-114-186.ngrok.io/carts "Authorization:${Athorization}"
