from XInput import *
import serial
import struct
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
#set_deadzone(DEADZONE_TRIGGER, 10)
import struct

# class Controller:
#     def __init__(self, center):
#         self.center = center

# controllers = (Controller((150., 100.)),
#                Controller((450., 100.)),
#                Controller((150., 300.)),
#                Controller((450., 300.)))



port = "COM9"  # Replace with the appropriate COM port name 9COM
baudrate = 57600  # Replace with the desired baud rate

ser = serial.Serial(port, baudrate=baudrate)
left_position=[0,0]
l_thumb_stick_pos=[127,127]
r_thumb_stick_pos=[0,0]
r_trigger_index_pos=0
l_trigger_index_pos=0
a_button=0
b_button=0
x_button=0
y_button=0
left_shoulder=0
right_shoulder=0
dpad_left = 0
dpad_right = 0
dpad_up = 0
dpad_down = 0

def crc16(data : bytearray, offset , length):
    if data is None or offset < 0 or offset > len(data)- 1 and offset+length > len(data):
        return 0
    crc = 0xFFFF
    for i in range(0, length):
        crc ^= data[offset + i] << 8
        for j in range(0,8):
            if (crc & 0x8000) > 0:
                crc =(crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF







while 1:

    events = get_events()
    #if ser.in_waiting > 0:
        # line = ser.readline().decode().strip()
        # print(line)
    for event in events:
        #controller = controllers[event.user_index]
        if event.type == EVENT_CONNECTED:
            #print('EBAT CONNECTED')
            pass
            #canvas.itemconfig(controller.on_indicator, fill="light green")

        elif event.type == EVENT_DISCONNECTED:
            pass
            #canvas.itemconfig(controller.on_indicator, fill="")

        elif event.type == EVENT_STICK_MOVED:
            if event.stick == LEFT:
                l_thumb_stick_pos=(int(round(127+(127*event.x),0)),int(round(127+(127*event.y),0)))
                left_position=l_thumb_stick_pos
                #print(l_thumb_stick_pos)
                #canvas.coords(controller.l_thumb_stick, (
                #l_thumb_stick_pos[0] - 10, l_thumb_stick_pos[1] - 10, l_thumb_stick_pos[0] + 10,
                #l_thumb_stick_pos[1] + 10))

            elif event.stick == RIGHT:
                # r_thumb_stick_pos = (int(round(255 * (event.x), 0)),
                #                      int(round(255 * (event.y), 0)))
                r_thumb_stick_pos=(int(round(127+(127*event.x),0)),int(round(127+(127*event.y),0)))
                #print(127+event.x*127)
                #print(r_thumb_stick_pos)
        elif event.type == EVENT_BUTTON_PRESSED:
            if event.button == "A":
                if a_button==1:
                    a_button=0
                else:
                    a_button=1
            elif event.button == "B":
                if b_button==1:
                    b_button=0
                else:
                    b_button=1
            elif event.button == "Y":
                if y_button==1:
                    y_button=0
                else:
                    y_button=1
            elif event.button == "X":
                if x_button == 1:
                    x_button = 0
                else:
                    x_button = 1

            elif event.button == "DPAD_LEFT":
                dpad_left=1
            elif event.button == "DPAD_RIGHT":
                dpad_right = 1
            elif event.button == "DPAD_UP":
                dpad_up=1
            elif event.button == "DPAD_DOWN":
                dpad_down = 1

            elif event.button == "LEFT_SHOULDER":
                left_shoulder=1
            elif event.button == "RIGHT_SHOULDER":
                right_shoulder=1

        elif event.type == EVENT_BUTTON_RELEASED:
            if event.button == "DPAD_LEFT":
                dpad_left = 0
            elif event.button == "DPAD_RIGHT":
                dpad_right = 0
            elif event.button == "DPAD_UP":
                dpad_up = 0
            elif event.button == "DPAD_DOWN":
                dpad_down = 0
            elif event.button == "LEFT_SHOULDER":
                left_shoulder = 0
            elif event.button == "RIGHT_SHOULDER":
                right_shoulder = 0


        elif event.type == EVENT_TRIGGER_MOVED:
            if event.trigger == LEFT:
                l_trigger_index_pos = (int(round(127 * event.value, 0)))
            elif event.trigger == RIGHT:
                r_trigger_index_pos = (int(round(127 * event.value, 0)))
    #print(left_position)
    if a_button==1:
        control_mode='Manipulator control'
    else:
        control_mode='Driving mode'

    #print(f"0xff {l_thumb_stick_pos[0]}|{l_thumb_stick_pos[1]}|{r_thumb_stick_pos[0]}|{r_thumb_stick_pos[1]}")
    #ser.write((f"0xff {l_thumb_stick_pos[0]}|{l_thumb_stick_pos[1]}|{r_thumb_stick_pos[0]}|{r_thumb_stick_pos[1]}l").encode())
# Правильный авриант    #str_otpr='x'+str(l_thumb_stick_pos[0])+'|'+str(l_thumb_stick_pos[1])+'|'+str(r_thumb_stick_pos[0])+'|'+str(r_thumb_stick_pos[1])+'|'+str(a_button)+'|'+str(b_button)+'b'
    control_sum=0
    # control_sum=l_thumb_stick_pos[0]+l_thumb_stick_pos[1]+r_thumb_stick_pos[0]+\
    #             r_thumb_stick_pos[1]+a_button+b_button+x_button+y_button+dpad_left+dpad_right+dpad_up+dpad_down+\
    #             right_shoulder+left_shoulder+r_trigger_index_pos+l_trigger_index_pos
    # control_ost=((control_sum))%113




    str_otpr_w=[(l_thumb_stick_pos[0]),(l_thumb_stick_pos[1]),(r_thumb_stick_pos[0]),(r_thumb_stick_pos[1]),a_button,b_button,x_button,y_button,dpad_right,dpad_left,dpad_up,dpad_down,right_shoulder,left_shoulder,r_trigger_index_pos,l_trigger_index_pos]
             # +'|'+str(b_button)+'|'+str(x_button)+'|'+str(y_button)+'|'+str(dpad_left)+'|'+str(dpad_right)+'|'+str(dpad_up)+'|'+str(dpad_down)
             # +'|'+str(control_ost)+'99')


    control_crc=crc16(str_otpr_w,0,16)
    crc0 = control_crc & 0x00FF
    crc1 = (control_crc & 0xFF00) >> 8

    str_otpr = [255,(l_thumb_stick_pos[0]), (l_thumb_stick_pos[1]), (r_thumb_stick_pos[0]), (r_thumb_stick_pos[1]),
                a_button, b_button, x_button, y_button, dpad_right, dpad_left, dpad_up, dpad_down, right_shoulder,
                left_shoulder, r_trigger_index_pos, l_trigger_index_pos,crc0,crc1]


    # +'|'+str(b_button)+'|'+str(x_button)+'|'+str(y_button)+'|'+str(dpad_left)+'|'+str(dpad_right)+'|'+str(dpad_up)+'|'+s
    # str_otpr=('x'+str(l_thumb_stick_pos[0])+'|'+str(l_thumb_stick_pos[1])+
    #           '|'+str(r_thumb_stick_pos[0])+'|'+str(r_thumb_stick_pos[1])+'|'+str(a_button)+'|'+str(b_button)+'k')

#     str_otpr=('y'+str(l_thumb_stick_pos[0])+'|'+str(l_thumb_stick_pos[1])+'|'+str(r_thumb_stick_pos[0])+
#               '|'+str(r_thumb_stick_pos[1])+'|'+str(a_button)+'|'+str(b_button)+'|'+str(x_button)+'|'+
#               str(dpad_left)+'|'+str(dpad_right)+'|'+str(dpad_up)+'|'+str(dpad_down)+'|'+str(left_shoulder)+'|'+str(right_shoulder)+'|'+str(l_trigger_index_pos)+'|'+str(r_trigger_index_pos)
# +'|'+str(control_ost)+'k')
#     #arr1=[14,'|',88,'|']
#print(str_otpr.encode('ascii'))
    ser.write(str_otpr)
    print(str_otpr)

    #ser.write(str_otpr.encode('ascii'))
    time.sleep(0.015)








        # elif event.type == EVENT_TRIGGER_MOVED:
        #     if event.trigger == LEFT:
        #
        #         l_trigger_index_pos = (
        #         controller.l_trigger_pos[0], controller.l_trigger_pos[1] - 20 + int(round(40 * event.value, 0)))
        #         canvas.coords(controller.l_trigger_index, (
        #         l_trigger_index_pos[0] - 10, l_trigger_index_pos[1] - 5, l_trigger_index_pos[0] + 10,
        #         l_trigger_index_pos[1] + 5))
        #     elif event.trigger == RIGHT:
        #         r_trigger_index_pos = (
        #         controller.r_trigger_pos[0], controller.r_trigger_pos[1] - 20 + int(round(40 * event.value, 0)))
        #         canvas.coords(controller.r_trigger_index, (
        #         r_trigger_index_pos[0] - 10, r_trigger_index_pos[1] - 5, r_trigger_index_pos[0] + 10,
        #         r_trigger_index_pos[1] + 5))
        #
        # elif event.type == EVENT_BUTTON_PRESSED:
        #     if event.button == "LEFT_THUMB":
        #         canvas.itemconfig(controller.l_thumb_stick, fill="red")
        #     elif event.button == "RIGHT_THUMB":
        #         canvas.itemconfig(controller.r_thumb_stick, fill="red")
        #
        #     elif event.button == "LEFT_SHOULDER":
        #         canvas.itemconfig(controller.l_shoulder, fill="red")
        #     elif event.button == "RIGHT_SHOULDER":
        #         canvas.itemconfig(controller.r_shoulder, fill="red")
        #
        #     elif event.button == "BACK":
        #         canvas.itemconfig(controller.back_button, fill="red")
        #     elif event.button == "START":
        #         canvas.itemconfig(controller.start_button, fill="red")
        #
        #
        #
        #     elif event.button == "A":
        #         print('a pres')
        #     elif event.button == "B":
        #         canvas.itemconfig(controller.B_button, fill="red")
        #     elif event.button == "Y":
        #         canvas.itemconfig(controller.Y_button, fill="red")
        #     elif event.button == "X":
        #         canvas.itemconfig(controller.X_button, fill="red")
        #
        # elif event.type == EVENT_BUTTON_RELEASED:
        #     if event.button == "LEFT_THUMB":
        #         canvas.itemconfig(controller.l_thumb_stick, fill="")
        #     elif event.button == "RIGHT_THUMB":
        #         canvas.itemconfig(controller.r_thumb_stick, fill="")
        #
        #     elif event.button == "LEFT_SHOULDER":
        #         canvas.itemconfig(controller.l_shoulder, fill="")
        #     elif event.button == "RIGHT_SHOULDER":
        #         canvas.itemconfig(controller.r_shoulder, fill="")
        #
        #     elif event.button == "BACK":
        #         canvas.itemconfig(controller.back_button, fill="")
        #     elif event.button == "START":
        #         canvas.itemconfig(controller.start_button, fill="")
        #
        #     elif event.button == "DPAD_LEFT":
        #         canvas.itemconfig(controller.dpad_left, fill="")
        #     elif event.button == "DPAD_RIGHT":
        #         canvas.itemconfig(controller.dpad_right, fill="")
        #     elif event.button == "DPAD_UP":
        #         canvas.itemconfig(controller.dpad_up, fill="")
        #     elif event.button == "DPAD_DOWN":
        #         pass
        #
        #     elif event.button == "A":
        #         pass
        #     elif event.button == "B":
        #        pass
        #     elif event.button == "Y":
        #         pass
        #     elif event.button == "X":
        #         pass