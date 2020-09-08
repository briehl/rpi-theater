# Notes on how to make this work.

## Raspberry Pi setup.

I did the setup on Windows 10 with the official Raspberry Pi Imager v1.4. Installed Raspberry Pi OS Lite on the SD card.

Once installed and configured with `raspi-config` I set it up with the following:

1.  Installed `VLC` with the following commands:

        > sudo apt update
        > sudo apt install vlc

2.  Create a `video` directory under the `pi` user.

3.  Copy videos to that directory. It's easiest with `scp`

        scp some_video.mkv pi@rpi-ip-address:video/

4.  Copy `theater.py` and `theater.service` to the `pi` home directory

        scp theater.* pi@rpi-ip-address

5.  Connect to the RPi however, and now we set up `systemd`.
    1. Move the `theater.service` to the systemd directory - in the version of the OS I used

            sudo mv theater.service /etc/systemd/system
    2. reload the `systemd` daemon: 
            sudo systemctl daemon-reload
    3. enable the service:
            sudo systemctl enable theater.service

Now that part's set - the Raspberry Pi will run the `theater.py` script on startup, which will call VLC on every movie in the `video` directory, and leave a break in between, forever.

