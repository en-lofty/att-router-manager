#!/home/raphael/.local/share/virtualenvs/python-O_96yZmr/bin/python
import logging
import os
import sys

import click
from logzero import logfile, logger, loglevel
from my_utils import MeasureBlockTime

from driver_singleton import DriverSingleton

logfile(os.path.join(sys.path[0], "./logs/core.log"))


def main():
    DriverSingleton(False)
    from managers.main_manager import MainManager as manager
    print(manager.password.get_password(True))
    manager.broadcast.set_broadcast(True, True)

    # print(manager.ssid.set_ssid("Test", True))
    input()
    # print(manager.channels.get_channel())
    DriverSingleton.close()


@click.command()
@click.option('--channel', '-c', type=str)
@click.option('--ssid', '-s', type=str, help="Change the SSID")
@click.option('--password', '-p', type=str, help="Change the password")
@click.option('--broadcast', '-b', type=bool, help="Change the broadcast status")
@click.option('--get-channel', is_flag=True)
@click.option('--get-password', is_flag=True)
@click.option('--get-broadcast', is_flag=True)
@click.option('--get-ssid', is_flag=True)
@click.option('--five_ghz', is_flag=True,
              help="Whether to change the 2.4ghz or the 5ghz settings. Default: 2.4ghz", default=False)
@click.option('--headless', '-h', is_flag=True, default=True)
@click.option('--verbose', '-v', is_flag=True)
def core(channel: str, ssid: str, password: str, broadcast: bool, get_channel: bool, get_password: bool,
         get_broadcast: bool, get_ssid: bool, five_ghz: bool, headless: bool, verbose: bool):
    DriverSingleton(headless)
    from managers.main_manager import MainManager as manager
    if not verbose:
        loglevel(logging.ERROR)
    if get_channel:
        click.echo(manager.channel.get_channel(not five_ghz))
    if get_password:
        click.echo(manager.password.get_password(not five_ghz))
    if get_broadcast:
        click.echo(manager.broadcast.is_broadcasting(not five_ghz))
    if get_ssid:
        click.echo(manager.ssid.get_ssid(not five_ghz))
    if channel:
        manager.channel.set_channel(channel)
    if ssid:
        manager.ssid.set_ssid(ssid, not five_ghz)
    if password:
        manager.password.set_password(password, not five_ghz)
    if broadcast:
        manager.broadcast.set_broadcast(broadcast, not five_ghz)


if __name__ == '__main__':
    with MeasureBlockTime("Main block"):
        if len(sys.argv) > 1:
            try:
                core()
            except Exception as e:
                logger.error(e)
                logger.exception(e)
            finally:
                DriverSingleton.close()
        else:
            main()
