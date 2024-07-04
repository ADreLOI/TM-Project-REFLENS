import math

class Hand:
    MAX_THRESHOLD = 0.1  # Example threshold, adjust as needed
    MIN_THRESHOLD = 0.05  # Example threshold, adjust as needed

    def __init__(self, landmarks):
        self.landmarks = landmarks
        self.init_hand()

    def init_hand(self):
        self.palm = self.landmarks.landmark[0]
        self.thumb_tip = self.landmarks.landmark[4]
        self.index_tip = self.landmarks.landmark[8]
        self.middle_tip = self.landmarks.landmark[12]
        self.ring_tip = self.landmarks.landmark[16]
        self.pinky_tip = self.landmarks.landmark[20]

    def distance(self, point1, point2):
        """Calculate the Euclidean distance between two landmarks."""
        return math.sqrt(
            (point1.x - point2.x) ** 2 +
            (point1.y - point2.y) ** 2
        )

    def is_finger_open(self, finger_tip):
        """Determine if a finger is open based on the distance from the palm."""
        distance_to_palm = self.distance(finger_tip, self.palm)
        return distance_to_palm > self.palm.y + self.MAX_THRESHOLD

    def is_finger_closed(self, finger_tip):
        """Determine if a finger is closed based on the distance from the palm."""
        distance_to_palm = self.distance(finger_tip, self.palm)
        return (
            distance_to_palm < self.palm.y + self.MIN_THRESHOLD or
            distance_to_palm < self.palm.y or
            distance_to_palm < 0
        )

    def is_hand_opened(self):
        """Determine if the hand is opened by checking all fingers."""
        return (
            self.is_finger_open(self.thumb_tip) and
            self.is_finger_open(self.index_tip) and
            self.is_finger_open(self.middle_tip) and
            self.is_finger_open(self.ring_tip) and
            self.is_finger_open(self.pinky_tip)
        )

    def is_hand_closed(self):
        """Determine if the hand is closed by checking all fingers."""
        return (
            self.is_finger_closed(self.thumb_tip) and
            self.is_finger_closed(self.index_tip) and
            self.is_finger_closed(self.middle_tip) and
            self.is_finger_closed(self.ring_tip) and
            self.is_finger_closed(self.pinky_tip)
        )

    def is_one(self):
        """Determine if the gesture is 'one' (index finger up)."""
        return (
            self.is_finger_closed(self.thumb_tip) and
            self.is_finger_open(self.index_tip) and
            self.is_finger_closed(self.middle_tip) and
            self.is_finger_closed(self.ring_tip) and
            self.is_finger_closed(self.pinky_tip)
        )

    def is_two(self):
        """Determine if the gesture is 'two' (index and middle fingers up)."""
        return (
            self.is_finger_closed(self.thumb_tip) and
            self.is_finger_open(self.index_tip) and
            self.is_finger_open(self.middle_tip) and
            self.is_finger_closed(self.ring_tip) and
            self.is_finger_closed(self.pinky_tip)
        )

    def is_three(self):
        """Determine if the gesture is 'three' (thumb, index, and middle fingers up)."""
        return (
            self.is_finger_open(self.thumb_tip) and
            self.is_finger_open(self.index_tip) and
            self.is_finger_open(self.middle_tip) and
            self.is_finger_closed(self.ring_tip) and
            self.is_finger_closed(self.pinky_tip)
        )
