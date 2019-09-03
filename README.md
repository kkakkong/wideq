WideQ
=====

A library for interacting with the "LG SmartThinq" system, which can control heat pumps and such. I reverse-engineered the API from their mobile app.

To try out the API, there is a simple command-line tool included here, called `example.py`.
To use it, provide it with a country and language code via the `-c` and `-l` flags, respectively:

    $ git clone https://github.com/gugu927/wideq.git
    $ cd wideq

    $ python3 example.py -c KR -l ko-KR

LG accounts seem to be associated with specific countries, so be sure to use the one with which you originally created your account.
For Korean, for example, you'd use `-c KR -l ko-KR`.

On first run, the script will ask you to log in with your LG account.
Logging in with Google does not seem to work, but other methods (plain email & password, Facebook, and Amazon) do. 

By default, the example just lists the devices associated with your account.
You can also specify one of several other commands:

* `ls`: List devices (the default).
* `mon <ID>`: Monitor a device continuously, printing out status information until you type control-C. Provide a device ID obtained from listing your devices.
* `washer-mon <ID>`: Like `mon`, but only for WASHER devices---prints out specific washer-related information in a more readable form.
* `dryer-mon <ID>`: Like `mon`, but only for DRYER devices---prints out specific dryer-related information in a more readable form.
* `dehum-mon <ID>`: Like `mon`, but only for DEHUMIDIFIER devices---prints out dehumidifier-related information in a more readable form.
* `ac-mon <ID>`: Like `mon`, but only for AC devices---prints out specific climate-related information in a more readable form.
* `set-temp <ID> <TEMP>`: Set the target temperature for an AC device.
* `turn <ID> <ONOFF>`: Turn an AC device on or off. Use "on" or "off" as the second argument.
* `ac-config <ID>`: Print out some configuration information about an AC device.

Credits
-------

This is by [GuGu927][andy].
The license is [MIT][].

I also made a [Home Assistant component][hass-smartthinq] which uses wideq.

For Korean user, visit [HomeAssistant Naver Cafe][cafe].

This library originated from [Adrian Sampson][sampson]

[cafe]: https://cafe.naver.com/koreassistant
[hass-smartthinq]: https://github.com/gugu927/hass-smartthinq
[andy]: https://github.com/gugu927
[mit]: https://opensource.org/licenses/MIT
[sampson]: https://github.com/sampsyo/wideq
