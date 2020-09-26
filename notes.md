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

## Notes on systemd
Debugging:

* run `journalctl -u theater.service` to show logs about the service
* run `systemctl status theater.service` to get high level status info

## Next Steps

1.  Add a switch or button to not load the script in some mode. A debug toggle.
2.  Learn the GPIO pins in Raspberry Pi and how to manipulate them to do things like control a motor.
3.  Come up with a setup or stand for the screen that's separate from the Raspberry Pi. I think the motor will have to run from the RPi power pins, then I'll just plug the monitor and Pi in separately.

## GPIO stuff
I think, due to how the pins work on the Pi and the screen, It won't work with the screen plugged directly into the Pi to make a sandwich shape. I mean, it's fine if we don't want to have the Pi control the motor to the curtains, but we do.

So.

Our options are.

1.  Plug in the screen.
    1.  Don't do the curtain thing at all, maybe animate some on the screen.
    2.  Be clever with attaching pins to the Pi with the screen attached, get 5V power from somewhere else.
    3.  Be really clever and possibly not fire safe and use the 5V rail on the Pi. It might overtax it, though. We'll see.
2.  Don't plug in the screen. Need a separate power source for the screen and a wee baby HDMI cable.
    1. Freely use all the Pi pins.
    2. One 5V -> motor, other (maybe) can power some lights? So now the lights go out, and the curtains are drawn, then the show begins. And the lights go back on at the end. Neat.
    3. Just the motor.

## Update 9/24/2020
Going with 2.2. right now. Got a setup with a separate power for the screen and got the stepper motor running with some GPIO pins. That's driven by motor.py - the StepperMotor class provides a function to drive a motor a certain number of steps in some direction with some delay between each step. Easy-peasy lemon squeezy.

Next = 2 parts.
1. Find an analog GPIO pin (I think? Maybe they're called something else? Or maybe they're all analog?) and wire the lights. I want them to fade in and out. Probably run a bunch of lights in serial. Also pretty easy-peasy.
2. Find a design or system for drawing and undrawing the curtain. I'm guessing with some clever pulley system, and maybe multiple strings on the same motor, I can make that work. But, well, TO THE INTERNET!
    1. Holy fucking perfect idea. Just minify this to baby curtain size, and we're good. https://myoddrawings.wordpress.com/2009/02/25/how-to-make-a-pvc-stage-curtain-and-pulley-display/