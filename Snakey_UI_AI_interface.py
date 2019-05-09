#!/usr/bin/env python3

__author__ = "Yxzh"

import pygame
import sys
import AI_core_logic
import AI_core_ML
from pygame.locals import *
from pygame.color import THECOLORS
import pygame.font
from random import randint


PLAYGROUND_WIDTH = 20
PLAYGROUND_HEIGHT = 20  # 游戏区域大小
INFOAREA_WIDTH = 100
INFOAREA_HEIGHT = 200  # 信息区域大小
WINDOW_TITLE = "Snacky"  # 屏幕标题
allowed_event = [pygame.KEYDOWN, pygame.QUIT]  # 事件列表
pygame.init()  # 初始化pygame
pygame.display.set_caption(WINDOW_TITLE)  # 窗口标题
fps_clock = pygame.time.Clock()  # 创建FPS时钟对象
pygame.event.set_allowed(allowed_event)  # 设置事件过滤
s_screen = pygame.display.set_mode((PLAYGROUND_WIDTH * 10 + INFOAREA_WIDTH, PLAYGROUND_HEIGHT * 10), 0, 32)  # 屏幕Surface
# s_screen = pygame.display.set_mode((PLAYGROUND_WIDTH + INFOAREA_WIDTH, PLAYGROUND_HEIGHT),pygame.FULLSCREEN , 0, 32)  # 全屏屏幕Surface

s_infoarea = pygame.Surface((PLAYGROUND_WIDTH * 10, PLAYGROUND_HEIGHT * 10), 0, 32)  # 信息区域Surface
s_gray = pygame.Surface((35, 37), 0, 32)  # 信息区域灰色实时刷新块
s_gray.fill(THECOLORS["gray"])
r_fast_update = pygame.Rect((65, 80), (100, 117))  # 信息区域实时刷新范围

si_snake = pygame.image.load("images/snake.png").convert_alpha()  # 加载图片
si_food = pygame.image.load("images/Pineapple.png").convert_alpha()
si_deadsnake = pygame.image.load("images/dead_snake.png").convert_alpha()
si_gamestart = pygame.image.load("images/game_start.png").convert_alpha()
si_bomb = pygame.image.load("images/bm.png").convert_alpha()

pygame.font.init()  # 初始化字体

f_arial = pygame.font.SysFont("arial", 24)  # 加载字体
f_optima = pygame.font.SysFont("optima", 35)
f_small_arial = pygame.font.SysFont("arial", 12, 1)

sf_arial_gameover = f_arial.render("GAMEOVER!", 1, THECOLORS["black"])  # 渲染文字
sf_arial_scoreboad = f_arial.render("SCOREBOARD", 1, THECOLORS["black"])
sf_small_arial_restart = f_small_arial.render("Press 'R' to restart.", 1, THECOLORS["black"])
sf_small_arial_scoreboard = f_small_arial.render("Press 'S' to open Scoreboard.", 1, THECOLORS["black"])
sf_small_arial_gamestart = f_small_arial.render("SPACE to start and 'Q' to exit.", 1, THECOLORS["black"])
sf_small_arial_back = f_small_arial.render("Press 'R' to return.", 1, THECOLORS["black"])
sf_small_arial_score = f_small_arial.render("Score: ", 1, THECOLORS["red"])
sf_optima_caption = f_optima.render("SNACKY", 1, THECOLORS["orange"])
sf_small_arial_level = f_small_arial.render("level: ", 1, THECOLORS["black"])
sf_small_arial_current_fps = f_small_arial.render("fps: ", 1, THECOLORS["black"])
sf_small_arial_ate = f_small_arial.render("ate: ", 1, THECOLORS["black"])
sf_small_arial_position = f_small_arial.render("pos: ", 1, THECOLORS["black"])
sf_small_arial_botton = f_small_arial.render("btnreg: ", 1, THECOLORS["black"])
sf_small_arial_direction = f_small_arial.render("direction: ", 1, THECOLORS["black"])
sf_small_arial_dot = f_small_arial.render(".", 1, THECOLORS["black"])
Lsf_small_arial_direction = {
	"W": f_small_arial.render("W", 1, THECOLORS["black"]), "S": f_small_arial.render("S", 1, THECOLORS["black"]),
	"A": f_small_arial.render("A", 1, THECOLORS["black"]), "D": f_small_arial.render("D", 1, THECOLORS["black"]),
}
Lsf_small_arial_numbers_black = []
for i in range(0, 10):
	Lsf_small_arial_numbers_black.append(f_small_arial.render(str(i), 1, THECOLORS["black"]))

