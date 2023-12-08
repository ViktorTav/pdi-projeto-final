# ALPHA = 1.5
# BETA = 0.3


# img = cv2.imread(
#         "C:/Users/vikto/Documents/Utfpr/5_periodo/pdi/projeto_final/imgs/3.png", cv2.IMREAD_UNCHANGED)

#     img = img.astype(np.float32) / 255
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     height = img.shape[0]
#     width = img.shape[1]

#     _, gray = cv2.threshold(gray, 0.9, 1, cv2.THRESH_BINARY)

#     cv2.imwrite("new_img.png", gray*255)

#     first_line = img[0]

#     for y in range(0, width):
#         red = first_line[y][2]
#         green = first_line[y][1]
#         blue = first_line[y][0]

#         red_percentage = red - max(green, blue)
#         yellow_percentage = abs(red-green) + (red+green) - blue/(red+green)
#         green_percentage = (green+blue)/2 - red

#         pixel_color = max(red_percentage, max(
#             yellow_percentage, green_percentage))

#         if pixel_color == red_percentage:
#             first_line[y] = 0.2
#         elif pixel_color == yellow_percentage:
#             first_line[y] = 0.5
#         elif pixel_color == green_percentage:
#             first_line[y] = 1

#     cv2.imwrite("new_img.png", img*255)


#     # interval = Interval(0.5, get_screen_info)

#     ALPHA = 1.5
#     BETA = 0.3

#     img = cv2.imread(
#         "./imgs/omen.png", cv2.IMREAD_UNCHANGED)

#     check_agent(img)

# img = img.astype(np.float32) / 255
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# height = img.shape[0]
# width = img.shape[1]

# _, gray = cv2.threshold(gray, 0.83, 1, cv2.THRESH_BINARY)

# cv2.imwrite("threshold.png", gray*255)

# first_line = img[0]

# colors = []

# for y in range(0, width):
#     red = first_line[y][2]
#     green = first_line[y][1]
#     blue = first_line[y][0]

#     red_percentage = red - max(green, blue)
#     yellow_percentage = (red+green)/2 - blue
#     green_percentage = (green+blue)/2 - red

#     if red_percentage > 0.1:
#         colors.append("r")
#         first_line[y] = 0.2
#     elif yellow_percentage > 0.05:
#         colors.append("y")
#         first_line[y] = 0.5
#     elif green_percentage > 0.1:
#         colors.append("g")
#         first_line[y] = 1

# print(colors)

# cv2.imwrite("new_img.png", img*255)
