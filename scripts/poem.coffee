# Description:
#   Allows Hubot to get random poem.
#
# Commands:
#   hubot poem

module.exports = (robot) ->
  robot.respond /poem/i, (msg) ->
    poem = _getRandomPoem()
    msg.send poem

_getRandomPoem = () ->
  templates = ["xx，xx，xx了xx。", "xxxx，xxxx，不过是一场xxxx。", "你说xxxx，我说xxxx，最后不过xxxx。", "xx，xx，许我一场xxxx。", "x一x一xx，半x半x半xx。", "你说xxxx xxxx，后来xxxx xxxx。", "xxxx，xxxx，终不敌xxxx"]
  foreWords = "情深缘浅 情深不寿 莫失莫忘 阴阳相隔 如花美眷 似水流年 眉目如画 曲终人散 繁华落尽 不诉离殇 一世长安".split(" ")
  twoWords = "朱砂 天下 杀伐 人家 韶华 风华 繁华 血染 墨染 白衣 素衣 嫁衣 倾城 孤城 空城 旧城 旧人 伊人 心疼 春风 古琴 无情 迷离 奈何 断弦 焚尽 散乱 陌路 乱世 笑靥 浅笑 明眸 轻叹 烟火 一生 三生 浮生 桃花 梨花 落花 烟花 离殇 情殇 爱殇 剑殇 灼伤 仓皇 匆忙 陌上 清商 焚香 墨香 微凉 断肠 痴狂 凄凉 黄梁 未央 成双 无恙 虚妄 凝霜 洛阳 长安 江南 忘川 千年 纸伞 烟雨 回眸 公子 红尘 红颜 红衣 红豆 红线 青丝 青史 青冢 白发 白首 白骨 黄土 黄泉 碧落 紫陌".split(" ")
  _getEsuSentence templates, foreWords, twoWords

_getEsuSentence = (templates, foreWords, twoWords) ->
  push = ""
  template = _getRandom templates
  while "xxxx" in template
    template = template.replace(/xxxx/, getRandom(foreWords))
  while "xx" in template
    template = template.replace(/xx/, getRandom(twoWords))
  while "x" in template
    if push
      template = template.replace(/x/, push)
      push = ""
    random = _getRandom foreWords
    template = template.replace(/x/, random.substring(0, 1))
    push = random.substring(1)

  return template

_getRandom = (t) ->
  randomIdx = Math.floor(Math.random() * t.length)
  return t[randomIdx]
