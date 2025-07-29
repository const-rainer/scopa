from scopalocalplayer import ScopaLocalPlayer
from scopanetworkplayer import ScopaNetworkPlayer
from scopaloc import ScopaLoc
from scopaserv import ScopaServ

class ScopaEngine:
    def __init__(self, host=None, port=None):
        if host is None or port is None:
            players = [ScopaLocalPlayer(1), ScopaLocalPlayer(2)]
            self.__server = ScopaLoc(players)
        else:
            self.__server = ScopaServ(host, port)

    def start(self):
        self.__server.play_game()
        

if __name__ == "__main__":
    #eng = ScopaEngine(host="0.0.0.0", port=12345)
    eng = ScopaEngine()
    eng.start()