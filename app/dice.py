import random
import json
import logging

tarot_cards = json.load(open('app/tarot.json'))


def tarot():
    card = random.choice(tarot_cards)
    logging.info('%s: %s', card['nameCN'], card['url'])
    return card


def nca():
    n = random.randint(1, 10)  # 1 <= N <= 10
    desc_str_map = {
        1: '大失敗\n命中包含自己的友方，由被攻擊方選擇被命中的部位。',
        2: '失敗\n未命中',
        3: '失敗\n未命中',
        4: '失敗\n未命中',
        5: '失敗\n未命中',
        6: '成功\n由被攻擊方選擇被命中的部位。',
        7: '成功\n命中腳部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
        8: '成功\n命中胴部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
        9: '成功\n命中腕部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
        10: '成功\n命中頭部。\n如果該部位全部件損壞，由攻擊者選擇其他任意部位。',
    }
    return f'死靈年代記之永遠的後日談：[{n}]  → {desc_str_map[n]}'


def choice(matched_msg):
    options_str = matched_msg.split('[')[1][:-1]
    options = options_str.split(',')
    result = f'自訂選項：[{",".join(options)}] → {random.choice(options)}'
    return result


def fortune():
    dice = random.randint(1, 1000)  # 1 <= N <= 1000
    ans = [
        '大吉だよ！\nやったね⭐︎',
        '大吉……騙你的，差一點呢！\n只是吉而已呦(`・ω・´)',
        '吉。🎉\n很棒呢！',
        '中吉。\n還不錯吧。(ゝ∀･)',
        '小吉。\n就是小吉，平淡過日子，願世界和平。☮',
        '半吉。\n㊗️pyon醬祝福你！(^y^)',
        '末吉。\n嗯～勉勉強強吧！(,,・ω・,,)。',
        '末小吉。\n至少不壞呢！(*´∀`)',
        '凶。\nσ ﾟ∀ ﾟ) ﾟ∀ﾟ)σ至少還有很多更糟的！',
        '小凶。\n(́◉◞౪◟◉‵)運氣不是很好呢，怎麼辦？',
        '半凶。\n有點糟糕～(◔౪◔)',
        '末凶。\nすばらしく運がないな、君は。😊',
        '大凶……⁉️\n欸這機率是千分之一喔？\n比大吉的百分之二還慘喔！？\n沒問題嗎？(((ﾟДﾟ;)))'
    ]
    if dice <= 20:
        return ans[0]
    elif dice <= 90:
        return ans[1]
    elif dice <= 160:
        return ans[2]
    elif dice <= 250:
        return ans[3]
    elif dice <= 363:
        return ans[4]
    elif dice <= 444:
        return ans[5]
    elif dice <= 525:
        return ans[6]
    elif dice <= 600:
        return ans[7]
    elif dice <= 720:
        return ans[8]
    elif dice <= 825:
        return ans[9]
    elif dice <= 929:
        return ans[10]
    elif dice <= 999:
        return ans[11]
    elif dice <= 1000:
        return ans[12]
    else:
        raise ValueError
