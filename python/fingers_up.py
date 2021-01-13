def calc(finger_joins, hand_bounding_rect):
    # Error
    if finger_joins < 0:
      return -1

    if finger_joins >= 1:
      return finger_joins + 1

    hand_height = hand_bounding_rect[3]
    hand_width = hand_bounding_rect[2]
    h_w_relation = hand_height / hand_width
    w_h_relation = hand_width / hand_height
    print(w_h_relation)
    
    # Closed hand
    if 1.15 <= h_w_relation  <= 1.25: 
        return 0
    # One finger up
    if 1.7 <= h_w_relation <= 2.3:
        return 1

    # Horizontal thumb up
    if 0.7 <= w_h_relation <= 1.1:
        return 1
    

    return 0