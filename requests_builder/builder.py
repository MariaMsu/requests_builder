import sys
import openai
import requests_builder.const_prompts as p
import re
import time
import datetime

openai.api_key = ""  # SET ME!!!!
SLEEP_TIME = 30
MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0


def extract_date(user_message, debug=False):
    # the current day in necessary for the request like "I want a car in a week"
    today = datetime.date.today().strftime("%Y-%m-%d")
    context = f"\nInfo: current day is {today}\n{p.p_date_extractor}."
    llm_response = openai.ChatCompletion.create(
        model=MODEL,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": user_message},
        ]
    )
    llm_result = llm_response.choices[0].message.content
    if debug:
        function_name = sys._getframe().f_code.co_name
        print(f"{function_name}():\t'{llm_result}'")
    #  ChatGPT usually prints "Assuming the current date is <current_date>, the requested date is ..."
    llm_reset_cleaned = llm_result.replace(f"current date is {today}", "...")
    date = re.findall(pattern=r'\d{4}\-\d{2}\-\d{2}', string=llm_reset_cleaned)
    return date


def extract_model(user_message, debug=False):
    llm_response = openai.ChatCompletion.create(
        model=MODEL,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": p.p_model_extractor},
            {"role": "user", "content": user_message},
        ]
    )
    llm_result = llm_response.choices[0].message.content
    if debug:
        function_name = sys._getframe().f_code.co_name
        print(f"{function_name}():\t'{llm_result}'")
    model = re.findall(pattern=r'(?<!\w)(21CF|11CF|21EM|21EN|DZ01|28FF)(?!\w)', string=llm_result)
    return model


def extract_addons(user_message, debug=False):
    OPERATORS = "()+-/"
    llm_response = openai.ChatCompletion.create(
        model=MODEL,
        temperature=TEMPERATURE,
        messages=[
            {"role": "system", "content": p.p_addons_extractor},
            {"role": "user", "content": user_message},
        ]
    )
    llm_result = llm_response.choices[0].message.content
    if debug:
        function_name = sys._getframe().f_code.co_name
        print(f"{function_name}():\t'{llm_result}'")
    addons = re.findall(pattern=r'(?:[()+-/ ]*(?:LL|RL|P337A|P33BA|P7LGA|S402A|S407A|S403A)[()+-/ ]*)+',
                        string=llm_result)
    addon_fixed = []
    # glue the pieces of the formula into one
    previous_ends_with_operator = True
    for a in addons:
        if not previous_ends_with_operator:
            addon_fixed.append('+')
        addon_fixed.append(a)
        previous_ends_with_operator = (a[-1] in OPERATORS)
    addon_fixed = "".join(addon_fixed)

    addon_fixed = addon_fixed.replace(" ", "")  # remove spaces
    for char in "()+-/":  # remove repetitive symbols
        addon_fixed = re.sub(pattern=fr'\{char}+', repl=char, string=addon_fixed)
    return addon_fixed


def extract_or_wait(function, user_message, debug):
    while True:
        try:
            response = function(user_message=user_message, debug=debug)
        except openai.error.RateLimitError as e:
            print(f"\tThe rate limit for the LLM is reached. Wait before calling {function.__name__} again...")
            time.sleep(SLEEP_TIME)
        else:
            break  # we got the response from the LLM
    return response


def compile_request(user_message, debug=False):
    dates = extract_or_wait(function=extract_date, user_message=user_message, debug=debug)
    if debug:
        print(f"date: {dates}")

    models = extract_or_wait(function=extract_model, user_message=user_message, debug=debug)
    if debug:
        print(f"model: {models}")

    addon = extract_or_wait(function=extract_addons, user_message=user_message, debug=debug)
    if debug:
        print(f"addons: {addon}")

    # if the LLM did not find a characteristics, we insert 'None' into the response to the corresponding place
    models = [None] if len(models) == 0 else models
    dates = [None] if len(dates) == 0 else dates
    # There can not be several addons, because a set of addons can be described with a single formula,
    # not with a list of options
    addon = None if len(addon) == 0 else addon

    requests = []
    for m in models:
        for d in dates:
            single_request = {
                "modelTypeCodes": [m],
                "booleanFormulas": [addon],
                "dates": [d]}
            requests.append(single_request)
    return requests


if __name__ == "__main__":
    DEBUG = True

    message = "I am planning to order the BMW M8 with a sunroof or panorama glass roof sky lounge, and the M Sport Package on 12th April 2018. Is this configuration possible?"
    print(extract_date(user_message=message, debug=DEBUG))
