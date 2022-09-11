from random import seed
from urllib import request
from nonebot import on_command, CommandSession
from urllib.parse import quote

api_base = "http://127.0.0.1:5123"

@on_command('vits', aliases=('vits', '语音合成'))
async def vits(session: CommandSession):
    model_name = session.current_arg_text.strip()
    if not model_name:
        await session.send("欢迎！目前支持的模型有：\n派蒙 (中文) (原作者:VentiJ)\nAtri (日语) (原作者:luoyily)\nLJ Speech (英语) (原作者:Jaehyeon Kim)")
        model_name = (await session.aget(prompt="想使用哪个模型呢？")).strip()
    model_standard_name = get_model_standard_name(model_name)
    while not model_standard_name:
        model_name = (await session.aget(prompt="找不到这个模型呢...请重新输入！")).strip()
        model_standard_name = get_model_standard_name(model_name)
    preload_model(model_standard_name)
    target_text = (await session.aget(prompt="模型加载完成啦！输入你想读出的文本吧！输入\"!退出\"退出语音合成。")).strip()
    while target_text != "!退出" and target_text.lower() != "!exit":
        voice_url = get_voice_url(model_standard_name,target_text)
        await session.send(f"[CQ:record,file={voice_url}]")
        target_text = (await session.aget()).strip()

def preload_model(model_name):
    request.urlopen(f"{api_base}/load?model_name={model_name}")

def get_voice_url(model_name,target_text):
    return f"{api_base}/synthesis?model_name={model_name}&target_text={quote(target_text)}"

def get_model_standard_name(model_name):
    model_list = {"atri":["亚托莉","亚托铃","萝卜子","アトリ","ロボ子","アトリん"],"paimon":["派蒙","应急食品","神奇海鲜"],"ljs":["ljspeech","lj speech"]}
    model_name = model_name.lower()
    if(model_name in model_list):
        return model_name
    else:
        for standard_name,names in model_list.items():
            for name in names:
                if name in model_name:
                    return standard_name
    return None