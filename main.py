import pygame
import sys
import random

# 画面サイズの定義
WIDTH, HEIGHT = 640, 480

# 色の定義（RGB形式）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (200, 200, 200)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

# ─────────────────────────
# キャラクターのクラス
# ─────────────────────────
class Character:
    def __init__(self, name, hp, attack_range):
        """
        コンストラクタ
        :param name: キャラクターの名前（文字列）
        :param hp: 初期のHP（整数）
        :param attack_range: 攻撃力の範囲（タプルで下限と上限を指定）
        """
        self.name = name
        self.hp = hp
        self.max_hp = hp  # 最大HPは初期HPと同じ
        self.attack_range = attack_range

    def attack(self, target):
        """
        攻撃を行うメソッド
        :param target: 攻撃対象のCharacterオブジェクト
        :return: 実際に与えたダメージ（整数）
        """
        damage = random.randint(*self.attack_range)  # attack_range内でランダムなダメージを算出
        target.take_damage(damage)  # 対象にダメージを与える
        return damage

    def take_damage(self, damage):
        """
        攻撃を受けた際のHP減少処理
        :param damage: 与えられるダメージ量（整数）
        """
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0  # HPがマイナスにならないように調整

    def is_defeated(self):
        """
        キャラクターが倒れているか確認する
        :return: Trueなら倒れている（HP <= 0）
        """
        return self.hp <= 0

