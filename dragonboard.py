"""
Modified from alexa's sample code
"""

from __future__ import print_function

import requests
import json

token = "c6760aad6568e3ed26b59535a20ce9cf5f2ea3d809e1323e473f4a8f644bbb5e"

headers = {
    "Authorization": "Bearer %s" % token,
}

bulb_color = "green"
bulb_state = "on"

def control_bulb(state, color):
    global bulb_state
    bulb_state = state
    global bulb_color
    bulb_color = color
    print("bulb state: ", bulb_state, "bulb color ", bulb_color)
    payload = {
      "states": [
        {
            "selector" : "all",
        },
      ],
      "defaults": {
        "power": bulb_state,
        "color": bulb_color,
        "duration": 1.0
        }
    }

    response = requests.put('https://api.lifx.com/v1/lights/states', data=json.dumps(payload), headers=headers)
    print(response.content)


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ChangeColorEmotion":
        return set_color_in_session(intent, session)
    elif intent_name == "ChangeColorRequest":
        return set_color_in_session(intent, session)
    elif intent_name == "ChangeState":
        return set_state_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Sure " 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Sure" 
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "  "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def set_color_in_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    if 'Color' in intent['slots']:
        bulb_color = intent['slots']['Color']['value']
        control_bulb("on", bulb_color)
        session_attributes = create_favorite_color_attributes(bulb_color)
        speech_output = "ok "
        reprompt_text = "Change color to " + bulb_color
    else:
        speech_output = "You can tell me that I am feeling blue"
        reprompt_text = "You can tell me that I am feeling blue"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_state_from_session(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    if 'State' in intent['slots']:
        bulb_state = intent['slots']['State']['value']
        control_bulb(bulb_state, "white")
        session_attributes = create_favorite_color_attributes(bulb_state)
        speech_output = "ok "
        reprompt_text = "Switched bulb " + bulb_state
    else:
        speech_output = "You can tell me to switch the bulb on or off"
        reprompt_text = "You can tell me to switch the bulb on or off"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
