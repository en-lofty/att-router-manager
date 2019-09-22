from managers.broadcast_manager import BroadcastManager
from managers.channel_manager import ChannelManager
from managers.password_manager import PasswordManager
from managers.ssid_manager import SSIDManager


class MainManager:
    BASE_URL = "http://192.168.1.254"
    SETTINGS_URL = "http://192.168.1.254/xslt?PAGE=C_2_1"
    channel = ChannelManager
    broadcast = BroadcastManager
    ssid = SSIDManager
    password = PasswordManager