def main():
	fps = 60  # 帧率
	pos_x = 0  # 蛇头位置
	pos_y = 0
	old_direction = "S"  # 当前蛇头方向
	snakes = [(0, 0)] * 2  # 蛇数组
	isfood = False  # 食物判定
	bombs = []  # 炸弹数组
	food_pos_x = 0  # 食物坐标
	food_pos_y = 0
	diffculty_counter = 0  # 难度计数
	ate = 0  # 食物计数
	level = 10  # 难度
	c_frame = 0  # 空闲帧数计数器
	diffculty = [14, 12, 10, 8, 6, 5, 4, 3, 2, 1, 0]  # 难度表 越难空闲帧越少
	deadflag = False  # 死亡判定
	
	f_gamestart(s_screen, fps_clock)  # 开始游戏画面
	
	while True:  # 屏幕循环
		for event in pygame.event.get():  # 事件循环
			if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_q:  # 退出事件
				pygame.quit()
				sys.exit()
		
		if c_frame >= diffculty[level]:  # 根据难度判断空闲帧 最高难度无空闲帧
			
			direction = AI_core_logic.get_next_direction([pos_x, pos_y], [food_pos_x, food_pos_y], snakes)  # 获取下一步方向
			
			if direction == "W" and old_direction != "S":
				old_direction = "W"
			if direction == "S" and old_direction != "W":
				old_direction = "S"
			if direction == "A" and old_direction != "D":
				old_direction = "A"
			if direction == "D" and old_direction != "A":
				old_direction = "D"
			
			if old_direction == "W":  # 自动前进
				pos_y -= 1
			if old_direction == "S":
				pos_y += 1
			if old_direction == "A":
				pos_x -= 1
			if old_direction == "D":
				pos_x += 1
			
			if pos_x < 0:  # 碰到屏幕边缘循环
				pos_x = PLAYGROUND_WIDTH - 1
			if pos_x > PLAYGROUND_WIDTH - 1:
				pos_x = 0
			if pos_y < 0:
				pos_y = PLAYGROUND_HEIGHT - 1
			if pos_y > PLAYGROUND_HEIGHT - 1:
				pos_y = 0
			
			del (snakes[0])
			
			if (pos_x, pos_y) in snakes:  # 自身碰撞检测
				deadflag = True  # 触发死亡判定
			
			snakes.append((pos_x, pos_y))  # 推入蛇数组底
			
			if len(bombs) < level:  # 根据难度刷新炸弹
				bomb_pos_x = randint(0, PLAYGROUND_WIDTH - 1)
				bomb_pos_y = randint(0, PLAYGROUND_HEIGHT - 1)
				
				while ((bomb_pos_x, bomb_pos_y) in snakes) or (
								  food_pos_x == bomb_pos_x or food_pos_y == bomb_pos_y) or (
								  (bomb_pos_x, bomb_pos_y) in bombs):  # 避免与蛇和食物和其他炸弹重叠刷新
					bomb_pos_x = randint(0, PLAYGROUND_WIDTH - 1)
					bomb_pos_y = randint(0, PLAYGROUND_HEIGHT - 1)
				
				bombs.append((bomb_pos_x, bomb_pos_y))
			
			if not isfood:  # 根据食物判定刷新食物
				food_pos_x = randint(0, PLAYGROUND_WIDTH - 1)
				food_pos_y = randint(0, PLAYGROUND_HEIGHT - 1)
				
				while (food_pos_x, food_pos_y) in snakes or (food_pos_x, food_pos_y) in bombs:  # 避免重叠刷新
					food_pos_x = randint(0, PLAYGROUND_WIDTH - 1)
					food_pos_y = randint(0, PLAYGROUND_HEIGHT - 1)
				
				isfood = True
			
			# if (pos_x, pos_y) in bombs:  # 炸弹碰撞检测
			# 	deadflag = True
			
			if pos_x == food_pos_x and pos_y == food_pos_y:  # 吃食物事件
				snakes.append((pos_x, pos_y))  # 将当前位置推入蛇数组
				diffculty_counter += 1  # 调整难度计数
				ate += 1
				isfood = False
			
			if diffculty_counter > 4:  # 难度调整
				if level < len(diffculty) - 1:
					level += 1
					diffculty_counter = 0
			
			s_screen.fill(THECOLORS["white"])  # 填充白屏
			
			s_screen.blit(si_food, (food_pos_x * 10 - 4, food_pos_y * 10 - 5))  # 填充食物图片
			
			for i in bombs:  # 填充炸弹图片
				s_screen.blit(si_bomb, [x * 10 - 2 for x in i])
			
			for i in snakes:  # 填充蛇图片
				s_screen.blit(si_snake, [x * 10 for x in i])
			
			s_infoarea.fill(THECOLORS["gray"])  # 填充信息区域各种信息
			pygame.draw.line(s_infoarea, THECOLORS["black"], (0, 0), (0, INFOAREA_HEIGHT), 3)  # 分隔线
			s_infoarea.blit(sf_small_arial_level, (10, 5))  # 难度信息提示
			s_infoarea.blit(sf_small_arial_ate, (10, 20))  # 食物数量信息
			s_infoarea.blit(sf_small_arial_position, (10, 35))  # 位置信息
			s_infoarea.blit(sf_small_arial_direction, (10, 65))  # 方向信息
			s_infoarea.blit(sf_small_arial_botton, (10, 80))  # 按键寄存信息 （实时刷新）
			s_infoarea.blit(sf_small_arial_current_fps, (10, 95))  # FPS（实时刷新）
			
			if level < 9:  # 刷新信息
				s_infoarea.blit(Lsf_small_arial_numbers_black[level], (65, 5))
			else:
				s_infoarea.blit(sf_small_arial_dot, (65, 5))
			f_show_number(s_infoarea, ate, (65, 20))
			f_show_number(s_infoarea, pos_x, (65, 35))
			f_show_number(s_infoarea, pos_y, (65, 50))
			s_infoarea.blit(Lsf_small_arial_direction[direction], (65, 65))
			
			s_screen.blit(s_infoarea, (PLAYGROUND_WIDTH * 10, 0))  # 信息Surface填充至屏幕Surface
			pygame.display.flip()  # 将图像内存缓冲刷新至屏幕
			
			c_frame = 0  # 更新计数器
			
			if deadflag:  # 死亡判定
				f_gameover(s_screen, fps_clock, ate)  # 游戏结束画面
				return
		
		c_frame += 1  # 迭代计数器
		
		s_infoarea.blit(s_gray, (65, 80))  # 填充实时刷新块（灰色背景）
		s_infoarea.blit(Lsf_small_arial_direction[old_direction], (65, 80))  # 填充按键寄存
		
		current_fps = fps_clock.get_fps() * 10  # 获取实时FPS
		s_infoarea.blit(Lsf_small_arial_numbers_black[int(current_fps / 100)], (65, 95))  # 填充FPS
		s_infoarea.blit(Lsf_small_arial_numbers_black[int((current_fps % 100) / 10)], (72, 95))
		s_infoarea.blit(sf_small_arial_dot, (79, 95))
		s_infoarea.blit(Lsf_small_arial_numbers_black[int((current_fps % 100) % 10)], (86, 95))
		
		s_screen.blit(s_infoarea, (PLAYGROUND_WIDTH * 10, 0))  # 将实时填充后的信息Surface填充至屏幕Surface
		pygame.display.update(r_fast_update)  # 局部实时屏幕刷新
		fps_clock.tick(fps)  # FPS等待时钟

