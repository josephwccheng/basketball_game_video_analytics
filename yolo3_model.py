import cv2, os
import numpy as np
import matplotlib.pyplot as plt

# Define objectness, prob and NMS thresholds
OBJ_THRESH = .7
P_THRESH = .5
NMS_THRESH = .3
# Set random seed
np.random.seed(999)

# Video Name
video_name = "Holy Guacamole - Season 2, Game 3-720p.mp4"
#%% Load YOLOv3 COCO weights, configs and class IDs
# Import class names

with open('yolov3/coco.names', 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
    colors = np.random.randint(0, 255, (len(classes), 3))
    # Give the configuration and weight files for the model and load the network using them
    cfg = 'yolov3/yolov3.cfg'
    weights = 'yolov3/yolov3.weights'
    # Load model
    model = cv2.dnn.readNetFromDarknet(cfg, weights)
    # Extract names from output layers
    layersNames = model.getLayerNames()
    outputNames = [layersNames[i - 1] for i in model.getUnconnectedOutLayers()]

#%% Define function to extract object coordinates if successful in detection
def where_is_it(frame, outputs):
    frame_h = frame.shape[0]
    frame_w = frame.shape[1]
    bboxes, probs, class_ids = [], [], []
    for preds  in outputs: # different detection scales
        hits = np.any(preds [:, 5:] > P_THRESH, axis=1) & (preds [:, 4] > OBJ_THRESH)
        # Save prob and bbox coordinates if both objectness and probability pass respective thresholds
        for i in np.where(hits)[0]:
            pred = preds [i, :]
            center_x = int(pred[0] * frame_w)
            center_y = int(pred[1] * frame_h)
            width = int(pred[2] * frame_w)
            height = int(pred[3] * frame_h)
            left = int(center_x - width / 2)
            top = int(center_y - height / 2)
            # Append all info
            # if len(np.where(hits)[0]) >= 1:
            bboxes.append([left, top, width, height])
            probs.append(float(np.max(pred[5:])))
            class_ids.append(np.argmax(pred[5:]))
    return bboxes, probs, class_ids

#%% Load video capture and init VideoWriter
vid = cv2.VideoCapture('.data/' + video_name)
vid_w, vid_h = int(vid.get(3)), int(vid.get(4))

# Check if camera opened successfully
assert vid.isOpened()

out = cv2.VideoWriter('output/yolo_' + video_name, cv2.VideoWriter_fourcc(*'mp4v'),
vid.get(cv2.CAP_PROP_FPS), (vid_w, vid_h))
# Check if capture started successfully


#%% Initiate processing

# Init frame_count
frame_count = 0
# Create new window
cv2.namedWindow('stream')

while(vid.isOpened()):
    # Perform detection every 60 frames
    perform_detection = frame_count % 60 == 0
    ret, frame = vid.read()
    if ret:
        print(frame)
        if perform_detection: # perform detection
            blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), [0,0,0], 1, crop=False)
            print(blob)
            # Pass blob to model
            model.setInput(blob)
            # Execute forward pass
            outputs = model.forward(outputNames)
            bboxes, probs, class_ids = where_is_it(frame, outputs)
            if len(bboxes) > 0:
                # Init multitracker
                mtracker = cv2.legacy.MultiTracker_create()
                # Apply non-max suppression and pass boxes to the multitracker
                idxs = cv2.dnn.NMSBoxes(bboxes, probs, P_THRESH, NMS_THRESH)
                for i in idxs:
                    bbox = [int(v) for v in bboxes[i]]
                    x, y, w, h = bbox
                    # Use median flow
                    mtracker.add(cv2.legacy.TrackerMedianFlow_create(), frame, (x, y, w, h))
                # Increase frame_counter
                frame_count += 1
            else: # declare failure
                cv2.putText(frame, 'Detection failed', (20, 80), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2)
        else: # perform tracking
            is_tracking, bboxes = mtracker.update(frame)
            if is_tracking:
                for i, bbox in enumerate(bboxes):
                    x, y, w, h = [int(val) for val in bbox]
                    class_id = classes[class_ids[idxs[i]]]
                    col = [int(c) for c in colors[class_ids[idxs[i]], :]]
                    # Mark tracking frame with corresponding color, write class name on top
                    cv2.rectangle(frame, (x, y), (x+w, y+h), col, 2)
                    cv2.putText(frame, class_id, (x, y - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 2)
                # Increase frame_counter
                frame_count += 1
            # If tracking fails, reset frame_count to trigger detection
            else:
                frame_count = 0

        # Display the resulting frame
        cv2.imshow('stream', frame)
        out.write(frame)

        # Exit if q is pressed
        waitKey = cv2.waitKey(5)
        if waitKey & 0xFF == ord('q'): 
            break
    # Break if capture read does not work
    else:
        print('Exhausted video capture.')
        break
print("code completed")
vid.release()
out.release()
cv2.destroyAllWindows()