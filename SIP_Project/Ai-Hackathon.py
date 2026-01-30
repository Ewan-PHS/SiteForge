import cv2
import numpy as np
import random
import pygame
import time


def edge_detection(image_path):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Simulate edge detection
    edge_image = cv2.Canny(image, 100, 200)

    # Return the edge image
    # cv2.imshow("3rd-angle-isometric-step", edge_image)
    return edge_image


def object_detection(image_path, num_objects=1, text="Object"):
    # Load image
    image = cv2.imread(image_path)
    height, width = image.shape[:2]

    for _ in range(num_objects):
        box_width = random.randint(int(0.05 * width), int(0.2 * width))
        box_height = random.randint(int(0.05 * height), int(0.2 * height))
        x1, y1 = random.randint(0, width - box_width), random.randint(0, height - box_height)
        x2, y2 = x1 + box_width, y1 + box_height

        # Draw a rectangle around the object
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the image with objects
    # cv2.imshow("3rd-angle-isometric-step", image)
    return image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def face_detection(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return image

pygame.init()

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))


object_image = object_detection("Images/3rd-angle-isometric-step.png")
image = pygame.image.load("Images/3rd-angle-isometric-step.png")

screen.blit(object_image, (0, 0))
while True:
    pygame.display.flip()
    time.sleep(0.5)
    break
# cv2.imshow("3rd-angle-isometric-step", object_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