def f_show_number(surface, number, position):
	"""
	在目标Surface上填充数字
	:param surface: 目标Surface
	:param number: 数字
	:param position: 位置
	"""
	
	surface.blit(Lsf_small_arial_numbers_black[int(number / 100)], (position[0], position[1]))
	surface.blit(Lsf_small_arial_numbers_black[int((number % 100) / 10)], (position[0] + 7, position[1]))
	surface.blit(Lsf_small_arial_numbers_black[int((number % 100) % 10)], (position[0] + 14, position[1]))
	return

def f_gamestart(_s_screen, _fps_clock):
	"""
	游戏开始画面
	:param _s_screen: 屏幕Surface
	:param _fps_clock: FPS时钟对象
	"""
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_q):  # 退出事件
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == K_s:  # 进入计分板画面
				f_scoreboard(_s_screen, _fps_clock)
			if event.type == pygame.KEYDOWN and event.key == K_SPACE:  # 进入main()函数
				return
		
		_s_screen.fill(THECOLORS["white"])
		_s_screen.blit(sf_optima_caption, (81, 3))
		_s_screen.blit(si_gamestart, (93, 90))
		_s_screen.blit(sf_small_arial_gamestart, (62, 52))
		_s_screen.blit(sf_small_arial_scoreboard, (62, 70))
		pygame.display.flip()
		_fps_clock.tick(5)

