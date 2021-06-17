# TwitchPlaysDreams Server

<h3> About </h3>

As of right now, this only works on Windows 10. I'll be looking into adding Mac OS support in the future.

Controller is emulated using [vgamepad](https://github.com/yannbouteiller/vgamepad)

<h3> Install </h3>

First, you'll need to install the [ViGEmBus Driver](https://github.com/ViGEm/ViGEmBus/releases/tag/setup-v1.17.333)

Note: Until this is packaged as a pypi package, and/or as an executible, installation is as follows:

    $ git clone https://github.com/soggychips/TwitchPlaysDreams
    $ cd TwitchPlaysDreams
    $ python -m venv venv
    $ .\venv\Scripts\activate
    $ pip install -r requirements.txt

<h3> Running the Server </h3>
    
Running the server is as easy as:
    
    $ python server.py

For runtime options, run server.py with the `-h` flag

<h3> Message format:</h3>

All messages need to be sent over UDP, in the following formats:

<b>Structure layout:</b>

    {
        'type': <str>,
        'name': <str>,
        'amount': (<float> | <array [float, float]>),
        'length': <float>
    }

where arrayed floats can be from -1.0 to 1.0, and single floats can be from 0.0 to 1.0

<h4> Taps </h4>

<b>Simple button press:</b>

    {
        'type': 'button',
        'name': 'x',
        'amount': 1.0,
        'length': 0.0

    }

or more simply

    {
        'type': 'button',
        'name': 'triangle'
    }

<b>Dpad press:</b>

    {
        'type': 'dpad',
        'name': 'left'
    }

<b>Trigger pull:</b>

    {
        'type': 'trigger',
        'name': 'r2',
    }

or a half trigger pull:

    {
        'type': 'trigger',
        'name': 'l2',
        'amount': 0.5
    }

<b>Stick</b>

    {
        'type': 'stick',
        'name': 'left',
        'amount': [0.3, -1.0]
    }

<h4> Holds </h4>

To hold, send a `length` value, in seconds.

<b>Button hold</b>

    {
        'type': 'button',
        'name': 'triangle',
        'length': 1.0
    }

<h4> Combinations </h4>

Combinations will apply each message at the same time, and hold it for the longest `length` amount given, or for 1 frame, if no `length` exists.

<b>Send an array:</b>

    [
        {
            'type': 'stick',
            'name': 'left',
            'amount': [0.3, -0.2]
        },
        {
            'type': 'button',
            'name': 'triangle'
        },
        ...
    ]

<b>Example: </b>Press the right trigger 1/4, pull left stick all the way left, and press X and Circle

    [
        {
            'type': 'trigger',
            'name': 'r2',
            'amount': 0.25
        },
        {
            'type': 'stick',
            'name': 'left',
            'amount': [-1.0, 0.0],
        },
        {
            'type': 'button',
            'name': 'x'
        },
        {
            'type': 'button',
            'name': 'circle'
        }
    ]

<b>Example: </b>Hold the left trigger 3/4 of the way, and circle, for a second

    [
        {
            'type': 'trigger',
            'name': 'l2',
            'amount': 0.75
        },
        {
            'type': 'button',
            'name': 'circle',
            'length': 1.0
        }
    ]
