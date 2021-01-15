def calc(finger_joins, hand_bounding_rect):
    # Error
    if finger_joins < 0:
      return -1

    hand_height = hand_bounding_rect[3]
    hand_width = hand_bounding_rect[2]
    h_w_relation = hand_height / hand_width
    # print(h_w_relation)

    if finger_joins >= 1 and h_w_relation > 1.0:
      return finger_joins + 1
    
    # Closed hand
    if finger_joins == 0 and 0.8 <= h_w_relation  <= 1.15: 
        return 0
    # One finger up (vertical)
    if finger_joins == 0 and 1.6 <= h_w_relation <= 2.4:
        return 1

    # Horizontal thumb up
    if 0.5 <= h_w_relation < 0.8:
        return 1
    

    return 0