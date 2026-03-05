import json
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from typing import Literal 
def create_message_from_template(template_path: str, mode: Literal['gen_img_ocr', 'reply_ocr', 'gen_ocr'], character_set, ocr_result, image_description = None, danmu_text = None):
    def _raise(msg: str):
        raise ValueError(msg)
    
    env = Environment(
        loader=FileSystemLoader("."),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals["raise"] = _raise

    rendered = env.get_template(template_path).render(
        mode=mode,
        character_set=character_set,
        ocr_result=ocr_result,
        image_description=image_description,
        danmu_text=danmu_text,
    )

    messages = json.loads(rendered)

    return messages
def clean_response(response, character_set, reply = None):

    # prompt = '"请从用户屏幕的OCR结果中总结关键信息，并以给定角色设定的口吻，为每个角色输出一条简短的网络用语风格弹幕。\n角色设定:\n姓名: 宇智波鼬 出自作品: 火影忍者 状态: 晓组织执行任务状态（冷酷疏离）\n姓名: 花子君 出自作品: 地缚少年花子君 状态: 日常恶作剧（校园七大不可思议）\n姓名: 我妻由乃 出自作品: 未来日记 状态: 日常守护雪辉状态（温柔乖巧）\n姓名: 三笠·阿克曼 出自作品: 进击的巨人 状态: 日常守护艾伦状态（温柔警惕）\n姓名: 利姆鲁·特恩佩斯特 出自作品: 关于我转生变成史莱姆这档事 状态: 刚转生为史莱姆（初期）\nOCR结果:\n标题: 【说书人】吐血讲解《后光杀人事件》｜炫学流你就使劲秀吧\n内容: 画家也没法再装了啊\n'
    res = response
    res = res.replace('<', '')
    res = res.replace('>', '')
    id_danmu_list = res.split('\n')

    
    char_text = character_set.strip().split('\n')

    char_list = []

    for char in char_text:
        if char.strip() != '' and char[0:4] == "姓名: ":
            char_list.append(char.split('姓名: ')[1].split(' ')[0])

    res_char_list = []
    res_danmu_list = []
    for id_danmu in id_danmu_list:

        if len(id_danmu.split('：')) != 2:
            continue
        else:
            if reply is not None:
                res_char = id_danmu.split('@')[0].strip()
            else:
                res_char = id_danmu.split('：')[0].strip()
            for char in char_list:
                if res_char in char:
                    res = res.replace(res_char, char)
                    res_char = char
                    break
            
            if res_char not in char_list:
                continue
            res_char_list.append(res_char)
            if reply is not None:
                res_danmu_list.append(id_danmu.split('@')[1].strip())
            else:
                res_danmu_list.append(id_danmu.split('：')[1].strip())
            
    res_new = ''
    for i in range(len(res_char_list)):
        if reply is not None:
            res_new += res_char_list[i] + '@' + res_danmu_list[i] + '\n'
            res_danmu_list[i] = res_danmu_list[i].split('：')[1]
        else:
            res_new += res_char_list[i] + '：' + res_danmu_list[i] + '\n'
    return res_new, res_char_list, res_danmu_list

if __name__ == '__main__':
    # 1.1 角色模板 包含角色名、作品信息和角色状态，不同角色之间用\n分割，最后一个角色后面也要附带\n
    # 每条角色信息应按照以下格式填写 : 为英文冒号，冒号后面跟着一个空格
    # 姓名: xxx 出自作品: xxx 状态: xxx\n  最后一行不带\n
    character_set = """姓名: 灶门祢豆子 出自作品: 鬼灭之刃 状态: 与炭治郎独处（温柔柔软状态）
姓名: 久保渚咲 出自作品: 久保同学不放过我 状态: 与久保明正面互动（羞涩局促状态）
姓名: 樱之宫莓香 出自作品: 调教咖啡厅 状态: 被客人误解（真的吓到人）
姓名: 夏目贵志 出自作品: 夏目友人帐 状态: 与猫咪老师相处（轻松惬意状态）"""
    # 1.2 OCR结果模板 最后一行不带\n
    ocr_result = """这里填什么信息都可以，基本没有格式限制和内容限制。\n但注意不要太长，也不要出现很多冗余的无用信息，内容尽量精简。"""

    # 1.3 图像描述模板 最后一行不带\n
    image_description = """这里填一整段完整的图片描述。中间尽量不要用回车分割。(有应该也没什么影响)"""

    # 1.4 弹幕文本模板
    # 每条弹幕应按以下格式填写
    # 角色名：弹幕内容\n 其中：是中文冒号 最后一行不带\n
    danmu_text = """申鹤：剑心澄澈
神里绫华：此游戏虽真实，望玩家珍视生命之重
八重神子：法医之戏？不如清酒配轻小说呢～
刻晴：攻略当简明高效，避免冗余恐怖"""

    
    template_path = 'template/prompt_template.jinja'
    
    mode = 'gen_img_ocr'
    message = create_message_from_template(template_path, mode, character_set, ocr_result, image_description = image_description)
    print(message[1]["content"])
    print('-'*100)

    mode = 'gen_ocr'
    message = create_message_from_template(template_path, mode, character_set, ocr_result, image_description = image_description)
    print(message[1]["content"])
    print('-'*100)

    mode = 'reply_ocr'
    message = create_message_from_template(template_path, mode, character_set, ocr_result, danmu_text = danmu_text)
    print(message[1]["content"])
    print('-'*100)