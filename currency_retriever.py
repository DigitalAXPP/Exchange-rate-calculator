import json
import requests


class Error(Exception):
    """Class to bundle all custom exceptions."""
    pass


class CurrencyValueError(Error):
    """Class to warn the user about incorrect currency input."""
    def __str__(self):
        return "Please enter a three character string as currency."


class CurrencyConverter:

    """
    A class to convert a certain amount of one currency to either an
    amount of another entered currency or if no second currency was entered,
    all currencies are displayed.

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
    __init__ : amount, currency_in, currency_out = None
        amount = Integer input from which the output will be calculated
        currency_in = Three character string input. Required to establish from
                    which currency to convert
        [currency_out] = Optional input, three character string. If entered the
                    output is converted to this parameter. The default is None.

    convert : Returns the converted currency with the currency code

    Raises
    ------
    CurrencyValueError
        If the input to either currency is not a string.
    """

    def __init__(self, amount, currency_in, currency_out = None):
        try:
            self.amount = int(amount)
        except (ValueError, NameError):
            print("Please enter an integer as amount.")
            exit()

        try:
            if isinstance(currency_in, str):
                self.currency_in = currency_in
            else:
                if not isinstance(currency_in, str):
                    raise CurrencyValueError
        except CurrencyValueError:
            print("Please enter a three character string as currency.")
            exit()

        try:
            if currency_out is None:
                self.currency_out = currency_out
            elif isinstance(currency_out, str):
                self.currency_out = currency_out
            else:
                raise CurrencyValueError
        except CurrencyValueError:
            print("Please enter a three character string as currency.")
            exit()

    def convert(self):

        """
        This method takes the class input and converts it to the target currency or if the target
        currency is omitted the amount will be converted in all currencies.

        Variables
        ---------
        web : string
            This variable takes a string and updates part of it with the user input to request the correct
            currency.
        rweb : HTTP Response instance
            This variable takes the http instance from the website.
        jdweb : Encoded JSON
            This variable stores the rweb instance encoded in JSON.
        jlweb : Decoded JSON
            This variable loads the JSON content in jdweb and decodes it.

        Returns
        -------
        Digit, String
            The function returns the converted amount and the corresponding country code.
        """

        # Initiation blocks to load the currency exchange rates

        try:
            web = "http://www.floatrates.com/daily/{0}.json".format(self.currency_in)
            rweb = requests.get(web)
        except requests.exceptions.ConnectionError:
            return "Connection to website failed. " \
                   "Please verify your internet connection."

        try:
            jdweb = json.dumps(rweb.json(), indent=2)
            jlweb = json.loads(jdweb)
        except json.decoder.JSONDecodeError:
            print("Your currency input is probably incorrect.")

        # Currency conversion block. If no target currency was entered, the amount will be
        # multiplied with the exchange 'rate' for every available currency. Otherwise, if
        # a target currency is entered, the exchange rate will be calculated for the selected
        # currency. The output is rounded to two point after the comma with the 'alphacode'
        # printed besides it.

        try:
            if self.currency_out is None:
                for k,v in jlweb.items():
                    output = self.amount * v["rate"]
                    print(round(output, 2), v["alphaCode"])
            else:
                output = self.amount * jlweb[self.currency_out]["rate"]
                print(round(output,2), jlweb[self.currency_out]["alphaCode"])
        except KeyError:
            print("Your currency output is not available.")


if __name__ == '__main__':
    c = CurrencyConverter(amount=1000, currency_in="czk", currency_out="cad").convert()
