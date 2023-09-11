import os
from rembg import remove
import cv2
import numpy as np
import json
from sklearn.cluster import KMeans

# Load color mappings from the JSON file
with open("./hex_map.json", "r") as j:
    c_dict = json.load(j)

color_dic = {
    "beige": 0,
    "black": 1,
    "blue": 2,
    "brown": 3,
    "burgundy": 4,
    "gray": 5,
    "green": 6,
    "khaki": 7,
    "lightgreen": 8,
    "lightpurple": 9,
    "mint": 10,
    "navy": 11,
    "orange": 12,
    "pink": 13,
    "purple": 14,
    "red": 15,
    "skyblue": 16,
    "teal": 17,
    "white": 18,
    "yellow": 19,
}


# Helper functions for background removal and color prediction
def remove_background(img_name):
    input = cv2.imread(img_name)
    output = remove(input, only_mask=True)
    cv2.imwrite(os.path.join(f"{img_name[:-4]}_mask.png"), output)
    return os.path.join(f"{img_name[:-4]}_mask.png")


def make_white(img_name):
    img = cv2.imread(img_name)
    img = remove(img)
    img = cv2.cvtColor(cv2.COLOR_BGR2RGB)
    black = np.where((img[:, :, 0] == 0) & (img[:, :, 1] == 0) & (img[:, :, 2] == 0))
    img[black] = (255, 255, 255)  # Make a white pixels
    cv2.imwrite(os.path.join(f"{img_name[:-4]}_white.png"))


with open("./hex_map.json", "r") as j:
    c_dict = json.load(j)


def show_colors(c):
    colors = []
    for rgb in c:
        paper = np.full((200, 200, 3), rgb, dtype=np.uint8)
        colors.append(paper)

    cv2.imshow("colors", cv2.cvtColor(np.hstack(colors), cv2.COLOR_BGR2RGB))


def rgb_to_hex(rgb):  # convert rgb array to hex code
    return "{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def cvt216(pxs):  # convert rgb into the value in 216
    st = [0, 51, 102, 153, 204, 255]
    p0 = min(st, key=lambda x: abs(x - pxs[0]))
    p1 = min(st, key=lambda x: abs(x - pxs[1]))
    p2 = min(st, key=lambda x: abs(x - pxs[2]))

    return np.array((p0, p1, p2))


def pixels_argsort(li):  # argsort pixels in list, must be 3 channels
    return np.unique(li, axis=0, return_counts=True)


def dom_with_Kmeans(img_list, k=3):  # use kmeans
    pixels = img_list

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)
    # Get the colors
    colors = kmeans.cluster_centers_
    # Get the labels (which cluster each pfixel belongs to)
    labels = kmeans.labels_
    # Count the frequency of each label
    label_counts = np.bincount(labels)

    labels = np.argsort(label_counts)[::-1]  # argsort for cluster labels

    dom_counts = [label_counts[i] for i in labels[:3]]
    total = sum(dom_counts)
    dom_counts = [d / total for d in dom_counts]  # each cluster's rate

    dom_colors = [colors[d_lab] for d_lab in labels[:3]]  # 3 most colors

    return dom_colors, dom_counts


def classify_color(image_path, mask_img=None):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image_rgb.shape

    if mask_img:
        mask = cv2.imread(mask_img)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        cropped_list = np.array(
            [
                image_rgb[i][j]
                for i in range(height)
                for j in range(width)
                if mask[i][j] > 100
            ]
        )

    kmeans_color, kmeans_dis = dom_with_Kmeans(cropped_list)
    fst, snd, trd = kmeans_color[:3]
    print(kmeans_dis)
    print(fst)
    print(snd)
    print(trd)

    fst_cvt216 = cvt216(fst)
    snd_cvt216 = cvt216(snd)
    trd_cvt216 = cvt216(trd)

    # return classified_color
    return (
        c_dict[rgb_to_hex(fst_cvt216)],
        c_dict[rgb_to_hex(snd_cvt216)],
        c_dict[rgb_to_hex(trd_cvt216)],
    )


def color_test(org_path, mask_img):
    pred_color, p2, p3 = classify_color(org_path, mask_img)
    return pred_color
