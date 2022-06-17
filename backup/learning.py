def rpy_message(message):
    
    #「こんにちは」と来た場合の返事
    if message == "こんにちは":
        reply_message = "こんにちは。\nいい天気ですね。"
    
    #「好きな食べ物は？」と来た場合の返事
    elif message == "好きな食べ物は？":
        reply_message = "餃子、ハンバーグ、オムライス等々"
    
    #「はまち」と来た場合の返事
    elif message == "はまち":
        reply_message = "三種の神器の一つ。\nちゃいろの毛玉。\nもふもふかわいい...。"

    #「最近ハマっていることは？」と来た場合の返事
    elif message == "最近ハマっていることは？":
        reply_message = "モンハンにハマってます！"

    #それ以外の返事
    else:
        reply_message = f"あなたは「{message}」と言いました！"
    
    return reply_message
