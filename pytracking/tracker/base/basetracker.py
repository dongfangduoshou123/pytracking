def track_videofile(self,videofilePath):
        "Run track with a video file input."

        #cap = cv.VideoCapture("/home/dtt/Videos/haze/v_1509066461577.avi")
        cap = cv.VideoCapture(videofilePath)
        display_name = 'Display: ' + self.params.tracker_name
        cv.namedWindow(display_name, cv.WINDOW_NORMAL | cv.WINDOW_KEEPRATIO)
        cv.resizeWindow(display_name, 960, 720)

        while True:
            success, frame = cap.read()
            if success is not True:
                break
            cv.imshow(display_name, frame)
            k = cv.waitKey(100)
            if k == 27:
                x, y, w, h = cv.selectROI(display_name, frame)
                init_state = [x, y, w, h]
                self.initialize(frame, init_state)
                break

        if hasattr(self, 'initialize_features'):
            self.initialize_features()

        while True:
            ret, frame = cap.read()
            frame_disp = frame.copy()

            # Draw box
            state, flag= self.track(frame)
            if(flag is not 'not_found'):
                state = [int(s) for s in state]
                cv.rectangle(frame_disp, (state[0], state[1]), (state[2] + state[0], state[3] + state[1]),
                             (0, 255, 0), 5)
            else:
                print("target is disappeared.")

            # Display the resulting frame
            cv.imshow(display_name, frame_disp)
            key = cv.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('r'):
                ret, frame = cap.read()
                cv.imshow(display_name, frame)
                x, y, w, h = cv.selectROI(display_name, frame)
                init_state = [x, y, w, h]
                self.initialize(frame, init_state)


        # When everything done, release the capture
        cap.release()
        cv.destroyAllWindows()
