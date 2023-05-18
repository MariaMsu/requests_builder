from requests_builder.builder import compile_request
from collections import Counter
from unittest import TestCase

DEBUG = False

requests = [
    "I am planning to order the BMW M8 with a sunroof or panorama glass roof sky lounge, and the M Sport Package on 12th April 2018. Is this configuration possible?",
    "Hello, is the X7 xDrive40i available without a panorama glass roof and with the EU Comfort Package. I need the vehicle on the 8th of November 2024.",
    "I want to order a BMW iX with right-hand drive configuration. I will be ordering it at the start of October 2022.",
    "Hello, I want to order a car.",
    "My son wants a car with a Panorama Glass Roof Sky Lounge!"
]

responses = [
    [
        {"modelTypeCodes": ["DZ01"],
         "booleanFormulas": ["+(S403A/S407A)+P337A"],
         "dates": ["2018-04-12"]}
    ],
    [
        {"modelTypeCodes": ["21EM"],
         "booleanFormulas": ["-S402A+P7LGA"],
         "dates": ["2024-11-08"]}
    ],
    [
        {"modelTypeCodes": ["21CF"],
         "booleanFormulas": ["+RL"],
         "dates": ["2022-10-01"]},
        {"modelTypeCodes": ["11CF"],
         "booleanFormulas": ["+RL"],
         "dates": ["2022-10-01"]}
    ],
    [
        {"modelTypeCodes": [None],
         "booleanFormulas": [None],
         "dates": [None]}
    ],
    [
        {"modelTypeCodes": [None],
         "booleanFormulas": ["+S407A"],
         "dates": [None]}
    ]
]


def are_formulas_equal(expected_f, actual_f):
    # dummy comparator of the booleanFormulas
    if expected_f == actual_f:
        return True
    expected_c = Counter(expected_f)
    actual_c = Counter(actual_f)
    if expected_c == actual_c:
        print(f"INFO: the actual formula '{actual_f}' seems to be equal to the expected formula '{expected_f}', "
              "but the order of the elements is different.")
        return True
    return False


def is_response_correct(actual, expected):
    # we can not just compare the lists because of booleanFormulas can be different
    # even if they describe the same
    if len(actual) != len(expected):
        return False
    for i in range(len(actual)):
        if (actual[i]['modelTypeCodes'][0] != expected[i]['modelTypeCodes'][0]) or \
                (actual[i]['dates'][0] != expected[i]['dates'][0]) or \
                not are_formulas_equal(
                    expected_f=expected[i]["booleanFormulas"][0], actual_f=actual[i]["booleanFormulas"][0]
                ):
            return False
    return True


class Test(TestCase):
    def test_request_builder(self):
        for i, (user_input, expected) in enumerate(zip(requests, responses)):
            actual = compile_request(user_message=user_input, debug=DEBUG)
            with self.subTest(i=i):
                self.assertTrue(is_response_correct(actual=actual, expected=expected),
                                msg=f"\nactual:   {actual}\nexpected: {expected}")
