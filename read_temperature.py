#!/usr/bin/env python
import temperature_probe


def main():
    probe = temperature_probe.Probe()
    print float(probe.temperature) / 1000.0


if __name__ == '__main__':
    main()
