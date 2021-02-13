#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scratra.scratra import *
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import time
import pygame
from aip import AipSpeech

# 树莓派小车电机驱动初始化
PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24

BtnPin = 19
Gpin = 5
Rpin = 6
SensorRight = 16
SensorLeft = 12


@end
def end(scratch):
    GPIO.cleanup()


@broadcast("up")
def robotup(scratch):
    robot_speech("向前走")
    L_Motor.ChangeDutyCycle(50)
    GPIO.output(AIN2, False)  #AIN2
    GPIO.output(AIN1, True)  #AIN1

    R_Motor.ChangeDutyCycle(50)
    GPIO.output(BIN2, False)  #BIN2
    GPIO.output(BIN1, True)  #BIN1
    time.sleep(0)


@broadcast("down")
def robotdown(scratch):
    robot_speech("向后走")
    L_Motor.ChangeDutyCycle(50)
    GPIO.output(AIN2, True)  #AIN2
    GPIO.output(AIN1, False)  #AIN1

    R_Motor.ChangeDutyCycle(50)
    GPIO.output(BIN2, True)  #BIN2
    GPIO.output(BIN1, False)  #BIN1
    time.sleep(0)


@broadcast("right")
def robotright(scratch):
    robot_speech("向右走")
    L_Motor.ChangeDutyCycle(50)
    GPIO.output(AIN2, False)  #AIN2
    GPIO.output(AIN1, True)  #AIN1

    R_Motor.ChangeDutyCycle(50)
    GPIO.output(BIN2, True)  #BIN2
    GPIO.output(BIN1, False)  #BIN1
    time.sleep(0)


@broadcast("left")
def robotleft(scratch):
    robot_speech("向左走")
    L_Motor.ChangeDutyCycle(50)
    GPIO.output(AIN2, True)  #AIN2
    GPIO.output(AIN1, False)  #AIN1

    R_Motor.ChangeDutyCycle(50)
    GPIO.output(BIN2, False)  #BIN2
    GPIO.output(BIN1, True)  #BIN1
    time.sleep(0)


@broadcast("stop")
def robotstop(scratch):
    robot_speech("停止")
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)  #AIN2
    GPIO.output(AIN1, False)  #AIN1

    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)  #BIN2
    GPIO.output(BIN1, False)  #BIN1
    time.sleep(0)


def robot_speech(content):
    text = content
    result = aipSpeech.synthesis(text=text,
                                 options={
                                     'spd': 5,
                                     'vol': 9,
                                     'per': 0,
                                 })
    if not isinstance(result, dict):
        with open('makerobo.mp3', 'wb') as f:
            f.write(result)
    else:
        print(result)
    #我们利用树莓派自带的pygame
    pygame.mixer.init()
    pygame.mixer.music.load('makerobo.mp3')
    pygame.mixer.music.play()


#初始化舵机
pwm = Adafruit_PCA9685.PCA9685()
# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

if __name__ == "__main__":
    GPIO.setwarnings(False)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(AIN2, GPIO.OUT)
    GPIO.setup(AIN1, GPIO.OUT)
    GPIO.setup(PWMA, GPIO.OUT)

    GPIO.setup(BIN1, GPIO.OUT)
    GPIO.setup(BIN2, GPIO.OUT)
    GPIO.setup(PWMB, GPIO.OUT)

    GPIO.setup(Gpin, GPIO.OUT)  # 设置绿色Led引脚模式输出
    GPIO.setup(Rpin, GPIO.OUT)  # 设置红色Led引脚模式输出
    GPIO.setup(BtnPin, GPIO.IN,
               pull_up_down=GPIO.PUD_UP)  # 设置输入BtnPin模式，拉高至高电平(3.3V)
    GPIO.setup(SensorRight, GPIO.IN)
    GPIO.setup(SensorLeft, GPIO.IN)

    L_Motor = GPIO.PWM(PWMA, 100)
    L_Motor.start(0)

    R_Motor = GPIO.PWM(PWMB, 100)
    R_Motor.start(0)

    #这里需要填你自己的id和密钥
    APP_ID = '16226519'
    API_KEY = '5KVxQVES4LSja0u2G4y8m1O9'
    SECRET_KEY = 'KhaXYwGLSmQYgnwHkuXKpV9MO2ta0bQ8'

    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    run()
