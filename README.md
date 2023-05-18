# BMW requests builder

This utility can take unstructured prompts written by the user 
and convert them into a request body like the one shown below:

**User Prompt**: 
"I am planning to order the BMW M8 with a sunroof or panorama glass roof sky lounge, and the M Sport Package on 12th April 2018. Is this configuration possible?"

**Request Body**:
```json
[
  {
    "modelTypeCodes": ["DZ01"],
    "booleanFormulas": ["+(S403A/S407A)+P337A"],
    "dates": ["2018-04-12"]
  }
]
```
The utility works in the following way:  
1) Read messages from the console  
2) Call ChatGPT with 3 different setups in order to extract the date, car model and additional configuration.
3) Parse ChatGPT output with regex in order to extract the necessary substrings for the request body.
4) Assemble a request body from the extracted information.


## How to build

Run the following commands from the project root.

```bash
sudo apt-get install python3.11-dev python3.11-venv
python3.11 -m venv venv
source venv/bin/activate
pip install -e .
```

## How to run, example

Set the openAI API key to [builder.py](requests_builder%2Fbuilder.py) before running!  

The free version of ChatGPT allows only 3 requests per minute.
Therefore, the utility can only process one message per minute.

```bash
build-requests \
  "My son wants a car with a Panorama Glass Roof Sky Lounge in a month" \
  "Hello, is the X7 available without a panorama glass roof and with the EU Comfort Package. I need the vehicle on the 8th of November 2024."
```
This example shows that among other things, the utility can operate with the **relative dates** ("in a month") and 
with the **vaguely worded statement** ("model X7" -> "21EM, 21EN").

The utility a set of string as an argument.
Run the following command to receive a help message

```bash
build-requests -h
```

## How to test

The free version of ChatGPT allows only 3 requests per minute.
Therefore, the test takes about 5 minutes.

```bash
cd tests
python -m unittest discover
```

## Bonus requirements

1. Write tests to ensure the application works as expected.  
   ✅ The instruction on how to run the tests is given above.


2. Add error handling and validation to ensure the prompts entered by the user are valid.  
   ✅ If the utility argument can not be converted to a list of string,
   the program ends, printing a message with instructions on how to call it correctly.


3. Allow the user to modify the request body before sending the request.  
   ✅ The user can modify the request in the console.


4. Allow the user to enter multiple prompts and generate a request body for each one.  
   ✅ The can pass a list of prompts to the utility.
