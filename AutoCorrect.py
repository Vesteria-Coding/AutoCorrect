import os
import ollama
import argparse
import keyboard
import time as t
from google import genai
import pyautogui as autogui
from dotenv import load_dotenv

# Setup
parser = argparse.ArgumentParser(description="Simple Spell Checker Using Gemini")
parser.add_argument('--api_key', help='Input your Gemini API key')
parser.add_argument('--local_model', action='store_true', help='Runs a local model on your PC')
args = parser.parse_args()
api_key = args.api_key
local_model = args.local_model

# Handle local model
if local_model:
    try:
        print('Ready')
        while True:
            keyboard.wait('`')
            key_log = ''
            t.sleep(0.02)
            autogui.press('backspace')
            while True:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    key = event.name
                    if key == '`':
                        response = ollama.chat(
                            model="gemma:2b",
                            messages=[{
                                "role": "user",
                                "content": f"Do not add, remove, or change the meaning of any words. Only correct spelling and grammar errors in the following text: {key_log}"
                            }]
                        )
                        output = response["message"]["content"]
                        print(output)
                        key_log += '`'
                        for i in key_log:
                            autogui.press('backspace')
                        t.sleep(0.01)
                        autogui.typewrite(output, interval=0.04)
                        t.sleep(0.02)
                        break
                    elif len(key) == 1:
                        key_log += key
                        print(key)
                    elif key == 'backspace':
                        key_log = key_log[:-1]
                    elif key == 'space':
                        key_log += ' '
                        print(key)
                    elif key == 'decimal':
                        key_log += '.'
                        print(key)
    except KeyboardInterrupt:
        print('Exiting')
        quit(1)

# Handle Gemini API
if api_key:
    with open('.env', 'w') as f:
        f.write(f'API_KEY={api_key}')
    print('Saved API Key')

    load_dotenv()
    client = genai.Client(api_key=os.getenv("API_KEY"))

    try:
        print('Ready')
        while True:
            keyboard.wait('`')
            key_log = ''
            t.sleep(0.02)
            autogui.press('backspace')
            while True:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    key = event.name
                    if key == '`':
                        response = client.models.generate_content(
                            model="gemini-2.0-flash",
                            contents=f"Do not add, remove, or change the meaning of any words. Only correct spelling and grammar errors in the following text: {key_log}"
                        )
                        print(response.text)
                        key_log += '`'
                        for i in key_log:
                            autogui.press('backspace')
                        t.sleep(0.01)
                        autogui.typewrite(response.text, interval=0.04)
                        t.sleep(0.02)
                        break
                    elif len(key) == 1:
                        key_log += key
                        print(key)
                    elif key == 'backspace':
                        key_log = key_log[:-1]
                    elif key == 'space':
                        key_log += ' '
                        print(key)
                    elif key == 'decimal':
                        key_log += '.'
                        print(key)
    except KeyboardInterrupt:
        print('Exiting')
        quit(1)
