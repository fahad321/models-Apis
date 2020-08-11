import base64
import cv2
import os
from glob import glob
import matplotlib.pyplot as plt


def extract_features(img):
    fast = cv2.xfeatures2d.SURF_create(500)
    kp, des = fast.detectAndCompute(img, None)
    img2 = cv2.drawKeypoints(img, kp, None)
    return kp, des


def extract_features_dataset(images, extract_features_function):
    kp_list = []
    des_list = []
    i = 0
    for img in images:
        kp, des = extract_features(img)
        i += 1
        kp_list.append(kp)
        des_list.append(des)
    return kp_list, des_list


def match_features(des1, des2):
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    match = flann.knnMatch(des1, des2, k=2)
    ### END CODE HERE ###

    return match


# Optional
def filter_matches_distance(match, dist_threshold):
    filtered_match = []
    ### START CODE HERE ###
    for i, (m, n) in enumerate(match):
        if m.distance < n.distance * dist_threshold:
            filtered_match.append(m)

    ### END CODE HERE ###
    return filtered_match


# Optional
def filter_matches_dataset(filter_matches_distance, matches, dist_threshold):
    filtered_matches = []

    ### START CODE HERE ###
    for match in matches:
        filtered_match = filter_matches_distance(match, dist_threshold)
        filtered_matches.append(filtered_match)

    ### END CODE HERE ###

    return filtered_matches


def visualize_matches(image1, kp1, image2, kp2, match):
    image_matches = cv2.drawMatchesKnn(image1, kp1, image2, kp2, match, None, flags=2)
    plt.figure(figsize=(16, 6), dpi=100)
    plt.imshow(image_matches)


# In[9]:


def match_features_dataset(des_list, match_features):
    matches = []

    ### START CODE HERE ###
    for i in range(len(des_list) - 1):
        des1 = des_list[i]
        des2 = des_list[i + 1]
        match = match_features(des1, des2)
        matches.append(match)

    ### END CODE HERE ###

    return matches


def run_detections(img, threshold=100):
    samples = glob("unique/*")
    sample_images = []
    res = {}
    test_kp, test_des = extract_features(img)
    fil_mats = {}
    for jj in samples:
        j = cv2.imread(jj)
        j = cv2.cvtColor(j, cv2.COLOR_BGR2GRAY)
        sample_kp, sample_des = extract_features(j)
        match = match_features(test_des, sample_des)
        filtered_match = filter_matches_distance(match, 0.7)

        print(len(filtered_match), img, jj)
        fil_mats[jj] = len(filtered_match)
        cv2.imshow("i", img)
        cv2.imshow("j", j)
        cv2.waitKey(0)
    cv2.destroyAllWindows()

    arr = [i[0] for i in fil_mats]

    k = max(fil_mats, key=fil_mats.get)
    val = fil_mats.get(k)
    if val < threshold:
        res["detected"] = False
    else:
        res["detected"] = True
    res["detection"] = k
    res["matched_features"] = val
    etval, buffer = cv2.imencode(".png", img)
    jpg_as_text = base64.b64encode(buffer)
    res["img"] = base64.b64encode(jpg_as_text)

    return res

