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

#For unique file name
import uuid

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/record')
@login_required
def gen_record():
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
      print("Unable to read camera feed")

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

    while(True):
      ret, frame = cap.read()

      if ret == True:

        # Write the frame into the file 'output.avi'
        out.write(frame)

        # Display the resulting frame
        #cv2.imshow('frame',frame)
        return Response(gen_frames(1),
                mimetype='multipart/x-mixed-replace; boundary=frame')

        # Press Q on keyboard to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

      # Break the loop
      else:
        break

    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()

    # Closes all the frames
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

# The Home page is accessible to anyone
@main_blueprint.route('/camera2')
@login_required
def camera2():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return render_template('main/index.html')
    #return Response(gen_frames(1),
    #                mimetype='multipart/x-mixed-replace; boundary=frame')


# The Home page is accessible to anyone
@main_blueprint.route('/camera1')
@login_required
def camera1():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
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
if __name__ == '__main__':
    app.run(host='127.0.0.1')
