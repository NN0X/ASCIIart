import cv2

class ASCIIart:
    def __init__(self, color_balance=0.5, charset="#@*:. ", width=80, height=40):
        self.image = None
        self.ascii_art = None
        self.color_balance = color_balance
        self.charset = charset
        self.width = width
        self.height = height

    def load_image(self, image_path):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError("Image not found or unable to load.")

    def prepare_image(self):
        if self.image is None:
            raise ValueError("Image not loaded. Please load an image first.")
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image = cv2.GaussianBlur(self.image, (5, 5), 0)
        self.image = cv2.addWeighted(self.image, 1.5, self.image, -0.5, 0)
        self.image = cv2.convertScaleAbs(self.image, alpha=1.5, beta=0)
        self.image = cv2.resize(self.image, (self.width, self.height))
        self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)

    def generate_ascii_art(self):
        if self.image is None:
            raise ValueError("Image not loaded. Please load an image first.")

        ascii_art = []
        height, width = self.image.shape
        for y in range(height):
            line = ""
            for x in range(width):
                pixel_value = self.image[y, x]
                pixel_value = int(pixel_value * self.color_balance)
                if pixel_value < 0:
                    pixel_value = 0
                elif pixel_value > 255:
                    pixel_value = 255
                pixel_value = int(255 * (pixel_value / 255) ** 0.5)
                index = int(pixel_value / 255 * (len(self.charset) - 1))
                if index < 0:
                    index = 0
                elif index >= len(self.charset):
                    index = len(self.charset) - 1

                line += self.charset[index]
            ascii_art.append(line)

        self.ascii_art = "\n".join(ascii_art)
        return self.ascii_art

if __name__ == "__main__":
    ascii_art = ASCIIart(color_balance=0.7)
    try:
        path = input("Enter the path to the image: ")
        ascii_art.load_image(path)
        ascii_art.prepare_image()
        art = ascii_art.generate_ascii_art()
        print(art)
    except ValueError as e:
        print(e)
