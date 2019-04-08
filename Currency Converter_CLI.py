import json
import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--amount', type=int, default=100,
                        help='Insert parameter you want to have converted.')
    parser.add_argument('-ci', '--currency_in', type=str, default='czk',
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

    Attributes
    ----------
    amount : integer
        The amount which will be converted
    currency_in : string
        The currency from which the amount will be converted.
    currency_out : string
        The currency to which the amount will be converted.

    Currencies
    ----------
    USD, EUR, GBP, JPY, AUD, CAD, CHF, XAF, TJS, MGA, LRD, SSP, LSL, SCR
    DKK, AED, VND, EGP, SVC, TTD, GHS, MRU, TZS, KWD, PEN, JOD, IQD, CVE
    LAK, DOP, MNT, NZD, RON, BDT, PYG, MAD, XPF, AOA, YER, SAR, TRY, IDR
    KZT, BOB, BZD, KMF, ALL, KHR, ZAR, PHP, TMT, AFN, JMD, GIP, SZL, NPR
    THB, TWD, UAH, ETB, SRD, SYP, ERN, SOS, KRW, BHD, NGN, RSD, MKD, SBD
    ANG, MOP, WST, MUR, HUF, BYN, ARS, TND, BIF, ZMW, GTQ, BAM, DZD, PLN
    HRK, HKD, AMD, VES, BSD, GNF, GEL, OMR, BND, SGD, MXN, MDL, NIO, GYD
    RWF, SLL, MVR, COP, XOF, UZS, PAB, NAD, SDG, MZN, KES, INR, BBD, PGK
    IRR, GMD, XCD, HTG, TOP, UGX, CNY, MYR, BGN, PKR, LBP, LYD, AWG, MWK
    CUP, VUV, NOK, ISK, BRL, AZN, UYU, STN, DJF, MMK, QAR, BWP, RUB, ILS
    KGS, CRC, FJD, CDF, HNL, LKR, CLP, SEK

    Methods
    -------
        amount = Integer input from which the output will be calculated.
        currency_in = Three character string input. Required to establish from
                    which currency to convert.
        [currency_out] = Optional input, three character string. If entered the
                    output is converted to this parameter. The default is None.
    """

    # Input validation part
    try:
        amount = int(args.amount)
    except (ValueError, NameError):
        return "Please enter an integer as amount."

    try:
        if isinstance(args.currency_in, str):
            currency_in = args.currency_in
        else:
            if not isinstance(args.currency_in, str):
                raise ValueError
    except ValueError:
        return "Please enter a three character string as currency."

    try:
        if args.currency_out is None:
            currency_out = args.currency_out
        elif isinstance(args.currency_out, str):
            currency_out = args.currency_out
        else:
            raise KeyError
    except (ValueError, KeyError):
        return "Please enter a three character string as currency."

    # Setting path to the 'Currency' folder and load the JSON file
    try:
        folder = os.path.join(os.curdir, 'Currency', '{0}.txt'.format(currency_in))
        with open(folder, 'r') as json_src:
            content = json.load(json_src)
    except FileNotFoundError:
        return "Please locate the 'Currency' folder in the same directory as the .py" \
               "file."

    # Calculating the exchanged value
    # If currency_out has been specified, the amount will be multiplied by the currency rate.
    # Otherwise, if currency_out is None, the amount will be multiplied by all currencies and
    # printed separately.
    try:
        if currency_out is not None:
            output = amount * content[currency_out]["rate"]
            return "{0} {1}".format(round(output, 2), content[currency_out]["alphaCode"])
        else:
            for k, v in content.items():
                output = amount * v["rate"]
                print("{0} {1}".format(round(output, 2), v["alphaCode"]))
    except (ValueError, KeyError):
        return "Please enter a valid, three character string for your currency."

if __name__ == '__main__':
    main()
