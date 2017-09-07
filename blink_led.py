import led
from RPi import GPIO


def colors():
    while True:
        yield led.RED
        yield led.GREEN
        yield led.BLUE
        yield led.YELLOW


def main():
    with led.new_led() as a_led:
        seq = led.Sequence().blink(color_seq=colors(), on_time=.66, off_time=.33)
        seq.run(a_led)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
