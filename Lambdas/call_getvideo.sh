#!/bin/bash

# $1 Is the JSON file with the variables and keys inside
event=$( cat $1 )
echo $event

curl -X POST https://4od3mhmz7k.execute-api.us-east-1.amazonaws.com/VtoF/ \
  -H "Content-Type: application/json" \
  -d  "$event"