import random


def Rock_Paper_Scissors(user_hand):
    hands = ['グー', 'チョキ', 'パー']
    res_text = 'グー,チョキ,パーを選んでください。'
    check_flg = False

    for check_hand in hands:
        if user_hand == check_hand:
            check_flg = True

    if not check_flg:
        return res_text

    bot_num = random.randint(0, 2)
    hand = hands[bot_num]
    win_flg = False
    draw_flg = False

    if hand == hands[0] and user_hand == hands[2]:
        win_flg = True
    elif hand == hands[1] and user_hand == hands[0]:
        win_flg = True
    elif hand == hands[2] and user_hand == hands[1]:
        win_flg = True
    elif hand == user_hand:
        draw_flg = True

    if win_flg:
        res_text = f"あなたは{user_hand}で私は{hand}でした。\n" \
                   f"よって貴方の勝ちです。"
    elif draw_flg:
        res_text = f"あなたは{user_hand}で私は{hand}でした。\n" \
                   f"あいこです。ぐぬぬ"
    else:
        res_text = f"あなたは{user_hand}で私は{hand}でした。\n" \
                   f"私の勝ちです。"

    return res_text

