def calc(finger_joins, hand_bounding_rect):
    # Error
    if finger_joins < 0:
      return -1

    if finger_joins >= 1:
      return finger_joins + 1

    hand_height = hand_bounding_rect[3]
    hand_width = hand_bounding_rect[2]
    h_w_relation = hand_height / hand_width
    print(h_w_relation)
    
    # Closed hand
    if 1.15 <= h_w_relation  <= 1.25: 
        return 0
    # One finger up
    if 1.8 <= h_w_relation <= 2.3:
        return 1
    

    return 0