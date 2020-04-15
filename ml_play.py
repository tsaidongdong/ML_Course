"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_position_history = []

    comm.ml_ready()
    while True:
        
        scene_info = comm.get_scene_info()
        ball_position_history.append(scene_info.ball)
        platform_center_x = scene_info.platform[0]+25
        if (len(ball_position_history)) == 1:
            ball_going_down = 0
        elif ball_position_history[-1][1] - ball_position_history[-2][1]:
            ball_going_down = 1
            vy = ball_position_history[-1][1]-ball_position_history[-2][1]
            vx = ball_position_history[-1][0]-ball_position_history[-2][0]
        else:
            ball_going_down =0

        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:

            comm.ml_ready()
            continue

        if ball_going_down ==1 :

            move_distance=(400-ball_position_history[-1][1])/vy*vx
            if vy<0 and vx<0:
                move_distance=-move_distance
            if vx>0 and vy<0:
                move_distance=-move_distance
            ball_destination = ball_position_history[-1][0]+move_distance
            #print(platform_center_x
            print(ball_destination)
            if ball_destination>200:
                ball_destination=200-(ball_destination-200)
            if ball_destination<0:
                ball_destination=-(ball_destination)
            print(ball_destination)
            if ball_destination>platform_center_x   and ball_position_history[-1][1]>200 :
                #print(ball_destination)

                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)

            elif ball_destination<platform_center_x  and ball_position_history[-1][1]>200:
                #print(ball_destination)
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            else:
                ball_destination = platform_center_x
