import json
import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--amount', type=float, default=[],
                        help='Insert parameter you want to have converted.')
    parser.add_argument('-ci', '--currency_in', type=str, default='eur',
                        help='Insert the currency of your amount.')
    parser.add_argument('-co', '--currency_out', type=str, default=None,
                        help='OPTIONAL. Insert the currency you want your amount to'
                             'be converted to.')
    args = parser.parse_args()
    sys.stdout.write(str(convert_amount(args)))

def convert_amount(args):

    """
    A function to convert a specified amount of one currency to either an
    amount of another currency or if no second currency was entered,
    the amount will be converted to all available currencies.

    Currencies
    ----------
    USD, EUR, GBP, JPY, AUD, CAD, CHF, DKK, AED, CZK, PLN

    Parameters
    -------
        amount = Integer input from which the output will be calculated.
        currency_in = Three character string input. Required to establish from
                    which currency to convert.
        [currency_out] = Optional input, three character string. If entered the
                    output is converted to this parameter. The default is None.
    """

    # Setting path to the 'Currency' folder and load the JSON file
    try:
        folder = os.path.join(os.curdir, '{0}.txt'.format(args.currency_in))
        with open(folder, 'r') as json_src:
            content = json.load(json_src)
    except FileNotFoundError:
        return "Please locate the 'Currency' folder in the same directory as the .py" \
               "file."

    # Calculating the exchanged value
    # If currency_out has been specified, the amount will be multiplied by the currency rate.
    # Otherwise, if currency_out is None, the amount will be multiplied by all currencies and
    # printed separately.

    # Create Output format

    frame = """
    {
        "input": {
            "amount": 100,
            "currency": "czk"
        },
        "output": {
            "eur": 150
        }
    }
    """

    data = json.loads(frame)
    output_dict = dict()

    try:
        data["input"]["amount"] = args.amount
        data["input"]["currency"] = args.currency_in
    except Exception as e:
        return e

    try:
        if args.currency_out is not None:
            output = round(args.amount * content[args.currency_out]["rate"], 2)
            data["output"] = {content[args.currency_out]["alphaCode"]: output}
            out = json.dumps(data, indent=2)
            return out
        else:
            for v in content.values():
                output = args.amount * v["rate"]
                output_dict[v["alphaCode"]] = output
                data["output"] = output_dict
        out = json.dumps(data, indent=2)
        return out
    except (ValueError, KeyError):
        return "Please enter a valid, three character string for your currency."
    except TypeError:
        return "Please enter a float as amount."

if __name__ == '__main__':
    main()
