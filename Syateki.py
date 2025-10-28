import os
import pygame
import random
import sys

# 初期化
pygame.init()
WIDTH, HEIGHT = 800, 600
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.display.set_caption("射的ゲーム - ベース版")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
title_font = pygame.font.SysFont("msgothic", 40)
message_font = pygame.font.SysFont("msgothic", 30)

# 画面表示に関するクラス
class ScreenManager:
    """
    ゲームのスタート画面と終了画面の描写を管理するクラス
    """
    def __init__(self,screen, WIDTH, HEIGHT, title_font, message_font):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.title_font = title_font
        self.message_font = message_font


    def start_screen(self):
        screen.fill((0,0,0)) # 黒色の画面

        title_txt = self.title_font.render("射的ゲーム",True,(255,255,255,))
        title_rect = title_txt.get_rect(center=(self.WIDTH//2,self.HEIGHT//2))
        screen.blit(title_txt,title_rect)
        
        message_text = self.message_font.render("-- スペースを押してスタート --",True,(255,255,255))
        message_rect = message_text.get_rect(center=(self.WIDTH//2,self.HEIGHT//2+40))
        screen.blit(message_text,message_rect)


    def finish_screen(self, score):
        screen.fill((0,0,0)) # 黒色の画面
        title_txt = self.title_font.render(f"最終スコア:{score}",True,(255,255,255))
        title_rect = title_txt.get_rect(center=(self.WIDTH//2,self.HEIGHT//2))
        screen.blit(title_txt,title_rect)

        message_text = self.message_font.render("-- Rキーでリトライ --", True, (150, 150, 150))
        message_rect = message_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 60))
        self.screen.blit(message_text, message_rect)

screen_manager = ScreenManager(screen, WIDTH, HEIGHT, title_font, message_font)

# 的の設定
target_radius = 30
target_x = random.randint(target_radius, WIDTH - target_radius)
target_y = random.randint(target_radius, HEIGHT - target_radius)

# スコア
score = 0

# ゲームの状態管理
game_state = "start" # ゲームの状況


# メインループ
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # スタート画面表示
        if game_state == "start":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = 0
                game_state = "playing" # クリックしたらゲームの状態を変更

        # クリックで命中判定
        if game_state == "playing" and event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            distance = ((mx - target_x) ** 2 + (my - target_y) ** 2) ** 0.5
            if distance <= target_radius:
                score += 1

                # デバック用
                if score == 10:
                    game_state = "finish"

                # 的をランダムに再配置
                target_x = random.randint(target_radius, WIDTH - target_radius)
                target_y = random.randint(target_radius, HEIGHT - target_radius) 

        if game_state == "finish":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                score = 0
                game_state = "playing"  # enter でリトライ 

    # ゲームの状態による画面表示の変化
    if game_state == "start":
        screen_manager.start_screen()  # スタート画面の表示
            
    elif game_state == "playing":
        screen.fill((200, 220, 255)) # 背景色（水色）
        
        # 的の描画
        pygame.draw.circle(screen, (255, 0, 0), (target_x, target_y), target_radius)
        pygame.draw.circle(screen, (255, 255, 255), (target_x, target_y), target_radius // 2)

        # スコア表示
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    elif game_state == "finish":
        screen_manager.finish_screen(score)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()