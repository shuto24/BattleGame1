import pygame
import sys
import random

pygame.init()

# 画面設定
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("勇者 vs 敵")

# フォント
font = pygame.font.SysFont(None, 36)

# 色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (180, 180, 180)

# 勇者と敵の情報
hero = {"hp": 100, "attack": (15, 25)}
enemy = {"hp": 100, "attack": (10, 20)}

# ターン制
player_turn = True
battle_log = "バトル開始！"

# ボタン設定
button_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT - 100, 120, 50)

clock = pygame.time.Clock()

# 描画関数
def draw():
    screen.fill(WHITE)
    
    # HP表示
    hero_text = font.render(f"勇者 HP: {hero['hp']}", True, BLACK)
    enemy_text = font.render(f"敵 HP: {enemy['hp']}", True, BLACK)
    screen.blit(hero_text, (50, 50))
    screen.blit(enemy_text, (350, 50))

    # バトルログ
    log_text = font.render(battle_log, True, BLACK)
    screen.blit(log_text, (50, 150))

    # ボタン
    pygame.draw.rect(screen, GRAY, button_rect)
    btn_text = font.render("攻撃", True, BLACK)
    screen.blit(btn_text, (button_rect.x + 25, button_rect.y + 10))

    pygame.display.flip()

# ゲームループ
running = True
while running:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player_turn and button_rect.collidepoint(event.pos):
                damage = random.randint(*hero["attack"])
                enemy["hp"] -= damage
                battle_log = f"勇者の攻撃！ 敵に{damage}ダメージ！"
                player_turn = False

                # 勝敗チェック
                if enemy["hp"] <= 0:
                    battle_log = "勇者の勝利！"
                    running = False

            elif not player_turn:
                pygame.time.wait(500)
                damage = random.randint(*enemy["attack"])
                hero["hp"] -= damage
                battle_log = f"敵の攻撃！ 勇者に{damage}ダメージ！"
                player_turn = True

                if hero["hp"] <= 0:
                    battle_log = "敵の勝利…"
                    running = False

    clock.tick(30)

# 終了処理
pygame.time.wait(2000)
pygame.quit()
sys.exit()
