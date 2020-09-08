# Notes on how to make this work.

## Hardware

-   Raspberry Pi 3B
-   [UCTRONICS 3.5" touch screen](https://www.amazon.com/gp/product/B076M399XX/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) not that I'll be using the touch part, but it's cheap and plugs in nicely.

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

    1.  Move the `theater.service` to the systemd directory - in the version of the OS I used

            sudo mv theater.service /etc/systemd/system
    2.  reload the `systemd` daemon: 

            sudo systemctl daemon-reload
    3.  enable the service:

            sudo systemctl enable theater.service

Now that part's set - the Raspberry Pi will run the `theater.py` script on startup, which will call VLC on every movie in the `video` directory, and leave a break in between, forever.

## Next Steps

1.  Add a switch or button to not load the script in some mode. A debug toggle.
2.  Learn the GPIO pins in Raspberry Pi and how to manipulate them to do things like control a motor.
3.  Come up with a setup or stand for the screen that's separate from the Raspberry Pi. I think the motor will have to run from the RPi power pins, then I'll just plug the monitor and Pi in separately.
