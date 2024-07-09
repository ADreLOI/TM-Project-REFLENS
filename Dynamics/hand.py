import math


class Hand:
    MAX_THRESHOLD = 0  # Example threshold, adjust as needed
    MIN_THRESHOLD = 0  # Example threshold, adjust as needed

    def __init__(self, landmarks):
        self.landmarks = landmarks
        self.init_hand()
        self.update_th()

    def init_hand(self):
        self.palm = self.landmarks.landmark[0]
        self.thumb_ip = self.landmarks.landmark[3]
        self.thumb_tip = self.landmarks.landmark[4]
        self.index_base = self.landmarks.landmark[5]
        self.index_p = self.landmarks.landmark[6]
        self.index_ip = self.landmarks.landmark[7]
        self.index_tip = self.landmarks.landmark[8]
        self.middle_base = self.landmarks.landmark[9]
        self.middle_p = self.landmarks.landmark[10]
        self.middle_ip = self.landmarks.landmark[11]
        self.middle_tip = self.landmarks.landmark[12]
        self.ring_base = self.landmarks.landmark[13]
        self.ring_p = self.landmarks.landmark[14]
        self.ring_ip = self.landmarks.landmark[15]
        self.ring_tip = self.landmarks.landmark[16]
        self.pinky_base = self.landmarks.landmark[17]
        self.pinky_p = self.landmarks.landmark[18]
        self.pinky_ip = self.landmarks.landmark[19]
        self.pinky_tip = self.landmarks.landmark[20]

    def update_th(self):
        self.MAX_THRESHOLD = self.distance(self.palm, self.thumb_tip) * 2
        self.MIN_THRESHOLD = self.distance(self.palm, self.thumb_tip) * 1.1

    def distance(self, point1, point2):
        """Calculate the Euclidean distance between two landmarks."""
        distance = math.sqrt(
            (point1.x - point2.x) ** 2 +
            (point1.y - point2.y) ** 2
        )
        return distance

    def distance_th(self, point1, point2, threshold):
        """Calculate the Euclidean distance between palm coordinated and pam coordinates with threshold."""
        return math.sqrt(
            (point1.x - (point2.x + threshold)) ** 2 +
            (point1.y - (point2.y + threshold)) ** 2
        )

    def is_finger_open(self, finger_tip, finger_ip, finger_base):
        """Determine if a finger is open based on the distance from the palm."""
        tip_to_palm = self.distance(finger_tip, self.palm)
        ip_to_palm = self.distance(finger_ip, self.palm)
        base_to_palm = self.distance(finger_base, self.palm)
        return (
                tip_to_palm > ip_to_palm > base_to_palm
        )

    def is_finger_closed(self, finger_tip, finger_p):
        """Determine if a finger is closed based on the distance from the palm."""
        tip_to_palm = self.distance(finger_tip, self.palm)
        p_to_palm = self.distance(finger_p, self.palm)
        return (
                tip_to_palm < p_to_palm and
                (tip_to_palm < self.MIN_THRESHOLD)
        )

    @property
    def is_thumb_in_position(self):
        """Determine if a finger is closed based on the distance from the palm."""
        if self.thumb_tip.x > self.pinky_tip.x:
            thumb_inside = self.thumb_tip.x < self.index_tip.x
        else:
            thumb_inside = self.thumb_tip.x > self.index_tip.x
        return (
                thumb_inside
        )

    @property
    def is_hand_opened(self):
        """Determine if the hand is opened by checking all fingers."""
        return (
                not self.is_thumb_in_position and
                self.is_finger_open(self.thumb_tip, self.thumb_ip, self.palm) and
                self.is_finger_open(self.index_tip, self.index_ip, self.index_base) and
                self.is_finger_open(self.middle_tip, self.middle_ip, self.middle_base) and
                self.is_finger_open(self.ring_tip, self.ring_ip, self.ring_base) and
                self.is_finger_open(self.pinky_tip, self.pinky_ip, self.pinky_base)
        )

    @property
    def is_hand_closed(self):
        """Determine if the hand is closed by checking all fingers."""
        return (
                self.is_thumb_in_position and
                self.is_finger_closed(self.thumb_tip, self.middle_p) and
                self.is_finger_closed(self.index_tip, self.index_p) and
                self.is_finger_closed(self.middle_tip, self.middle_p) and
                self.is_finger_closed(self.ring_tip, self.ring_p) and
                self.is_finger_closed(self.pinky_tip, self.pinky_p)
        )

    @property
    def is_one(self):
        """Determine if the gesture is 'one' (index finger up)."""
        return (
                self.is_thumb_in_position and
                self.is_finger_closed(self.thumb_tip, self.middle_p) and
                self.is_finger_open(self.index_tip, self.index_ip, self.index_base) and
                self.is_finger_closed(self.middle_tip, self.middle_p) and
                self.is_finger_closed(self.ring_tip, self.ring_p) and
                self.is_finger_closed(self.pinky_tip, self.pinky_p)
        )

    @property
    def is_two(self):
        """Determine if the gesture is 'two' (index and middle fingers up)."""
        return (
                self.is_thumb_in_position and
                self.is_finger_closed(self.thumb_tip, self.middle_p) and
                self.is_finger_open(self.index_tip, self.index_ip, self.index_base) and
                self.is_finger_open(self.middle_tip, self.middle_ip, self.middle_base) and
                self.is_finger_closed(self.ring_tip, self.ring_p) and
                self.is_finger_closed(self.pinky_tip, self.pinky_p)
        )

    @property
    def is_three(self):
        """Determine if the gesture is 'three' (thumb, index, and middle fingers up)."""
        return (
                not self.is_thumb_in_position and
                self.is_finger_open(self.thumb_tip, self.thumb_ip, self.palm) and
                self.is_finger_open(self.index_tip, self.index_ip, self.index_base) and
                self.is_finger_open(self.middle_tip, self.middle_ip, self.middle_base) and
                self.is_finger_closed(self.ring_tip, self.ring_p) and
                self.is_finger_closed(self.pinky_tip, self.pinky_p)
        )

    @property
    def sui(self):
        """Determine if the gesture is 'three' (thumb, index, and middle fingers up)."""
        return (
                self.is_thumb_in_position and
                self.is_finger_closed(self.thumb_tip, self.middle_p) and
                self.is_finger_closed(self.index_tip, self.index_p) and
                self.is_finger_open(self.middle_tip, self.middle_ip, self.middle_base) and
                self.is_finger_closed(self.ring_tip, self.ring_p) and
                self.is_finger_closed(self.pinky_tip, self.pinky_p)
        )
