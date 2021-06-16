# TwitchPlaysDreams Server

<h3> About </h3>
    As of right now, this only works on Windows 10. I'll be looking into adding Mac OS support in the future.
    
<h3> Install </h3>

First, you'll need to install the [ViGEmBus Driver](https://github.com/ViGEm/ViGEmBus/releases/tag/setup-v1.17.333)

Until this is packaged as a pypi package, and/or as an executible, installation is as follows:

    $ git clone https://github.com/soggychips/TwitchPlaysDreams
    $ cd TwitchPlaysDreams
    $ python -m venv venv
    $ .\venv\Scripts\activate
    $ pip install -r requirements.txt

<h3> Running the Server </h3>
    
Running the server is as easy as:
    
    $ python server.py

For runtime options, run server.py with the `-h` flag