def f_gameover(_s_screen, _fps_clock, ate):
	"""
	游戏结束画面
	:param _s_screen: 屏幕Surface
	:param _fps_clock: FPS时钟对象
	:param ate: 食物计数
	"""
	
	fi_score = open("score.s", "a+")  # 将分数写入分数文件 不存在就新建
	fi_score.write(str(ate) + "\n")
	fi_score.close()  # 关闭文件IO流
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_q:  # 退出事件
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == K_s:  # 进入计分板画面
				f_scoreboard(_s_screen, _fps_clock)
				return
			if event.type == pygame.KEYDOWN and event.key == K_r:  # 重新开始
				return
		
		_s_screen.fill(THECOLORS["white"])
		_s_screen.blit(sf_arial_gameover, (72, 4))
		_s_screen.blit(sf_small_arial_score, (100, 35))
		_s_screen.blit(sf_small_arial_restart, (92, 50))
		_s_screen.blit(sf_small_arial_scoreboard, (62, 65))
		_s_screen.blit(si_deadsnake, (80, 75))
		f_show_number(_s_screen, ate, (150, 35))  # 填充该局得分
		pygame.display.flip()
		_fps_clock.tick(5)

def f_scoreboard(_s_screen, _fps_clock):  # 计分板画面
	"""
	计分板画面
	:param _s_screen: 屏幕Surface
	:param _fps_clock: FPS时钟对象
	"""
	
	fi_score = open("score.s", "r")  # 读取分数文件
	scores = []
	for i in fi_score.readlines():  # 转换为int
		scores.append(int(i))
	fi_score.close()
	
	scores.sort(reverse = True)  # 倒序排列
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or event.type == KEYDOWN and event.key == K_q:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key == K_r:  # 重新开始
				return
		_s_screen.fill(THECOLORS["white"])
		_s_screen.blit(sf_arial_scoreboad, (65, 4))
		_s_screen.blit(sf_small_arial_back, (100, 40))
		for i in range(0, len(scores)):  # 填充排行榜
			_s_screen.blit(Lsf_small_arial_numbers_black[i + 1], (130, 60 + 15 * i))
			_s_screen.blit(sf_small_arial_dot, (137, 60 + 15 * i))
			f_show_number(_s_screen, scores[i], (150, 60 + 15 * i))
			if i > 7:
				break
		pygame.display.flip()
		_fps_clock.tick(5)

if __name__ == "__main__":  # 程序入口
	while True:
		main()
