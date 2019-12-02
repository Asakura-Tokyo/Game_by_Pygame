""" cave   """
"""
変更点
・穴の外側を茶色に変更(洞窟っぽくした)
・エンターキーでゲーム開始（突然始まらないようにした）
・ゲームオーバーしてもエンターキーでリスタート
・判定を甘くした
・escキーで終了（いちいちターミナルでcontrol+cを押すのが面倒）
・障害物を設置（画面上に障害物がないときは1/10、あるときは1/50の確率で場所はランダムに生成）
（連続する障害物のx軸の距離は最低でも30pxは離すようにした。）

変更したいこと
・洞窟の傾きを滑らかに
・飛行船から銃弾発射して障害物を破壊
・クリア条件、狭くなったら終了
・スコアに応じて幅や障害物の数をいじると面白いかも
・説明文を表示
・ゲームオーバーという表示
"""
import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE,K_RETURN, K_ESCAPE

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    """ メインルーチン """
    walls = 80
    ship_y = 250
    velocity = 0
    score = 0
    slope = randint(1, 6)
    sysfont = pygame.font.SysFont(None, 40)
    ship_image = pygame.image.load("ship.png")
    bang_image = pygame.image.load("bang.png")
    rock_image = pygame.image.load("rock.png")
    holes = []
    for xpos in range(walls):
        holes.append(Rect(xpos * 10, 100, 10, 400))
    game_over = False
    game_start = False
    # rock_pos_x=800
    # rock_pos_y=300
    rocks = []#障害物リスト

    while True:
        is_space_down = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_RETURN:
                    game_start = True
                if event.key == K_SPACE:
                    is_space_down = True

        if not game_start :
            start_phrase = sysfont.render("Press Enter key to Start",True, (255, 255, 225))
            quit_phrase = sysfont.render("Press Esc key to Quit",True, (255, 255, 225))
            SURFACE.blit(start_phrase, (400, 300))
            SURFACE.blit(quit_phrase, (400, 350))
        else:
            # 自機を移動
            if not game_over:
                score += 10
                velocity += -3 if is_space_down else 3
                ship_y += velocity

                # 洞窟をスクロール
                edge = holes[-1].copy()
                test = edge.move(0, slope)
                if test.top <= 0 or test.bottom >= 600:
                    slope = randint(1, 6) * (-1 if slope > 0 else 1)
                    edge.inflate_ip(0, -20)
                edge.move_ip(10, slope)
                holes.append(edge)
                del holes[0]
                holes = [x.move(-10, 0) for x in holes]

                #障害物の作成と消去
                if len(rocks) == 0:
                    #画面上で1個目の障害物を作成
                    if randint(1,10) == 1:#1/10の確率で障害物を作成
                        rocks.append([800,randint(holes[-1].top,holes[-1].bottom-50)])
                else:
                    #画面上で２個目以降の障害物を作成
                    if (800 - rocks[-1][0]) > 30:#前の障害物との距離は最小で30
                        if randint(1,50) == 1:#1/50の確率で障害物を作成
                            rocks.append([800,randint(holes[-1].top,holes[-1].bottom-50)])
                    #障害物を消去
                        if rocks[0][0] < 0:
                            del rocks[0]

                #障害物をスクロール
                for rock in rocks:
                    rock[0]-= 10

                #洞窟の壁との衝突
                if holes[0].top > ship_y or \
                    holes[0].bottom < ship_y + 55:
                    game_over = True
                #障害物との衝突
                if len(rocks) != 0:
                    if (rocks[0][0]==60) and (rocks[0][1] - 40) < ship_y < (rocks[0][1] + 60):
                        game_over = True

            # 描画
            SURFACE.fill((101, 50, 0))
            for hole in holes:
                pygame.draw.rect(SURFACE, (0, 0, 0), hole)
            SURFACE.blit(ship_image, (0, ship_y))
            score_image = sysfont.render("score is {}".format(score),True, (0, 0, 225))
            SURFACE.blit(score_image, (600, 20))
            if len(rocks) != 0:
                for rock in rocks:
                    SURFACE.blit(rock_image, (rock[0], rock[1]))

            if game_over:
                SURFACE.blit(bang_image, (0, ship_y-40))
                main()


        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()
