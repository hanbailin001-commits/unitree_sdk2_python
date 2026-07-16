import os
import asyncio
import edge_tts

# 这是为您专门加了标点断句的高燃喊麦词，方便机器狗换气和停顿
text = """
二哥，二哥，欢迎你！感谢你，来我这里！
二哥，二哥，欢迎你！等风，等雨，等着你！

他来了，他来了！他带着礼物，走来了！
他来了，他来了！他脚踏祥云，进来了！

二哥天，二哥地！二哥能顶，天立地！
二哥风，二哥雨！二哥能呼，风唤雨！

这是我的，好二哥！他有房，又有车！
再次欢迎，我二哥！刷点礼物，不用说！

来！感谢二哥！来！感谢二哥六十六！
谢我二哥，在身后！今生有你，已经足够！

二哥二哥，很优秀！感谢二哥的五百二十！
二哥他，还没有停！二哥少刷，行不行？
不行，不行，就不行！

感谢二哥，一生一世！让我们，再来一次！
心中立下，忠义二字！护我二哥，在展翅！

一声朋友，一生情！一生有你，才会赢！
让我护你，度安宁！心中刻下，二哥名！

二哥，二哥，你快过来！
让我来给你，安！排！
"""

# zh-CN-YunxiNeural 是一款非常有气势、语速有爆发力的年轻男声
VOICE = "zh-CN-YunxiNeural"
OUTPUT_FILE = "erge_welcome.wav"

async def generate_audio():
    print("🚀 正在为二哥全自动生成专属喊麦语音包...")
    # 调高语速 (+15%) 和音调 (+10Hz) 来模拟喊麦的激情状态
    communicate = edge_tts.Communicate(text, VOICE, rate="+15%", pitch="+10Hz")
    await communicate.save(OUTPUT_FILE)
    print(f"✅ 搞定！语音已自动保存为 {OUTPUT_FILE}")
    print("👉 现在您可以直接运行迎宾代码，狗子就能连喊带跳了！")

if __name__ == "__main__":
    asyncio.run(generate_audio())
