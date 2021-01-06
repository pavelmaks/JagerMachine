class ServoAct:
    def __init__(self):
        self.startPos = 0.0 #2.5 as 0 degree
        self.targetPos = 0.0
        self.holdTime = 0.0
        
        servo = 22 #pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(servo, GPIO.OUT)
        
        self.p = GPIO.PWM(servo, 50) #50 freq
        
        p.start(startPos) 
    
    def setPosition(self, pos):
        #5-10 
        p.ChangeDutyCycle(pos)
        # in servo motor,
        # 1ms pulse for 0 degree (LEFT)
        # 1.5ms pulse for 90 degree (MIDDLE)
        # 2ms pulse for 180 degree (RIGHT)

        # so for 50hz, one frequency is 20ms
        # duty cycle for 0 degree = (1/20)*100 = 5%
        # duty cycle for 90 degree = (1.5/20)*100 = 7.5%
        # duty cycle for 180 degree = (2/20)*100 = 10%
        #hard video code
    
    def hold(self):
        t = 1
        #setTargetPos
        #Timer
        #setStartPos
