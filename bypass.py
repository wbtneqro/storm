import re
import time


class stormwall():

    # ------------------------------------------------------------------------------- #

    def __init__(self, session, response):
        self.session = session
        self._response = response

    # ------------------------------------------------------------------------------- #

    def is_sw_challenge(self) -> bool:
        return self._response.status_code == 200 and '<script src="https://static.stormwall.pro/js' in self._response.text

    # ------------------------------------------------------------------------------- #

    def handle_sw_challenge(self):
        try:
            # Extract JS variables
            payload = dict(
                re.findall(
                    r'const\s*(cE|cK|cN)\s*=\s*[" ]([\w\d!:?]+)[" ;]',
                    self._response.text,
                    re.S | re.M
                )
            )

        except Exception:
            raise RuntimeError('Failed to extract JS variables.')

        # Were working a preparedrequest, we cannot simply call prepare_cookie incase cookies are already present.
        # https://kite.com/python/docs/requests.PreparedRequest
        if 'Cookie' in self._response.request.headers:
            self._response.request.headers['Cookie'] = '{}; {}={}'.format(
                self._response.request.headers['Cookie'],
                payload['cN'],
                self.solve_sw_challenge(
                    int(payload['cK']),
                    payload['cE']
                )
            )
        else:
            self._response.request.headers['Cookie'] = '{}={}'.format(
                payload['cN'],
                self.solve_sw_challenge(
                    int(payload['cK']),
                    payload['cE']
                )
            )

        # The JS waits 1000ms if the googleAnal or yaMetrika variable is defined.
        time.sleep(1)

        # Repeat original request via preparedrequest.
        self._response.request.headers['Referer'] = self._response.url
        return self.session.send(self._response.request)


    # ------------------------------------------------------------------------------- #

    def solve_sw_challenge(self, key: int, obfuscatedValue: str) -> str:
        # Ported from: https://pastebin.com/ZGtHDbnd
        alphabet = '0123456789qwertyuiopasdfghjklzxcvbnm:?!'
        alphabet_map = {}

        for i in range(len(alphabet)):
            alphabet_map[alphabet[i]] = i

        # ------------------------------------------------------------------------------- #

        def get_value(k: int, s: str) -> str:
            limit = len(alphabet) - 1
            value = ''

            for i in range(len(s)):
                char = s[i]

                if char not in alphabet_map:
                    value += char
                else:
                    index = alphabet_map[char] + k

                    if index > limit:
                        index -= limit - 1
                    elif index < 0:
                        index += limit + 1

                    value += alphabet[index]
            return value

        # ------------------------------------------------------------------------------- #

        def get_cookie_value(ck: int, ce: str) -> str:
            limit = len(alphabet) - 1
            value = ''

            for i in range(len(ce)):
                char = ce[i]
                value += get_value(ck * -1, char)
                ck += 1

                if ck > limit:
                    ck = 0

            return value

        # ------------------------------------------------------------------------------- #

        return get_cookie_value(key, obfuscatedValue)

    # ------------------------------------------------------------------------------- #