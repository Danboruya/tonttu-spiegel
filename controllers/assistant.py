#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import json
import os.path
import os
import pathlib2 as pathlib

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file
from google.assistant.library.device_helpers import register_device

import argparse
import subprocess
import application


try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


WARNING_NOT_REGISTERED = """
    This device is not registered. This means you will not be able to use
    Device Actions or see your device in Assistant Settings. In order to
    register this device follow instructions at:

    https://developers.google.com/assistant/sdk/guides/library/python/embed/register-device
"""


def synthesize_text(cmd, assistant):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()
    assistant.stop_conversation()

    input_text = texttospeech.types.SynthesisInput(text=cmd)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US', name='en-US-Wavenet-F')

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    with open('voice/response.mp3', 'wb') as out:
        out.write(response.audio_content)
        # print('Audio content written to file "output.mp3"')
    print(cmd)
    print()
    # assistant.stop_conversation()
    subprocess.call("mpg321 ./voice/response.mp3", shell=True)


def custom_command(event, assistant):
    if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        cmd = event.args["text"]
        print()
        print("You sed: {}".format(cmd))
        print()
        if 'echo' in cmd and ('message' in cmd):
            # synthesize_text("Now I\'m online.", assistant)
            synthesize_text(application.print_command(cmd), assistant)
            assistant.stop_conversation()
            cmd = ""
            return 1
        elif ('who' in cmd and ('is' in cmd and 'in' in cmd and 'the' in cmd and ('lab' in cmd or 'Lab' in cmd))) or ('who' in cmd and ('is' in cmd and 'in' in cmd and ('lab' in cmd or 'Lab' in cmd))):
            # synthesize_text(get_room_members(), assistant)
            assistant.stop_conversation()
            cmd = ""
            return 1
        elif 'show' in cmd and (('me' in cmd) and ('the' in cmd) and ('member' in cmd) and ('status' in cmd)):
            # synthesize_text(get_all_member_status(), assistant)
            assistant.stop_conversation()
            cmd = ""
            return 1
        elif 'set' in cmd and (('in' in cmd and ('lab' in cmd or 'Lab' in cmd)) or
                               ('do' in cmd and 'not' in cmd and 'disturb' in cmd) or
                               ('in' in cmd and 'University' in cmd) or
                               ('outside' in cmd and 'University' in cmd)):
            # synthesize_text(set_member_status(cmd), assistant)
            cmd = ""
            assistant.stop_conversation()
            return 1
        elif 'application' in cmd and 'help' in cmd:
            # synthesize_text(bot_help(), assistant)
            assistant.stop_conversation()
            cmd = ""
            return 1
        else:
            return 0
    return 0


def process_event(event, assistant):
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
        assistant: Assistant object.
    """
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print()
    print(event)
    flag = custom_command(event, assistant)
    print()
    # if flag == 1:
    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
            print()
    if event.type == EventType.ON_DEVICE_ACTION:
        for command, params in event.actions:
            print('Do command', command, 'with params', str(params))
    # else:
    #     pass


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--device-model-id', '--device_model_id', type=str,
                        metavar='DEVICE_MODEL_ID', required=False,
                        help='the device model ID registered with Google')
    parser.add_argument('--project-id', '--project_id', type=str,
                        metavar='PROJECT_ID', required=False,
                        help='the project ID used to register this device')
    parser.add_argument('--device-config', type=str,
                        metavar='DEVICE_CONFIG_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'googlesamples-assistant',
                            'device_config_library.json'
                        ),
                        help='path to store and read device configuration')
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='path to store and read OAuth2 credentials')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + Assistant.__version_str__())

    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    device_model_id = None
    last_device_id = None
    try:
        with open(args.device_config) as f:
            device_config = json.load(f)
            device_model_id = device_config['model_id']
            last_device_id = device_config.get('last_device_id', None)
    except FileNotFoundError:
        pass

    if not args.device_model_id and not device_model_id:
        raise Exception('Missing --device-model-id option')

    # Re-register if "device_model_id" is given by the user and it differs
    # from what we previously registered with.
    should_register = (
        args.device_model_id and args.device_model_id != device_model_id)

    device_model_id = args.device_model_id or device_model_id

    with Assistant(credentials, device_model_id) as assistant:
        events = assistant.start()

        device_id = assistant.device_id
        print('device_model_id:', device_model_id)
        print('device_id:', device_id + '\n')

        # Re-register if "device_id" is different from the last "device_id":
        if should_register or (device_id != last_device_id):
            if args.project_id:
                register_device(args.project_id, credentials,
                                device_model_id, device_id)
                pathlib.Path(os.path.dirname(args.device_config)).mkdir(
                    exist_ok=True)
                with open(args.device_config, 'w') as f:
                    json.dump({
                        'last_device_id': device_id,
                        'model_id': device_model_id,
                    }, f)
            else:
                print(WARNING_NOT_REGISTERED)

        for event in events:
            process_event(event, assistant)


if __name__ == '__main__':
    main()
