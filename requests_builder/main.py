import argparse
import json

from requests_builder.builder import compile_request


def main():
    parser = argparse.ArgumentParser(
        prog='BMW requests builder',
        description='The utility parses unstructured user messages and convert them into the structured json requests')

    parser.add_argument('messages', type=str, nargs='+', help='One or more user messages')
    args = parser.parse_args()

    for message in args.messages:
        car_request = compile_request(user_message=message, debug=False)
        json_formatted_str = json.dumps(car_request, indent=2)
        print(json_formatted_str)


if __name__ == "__main__":
    main()
