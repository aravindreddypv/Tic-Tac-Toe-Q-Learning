import Player
import BestPlayer
import QPlayer
import QAfterStatePlayer

if __name__ == '__main__':

    Qp = QPlayer.QPlayer()
    Rp = Player.RandomPlayer()
    Sp = Player.SafePlayer()
    Bp = BestPlayer.BestPlayer()
    Hp = Player.HumanPlayer()
    QA = QAfterStatePlayer.QASP()
    Mp = Player.MyPlayer()
    # Qp.train(Bp)
    QA.train(Bp)
    # QA.trainAll(Rp,Sp,Mp)