# ─────────────────────────
# シンプルなボタンクラス
# ─────────────────────────
class Button:
    def __init__(self, rect, text, font, inactive_color=GRAY, text_color=BLACK):
        """
        ボタンの初期設定
        :param rect: ボタンの位置とサイズ (x, y, width, height)
        :param text: ボタンに表示するテキスト
        :param font: 使用するフォント（pygame.font.Fontオブジェクト）
        :param inactive_color: ボタンの背景色（非アクティブ時）
        :param text_color: テキストの色
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.inactive_color = inactive_color
        self.text_color = text_color

    def draw(self, screen):
        """
        ボタンを画面に描画する
        :param screen: 描画先のpygameのSurfaceオブジェクト
        """
        pygame.draw.rect(screen, self.inactive_color, self.rect)  # ボタンの四角形を描画
        text_surface = self.font.render(self.text, True, self.text_color)  # テキストのレンダリング
        text_rect = text_surface.get_rect(center=self.rect.center)  # テキストの位置をボタンの中心に合わせる
        screen.blit(text_surface, text_rect)  # 画面にテキストを描画

    def is_clicked(self, pos):
        """
        クリック判定
        :param pos: クリック位置の座標 (x, y)
        :return: クリック位置がボタン内ならTrue
        """
        return self.rect.collidepoint(pos)

# ─────────────────────────
# ゲーム本体のクラス
# ─────────────────────────
class BattleGame:
    def __init__(self, hero, enemy):
        """
        ゲームの初期化処理
        :param hero: 主人公のCharacterオブジェクト
        :param enemy: 敵キャラクターのCharacterオブジェクト
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # ゲームウィンドウの作成
        pygame.display.set_caption("Battle: Hero vs Enemy")  # ウィンドウタイトル
        self.clock = pygame.time.Clock()  # フレームレート管理用
        self.font = pygame.font.SysFont(None, 32)  # 使用するフォントの設定（サイズ32）
        self.hero = hero  # 主人公の設定
        self.enemy = enemy  # 敵キャラクターの設定
        self.turn = "hero"  # 現在のターン（"hero"：勇者のターン、"enemy"：敵のターン）
        self.battle_log = "Battle Start!"  # バトルの経過を記録するログ
        # 攻撃ボタンの生成（画面下部中央に配置）
        self.attack_button = Button((WIDTH // 2 - 60, HEIGHT - 80, 120, 50), "Attack", self.font)

    def is_game_over(self):
        """
        ゲームの終了条件をチェック
        :return: 勇者または敵が倒れていればTrue
        """
        return self.hero.is_defeated() or self.enemy.is_defeated()

    def enemy_turn(self):
        """
        敵のターンの処理
        敵が勇者を攻撃する処理を行い、ターンを勇者に戻す
        """
        # 敵のターンの前に少し待つ（見た目のため）
        pygame.time.wait(500)
        damage = self.enemy.attack(self.hero)  # 敵の攻撃
        # 攻撃結果をログに記録
        self.battle_log = f"{self.enemy.name} attacks! {self.hero.name} takes {damage} damage."
        self.turn = "hero"  # ターンを勇者に戻す
        # 勇者が倒れた場合、ログを更新
        if self.hero.is_defeated():
            self.battle_log = f"{self.hero.name} is defeated! {self.enemy.name} wins!"

    def handle_event(self, event):
        """
        各種イベント（キーボード、マウス、ウィンドウ閉じるなど）の処理
        :param event: pygameのイベントオブジェクト
        """
        if event.type == pygame.QUIT:
            # ウィンドウが閉じられたら終了
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 左クリック時の処理
            if self.turn == "hero":  # 勇者のターンの場合のみ攻撃できる
                if self.attack_button.is_clicked(event.pos):  # 攻撃ボタンがクリックされたか判定
                    damage = self.hero.attack(self.enemy)  # 勇者の攻撃
                    self.battle_log = f"{self.hero.name} attacks! {self.enemy.name} takes {damage} damage."
                    # 敵が倒れたかチェック
                    if self.enemy.is_defeated():
                        self.battle_log = f"{self.enemy.name} is defeated! {self.hero.name} wins!"
                    else:
                        self.turn = "enemy"  # 敵のターンへ変更

    def draw(self):
        """
        画面を描画する処理
        キャラクターの状態、バトルログ、攻撃ボタンなどを描画する
        """
        self.screen.fill(WHITE)  # 画面を白でクリア

        # 主人公の状態（名前、現在HP、最大HP）の描画
        hero_status = self.font.render(f"{self.hero.name} HP: {self.hero.hp}/{self.hero.max_hp}", True, BLACK)
        self.screen.blit(hero_status, (20, 20))

        # 敵キャラクターの状態の描画（画面右側に配置）
        enemy_status = self.font.render(f"{self.enemy.name} HP: {self.enemy.hp}/{self.enemy.max_hp}", True, BLACK)
        enemy_status_x = WIDTH - enemy_status.get_width() - 20  # 敵ステータスを右寄せにするための計算
        self.screen.blit(enemy_status, (enemy_status_x, 20))

        # バトル経過のログを画面中央あたりに表示
        log_surface = self.font.render(self.battle_log, True, BLACK)
        self.screen.blit(log_surface, (20, HEIGHT // 2))

        # 勇者のターンで、かつゲームが終了していなければ攻撃ボタンを描画
        if self.turn == "hero" and not self.is_game_over():
            self.attack_button.draw(self.screen)

        pygame.display.flip()  # 描画内容を画面に反映

    def run(self):
        """
        ゲームループ
        イベント処理、描画、フレームレート調整などを行う
        """
        while True:
            # 発生したすべてのイベントを処理する
            for event in pygame.event.get():
                self.handle_event(event)

            # 敵のターンの場合、enemy_turn() を呼び出す
            if self.turn == "enemy" and not self.is_game_over():
                self.enemy_turn()

            self.draw()  # 画面を再描画
            self.clock.tick(30)  # 1秒間に30フレームを目安にループを回す

# ─────────────────────────
# プログラムのエントリーポイント
# ─────────────────────────
if __name__ == "__main__":
    # キャラクター（勇者と敵）のインスタンス作成
    # ここで各パラメーターを変更すれば、簡単に別のキャラクターを作れる
    hero = Character("Hero", 100, (15, 25))     # 勇者はHP100、攻撃力15～25
    enemy = Character("Enemy", 100, (10, 20))     # 敵はHP100、攻撃力10～20

    # BattleGame クラスのインスタンスを作成し、ゲームを開始する
    game = BattleGame(hero, enemy)
    game.run()
