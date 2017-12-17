"""
Demo Alexa Lambda function

Read along at https://jamesoff.net/alexa-howto
"""

import os
import random

import boto3
from ask import alexa


def lambda_handler(request_obj, context=None):
    metadata = {}

    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default(request):
    return alexa.create_response('You can ask me how many hats either of us is wearing, or to pull a cracker.')


@alexa.intent_handler('PullCracker')
def pull_cracker_handler(request):
    prizes = ['mood fish', 'plastic frog', 'magnifying glass']
    retval = '<say-as interpret-as="interjection">{}</say-as>'.format(random.choice(['boom', 'pop', 'snap']))
    retval = retval + '<break time="0.5s" />'
    winner = random.choice(['alexa', 'user'])
    if winner == 'user':
        retval = retval + 'You won, and you got a {}!'.format(random.choice(prizes))
        hats = increment_hats(request.user_id())
        if hats > 1:
            retval = retval + " You're now wearing {} hats.".format(hats)
    else:
        retval = retval + 'I won, and I got a {}'.format(random.choice(prizes))
        hats = increment_hats(request.user_id() + ':alexa')
        if hats > 1:
            retval = retval + " I'm now wearing {} hats.".format(hats)
    retval = '<speak>{}</speak>'.format(retval)
    return alexa.create_response(
        message=retval,
        end_session=True,
        is_ssml=True
    )


@alexa.intent_handler('CountHats')
def count_hats_handler(request):
    hats = get_hats(request.user_id())
    if hats == 0:
        retval = 'You have no hats.'
    elif hats == 1:
        retval = 'You have one hat.'
    else:
        retval = 'You are wearing {} hats'.format(hats)
    return alexa.create_response(retval, end_session=True)


@alexa.intent_handler('AlexaHats')
def alexa_hats_handler(request):
    """We'll write this function below."""
    pass


def increment_hats(userid):
    hat_info = table.update_item(
        Key={'userid': str(userid)},
        AttributeUpdates={
            'hats': {
                'Action': 'ADD',
                'Value': 1
            }
        },
        ReturnValues='ALL_NEW'
    )
    return hat_info['Attributes']['hats']


def get_hats(userid):
    try:
        hat_info = table.get_item(
            Key={'userid': str(userid)}
        )
        hats = hat_info['Item']['hats']
    except:
        hats = 0
    return int(hats)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['BMOTION_TABLE'])
