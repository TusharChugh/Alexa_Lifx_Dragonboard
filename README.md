# Alexa_Lifx_Dragonboard
Intergrated Alexa and Lifx bulb

## Hardware required
1. Amazon Echo
2. Lifx Color 1000 bulb: http://www.lifx.com/products/color-1000?variant=8930428227

## Resouces
1. Lifx HTTP API: https://api.developer.lifx.com/
2. Creating a deployment package for AWS lambda function: http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html

## Setup for Lifx app (not required for the demo but still is quite useful)
1. Download Lifx app from the market place
2. Reset the bulb (if it is already paired) and then pair it up with your phone
3. Follow the instructions in the app and complete the setup
4. Make sure that you have claimed the device

## Get the private token
1. Register as a develop for Beta HTTP API's with Lifx
2. Go to https://cloud.lifx.com/settings to get your token. If it doesn't work then use the URL from https://api.developer.lifx.com/docs/authentication

## Clone the code
1. https://github.com/TusharChugh/Alexa_Lifx_Dragonboard.git

## Setup AWS Lambda Function
1. Go to https://console.aws.amazon.com/lambda/
2. Click on 'create a lambda function'
3. Skip
4. Configure triggers -> alexa skills kit, next
5. Give some name and description
6. Runtime python 2.7
7. Compress requests-2.11.1.dist-info, requests and dragonboard.py to dragonboard.zip
8. Code copy entry -> upload a .zip file
9. Handler: dragonboard.lambda_handler
10. Create rule (lambda_basic_execution)
11. Next -> Complete Function
12. In dragonboard.py paste the token obtained from Lifx

## Set up Alexa skills Kit
1. Go to https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit
2. Click on 'create a skill now' (you will need to sign in with your amazon account)
3. Click on 'add a new skill' button
4. On skill information tab, give invocation name as 'dragonboard' and a name of your choice
5. Go to interaction mode tab, first add custom slot type from 'custom_slot_types.txt'
  e.g: Type: LIST_OF_COLORS	
        Value: red 
        green
        blue
        orange
        pink
        white
        yellow
        violet
        cyan
6. Copy the content of intent_schema.json and sample_utterance.txt as is
7. Go to configuration tab, select Lambda ARN (you can get this ARN on the top of 'Lamda function' which was created in the previous section
8. Go to test tab: Sample utterance->Enter Utterance->Alexa tell dragonboard, I am feeling blue
9. You should see the bulb change the color and the result in Lambda response

