img = cv2.imread("./chars.png", cv2.IMREAD_GRAYSCALE)

_, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

num_labels, labels,  stats, _ = cv2.connectedComponentsWithStats(img)

stats = sorted(
    stats, key=lambda x: x[cv2.CC_STAT_LEFT])

for i in range(2, num_labels):
    x = stats[i][cv2.CC_STAT_LEFT]
    y = stats[i][cv2.CC_STAT_TOP]
    w = stats[i][cv2.CC_STAT_WIDTH]
    h = stats[i][cv2.CC_STAT_HEIGHT]

    x_2 = stats[i-1][cv2.CC_STAT_LEFT]
    y_2 = stats[i-1][cv2.CC_STAT_TOP]
    w_2 = stats[i-1][cv2.CC_STAT_WIDTH]
    h_2 = stats[i-1][cv2.CC_STAT_HEIGHT]

    # print(abs(y_2+h_2 - y))
    # print(abs(x_2+w - x))

    # print()

    if abs(y_2+h_2 - y) <= 20 and abs(x_2 - x) <= 5:
        print(chars[i-2])
        stats[i][cv2.CC_STAT_LEFT] = min(x, x_2)
        stats[i][cv2.CC_STAT_TOP] = min(y, y_2)
        stats[i][cv2.CC_STAT_WIDTH] = (
            abs(x-x_2) + max(x+w, x+w_2)) - min(x, x_2)
        stats[i][cv2.CC_STAT_HEIGHT] = (
            abs(y-y_2) + max(y+h, y+h_2)) - min(y, y_2)

        stats.pop(i-1)

for i in range(1, num_labels):
    x = stats[i][cv2.CC_STAT_LEFT]
    y = stats[i][cv2.CC_STAT_TOP]
    w = stats[i][cv2.CC_STAT_WIDTH]
    h = stats[i][cv2.CC_STAT_HEIGHT]

    img_char = img[y:y+h, x:x+w]

    dest = f"./chars/{chars[i-1]}.png"

    if chars[i-1].isupper():
        dest = f"./chars/{chars[i-1]}_.png"

    cv2.imwrite(dest, img_char)
