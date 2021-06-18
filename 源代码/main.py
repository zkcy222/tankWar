# coding=utf-8
import sys
import pygame
import random
import globals
import gamerClass
import bulletClass
import homeClass
import npcClass
import wallClass
import boomClass

mapSize = mapWidth, mapHeight = 520, 520  # 初始化窗口
def main():
    # 初始化
    pygame.init()
    screen = pygame.display.set_mode(mapSize)
    done = False
    clock = pygame.time.Clock()
    ifmove = 0 # 检测方向键是否按下
    time = 0  # 游戏运行时间 单位不确定 只是数值
    fireTimer = 0  # 发射冷却倒计时
    score = 0  # 分数

    # 加载背景图片
    background = pygame.image.load("pic/ground.png")
    backgroundrect = background.get_rect()

    # 创建玩家
    gamer = gamerClass.Gamer(mapSize)

    # 创建精灵组 
    enemyGroup = pygame.sprite.Group()  # 敌人
    gamerGroup = pygame.sprite.Group(gamer)  # 玩家
    wallGroup = pygame.sprite.Group()  # 墙
    whiteWallGroup = pygame.sprite.Group()  # 白色墙
    redWallGroup = pygame.sprite.Group()  # 红色墙
    bulletGroup = pygame.sprite.Group()  # 子弹
    tankGroup = pygame.sprite.Group(gamer)  # 坦克组
    itemGroup = pygame.sprite.Group(gamer)  # 可碰撞物体组
    homeGroup = pygame.sprite.Group()  # 大本营组
    boomGroup = pygame.sprite.Group() #爆炸图画

    # 生成大本营
    home = homeClass.Home(240, 480)
    homeGroup.add(home)
    itemGroup.add(home)

    # 生成敌人
    enemyPositionList = [[0, 0], [320, 160], [400, 40]]
    for i in range(3):
        enemy = npcClass.Npc(mapSize, enemyPositionList[i][0], enemyPositionList[i][1])
        enemyGroup.add(enemy)
        tankGroup.add(enemy)
        itemGroup.add(enemy)

    # 生成墙
    whiteWallList = [[0, 260], [20, 260], [480, 260], [500, 260], [240, 100], [260, 100], [240, 120], [260, 120]]
    for i in range(8):
        newWhiteWall = wallClass.WhiteWall(whiteWallList[i][0], whiteWallList[i][1])
        wallGroup.add(newWhiteWall)
        whiteWallGroup.add(newWhiteWall)
        itemGroup.add(newWhiteWall)
    redWallList = [[40, 40, 200], [120, 40, 200], [200, 40, 180],
                   [280, 40, 180], [360, 40, 200], [440, 40, 200],
                   [0, 240, 260], [480, 240, 260], [80, 240, 280],
                   [120, 240, 280],  [360, 240, 280], [400, 240, 280],
                   [200, 200, 240],   [280, 200, 240],  [40, 320, 480],
                   [120, 320, 480],  [200, 280, 420],  [240, 300, 340],
                   [280, 280, 420],  [360, 320, 480],  [440, 320, 480]]
    for i1 in range(21):
        for i2 in range(redWallList[i1][1], redWallList[i1][2], 20):
            newRedWall1 = wallClass.RedWall(redWallList[i1][0], i2)
            newRedWall2 = wallClass.RedWall(redWallList[i1][0] + 20, i2)
            wallGroup.add(newRedWall1)
            wallGroup.add(newRedWall2)
            redWallGroup.add(newRedWall1)
            redWallGroup.add(newRedWall2)
            itemGroup.add(newRedWall1)
            itemGroup.add(newRedWall2)
    redWallList2 = [[220, 460], [240, 460], [260, 460], [280, 460], [220, 480], [220, 500], [280, 480], [280, 500]]
    for i in range(8):
        newRedWall = wallClass.RedWall(redWallList2[i][0], redWallList2[i][1])
        wallGroup.add(newRedWall)
        redWallGroup.add(newRedWall)
        itemGroup.add(newRedWall)
    # 游戏死循环
    while not done:
        clock.tick(24)
        pygame.display.flip()
        enemyGroup.update()
        gamerGroup.update()
        bulletGroup.update()
        boomGroup.update()
        time += 1
        fireTimer -= 1
        # 玩家键盘操作事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    gamer.setInfo(globals.speed, 0)
                    ifmove += 1
                elif event.key == pygame.K_LEFT:
                    gamer.setInfo(globals.speed, 1)
                    ifmove += 1
                elif event.key == pygame.K_DOWN:
                    gamer.setInfo(globals.speed, 2)
                    ifmove += 1
                elif event.key == pygame.K_RIGHT:
                    gamer.setInfo(globals.speed, 3)
                    ifmove += 1
                elif (event.key == pygame.K_SPACE) and (fireTimer < 0):
                    fireTimer = globals.fireCold
                    gamer.setSpeed(0)
                    newbullet = bulletClass.Bullet(mapSize, gamer.getDir(), gamer.getRect())
                    bulletGroup.add(newbullet)
            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP or event.key == pygame.K_LEFT or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT):
                    if ifmove == 1:
                        ifmove = 0
                        gamer.setSpeed(0)
                    else:
                        ifmove -= 1

        # npc随机动作
        for tankI in enemyGroup:
            if (time % 15) == 0:
                i = random.randint(0, 10)
                if i < globals.difficulty:
                    tankI.setSpeed(0)
                    newbullet = bulletClass.Bullet(mapSize, tankI.getDir(), tankI.getRect())
                    bulletGroup.add(newbullet)
                tankI.randomAction(i)

        # 子弹碰撞检测及后续动作
        # 检测子弹坦克间碰撞
        for bulletI in bulletGroup:
            for tankI in enemyGroup:
                if pygame.sprite.collide_rect(bulletI, tankI):
                    bulletI.kill()
                    tankI.gotShot()
                    if tankI.getLife() == 0:
                        tankI.kill()
                        score += globals.difficulty * 100
                        print("您的分数：", score)
                        re = tankI.getRect()
                        boom = boomClass.Boom((re.left + re.right) / 2,(re.top + re.bottom) / 2)
                        boomGroup.add(boom)
            for tankI in gamerGroup:
                if pygame.sprite.collide_rect(bulletI, tankI):
                    bulletI.kill()
                    tankI.gotShot()
                    if tankI.getLife() == 0:
                        tankI.kill()
                        re = tankI.getRect()
                        boom = boomClass.Boom((re.left + re.right) / 2, (re.top + re.bottom) / 2)
                        boomGroup.add(boom)
                        print("游戏结束")
                        print("最终分数：", score)

        # 检测子弹间碰撞
        for bulletI1 in bulletGroup:
            for bulletI2 in bulletGroup:
                if pygame.sprite.collide_rect(bulletI1, bulletI2):
                    if not (bulletI1 == bulletI2):
                        bulletI1.kill()
                        bulletI2.kill()

        # 检测子弹打墙
        for bullet in bulletGroup:
            for whiteWall in whiteWallGroup:
                if pygame.sprite.collide_rect(bullet, whiteWall):
                    bullet.kill()
        for bullet in bulletGroup:
            for redWall in redWallGroup:
                if pygame.sprite.collide_rect(bullet, redWall):
                    bullet.kill()
                    redWall.kill()
                    re = redWall.getRect()
                    boom = boomClass.Boom((re.left + re.right) / 2, (re.top + re.bottom) / 2)
                    boomGroup.add(boom)

        # 检测大本营受到攻击
        for bullet in bulletGroup:
            for home in homeGroup:
                if pygame.sprite.collide_rect(bullet, home):
                    bullet.kill()
                    home.kill()
                    re = home.getRect()
                    boom = boomClass.Boom((re.left + re.right) / 2, (re.top + re.bottom) / 2)
                    boomGroup.add(boom)
                    print("游戏结束")
                    print("最终分数：", score)

        # 检测物体间碰撞
        for tank in tankGroup:
            for item in itemGroup:
                if not (tank == item):
                    if pygame.sprite.collide_rect(tank, item):
                        tank.backOff()
        # 画面刷新
        screen.blit(background, backgroundrect)
        homeGroup.draw(screen)
        wallGroup.draw(screen)
        enemyGroup.draw(screen)
        gamerGroup.draw(screen)
        bulletGroup.draw(screen)
        boomGroup.draw(screen)
        pygame.display.flip()  # 更新全部显示



print("游戏开始")
main()
