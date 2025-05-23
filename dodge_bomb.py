import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """ 
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横，縦）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True  # 横，縦方向用の変数
    # 横方向判定
    if rct.left < 0 or WIDTH < rct.right:  # 画面外だったら
        yoko = False
    # 縦方向判定
    if rct.top < 0 or HEIGHT < rct.bottom: # 画面外だったら
        tate = False
    return yoko, tate

def game_over(screen: pg.Surface) -> None:
    """    
    ゲームオーバー時に、半透明の黒い画面上に「Game Over」と表示し、泣いているこうかとん画像を貼り付ける関数 
    """
    font = pg.font.Font(None, 80)
    text = font.render("GAME OVER", True, (255, 255, 255)) # Game Overの文字
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    cry_kk_img = pg.image.load("fig/8.png") # 泣いているこうかとん
    left_kk_rect = cry_kk_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2))
    right_kk_rect = cry_kk_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2))
   
    overlay = pg.Surface((WIDTH, HEIGHT)) # ブラックアウト画面
    overlay.set_alpha(128)  # 半透明
    overlay.fill((0, 0, 0)) # 黒色で塗りつぶす

    screen.blit(overlay, (0, 0))    # 画面をブラックアウト
    screen.blit(text, text_rect)    # Game Overの文字を描画
    screen.blit(cry_kk_img, left_kk_rect)   # 左側のこうかとん
    screen.blit(cry_kk_img, right_kk_rect)  # 右側のこうかとん

    pg.display.update()
    pg.time.wait(5000)  # 5秒間停止
    return

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """ 
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す
    """
    bb_imgs = []  # 爆弾Surfaceのリスト
    bb_accs = [a for a in range(1, 11)]  # 加速度リスト
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))  # 爆弾Surface
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 赤い円を描画
        bb_imgs.append(bb_img)  # リストに追加
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # こうかとん初期化
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # 爆弾初期化
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんRectと爆弾Rectが重なっていたら
        if kk_rct.colliderect(bb_rct): 
            game_over(pg.display.get_surface()) # ゲームオーバー
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 左右方向
                sum_mv[1] += mv[1]  # 上下方向

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 画面内に戻す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:  # 上下どちらかにはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()