# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm

#For camera and streaming
from flask import render_template, Response
import cv2
import glob
import os

#For unique file name
import uuid

main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.route('/play_video/<video>')
@login_required
def play_video(video):
    video_file = dirpath = os.getcwd() + '/videos/' + video
    play_videoFile(video_file,mirror=False)
    '''print("The video is : " + video)
    cap = cv2.VideoCapture('video')
    while (cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    return 1
    '''

def play_videoFile(filePath,mirror=False):

    cap = cv2.VideoCapture(filePath)
    cv2.namedWindow('Video Life2Coding',cv2.WINDOW_AUTOSIZE)
    while True:
        ret_val, frame = cap.read()

        if mirror:
            frame = cv2.flip(frame, 1)

        cv2.imshow('Video Life2Coding', frame)

        if cv2.waitKey(1) == 27:
            break  # esc to quit

    cv2.destroyAllWindows()

#View previously recorded videos
@main_blueprint.route('/list_recorded_videos')
@login_required
def list_recorded_videos():
    import platform
    operating_system = platform.system()

    if operating_system == 'Linux':
        dirpath = os.getcwd() + '/videos' #get the video directory or folder

        files = next(os.walk(dirpath))[2]
#        print(files.str())
        #files = dirpath + '/videos'
        """List recorded videos."""
        return render_template('main/list_recorded_videos.html', files = files, dirpath = dirpath)



    elif operating_system == 'Windows':
        print("Windows OS")

    else:
        print("Unsupported Operation System")



# The Home page is accessible to anyone
@main_blueprint.route('/camera2')
@login_required
def camera2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    #return render_template('main/index.html')
    return Response(gen_record2(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# The Home page is accessible to anyone
@main_blueprint.route('/camera1')
@login_required
def camera1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_record(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    #return render_template('main/index1.html')


@main_blueprint.route('/double_cam.html')
@login_required
def double_cam():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return render_template('main/double_cam.html')
    #return Response(gen_frames(1),
    #                mimetype='multipart/x-mixed-replace; boundary=frame')


# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('main/home_page.html')


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('main/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')


@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)

@main_blueprint.route('/record')
@login_required
def gen_record():
    import numpy as np
    import cv2
    from datetime import datetime
    import uuid

    now = datetime.now()
    unique_filename = str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second) #dt_object #str(uuid.uuid4())

    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('videos/record_' + str(unique_filename) +'.avi',fourcc, 20.0, (640,480))
    while(cap.isOpened()):
      ret, frame = cap.read()
      if ret==True:
        frame = cv2.flip(frame,0)
        # write the flipped frame
        out.write(frame)
        cv2.imshow('Live Stream Video',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      else:
        break
    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

@main_blueprint.route('/record')
@login_required
def gen_record2():
    import numpy as np
    import cv2
    from datetime import datetime
    import uuid

    now = datetime.now()
    unique_filename = str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "_" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second) #dt_object #str(uuid.uuid4())

    cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('videos/record_' + str(unique_filename) +'.avi',fourcc, 20.0, (640,480))
    while(cap.isOpened()):
      ret, frame = cap.read()
      if ret==True:
        frame = cv2.flip(frame,0)
        # write the flipped frame
        out.write(frame)
        cv2.imshow('Live Stream Video',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      else:
        break
    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()

@login_required
def gen_frames(number = 0): #generate frame by frame from camera
    '''
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    # Define the fps to be equal to 10. Also frame size is passed.
    unique_filename = str(uuid.uuid4())
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    '''
    #unique_filename = 'surveillannce' + str(uuid.uuid4())
    #out = cv2.VideoWriter('unique_filename.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    camera = cv2.VideoCapture(0)   #webcam
    if number == 0:
        pass # do nothing
    else:
        camera = cv2.VideoCapture(1)   #external camera

    while True:
        #Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == '__main__':
    app.run(host='127.0.0.1')
