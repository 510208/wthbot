num = 1
use_num = None

 if (message.channel.id == 1159807731767705691):
        global num , use_num
        if use_num == None:
             use_num = message.author.id
             if validate_input(message.content):
              result = eval(message.content)
              if result == num:
                await message.add_reaction('<a:o_k:1190587362481274891>')
                num = num + 1
                return
              else:
                await message.add_reaction('<a:x_:1190587365572485132>')
                num = 1
                await message.reply(f'# <@{message.author.id}>錯了啦 原因:**數不對** 爛欸，下個數字為 {num}')
                return
             else:
               return
        if message.author.id != use_num:
          if validate_input(message.content):
            result = eval(message.content)
            if result == num:
                await message.add_reaction('<a:o_k:1190587362481274891>')
                num = num + 1
                use_num = message.author.id
                return
            else:
                await message.add_reaction('<a:x_:1190587365572485132>')
                num = 1
                await message.reply(f'# <@{message.author.id}>錯了啦 原因:**數不對** 爛欸，下個數字為 {num}')
                use_num = None
                return
          else:
            return
        else:
            if validate_input(message.content):
             result = eval(message.content)
             await message.add_reaction('<a:x_:1190587365572485132>')
             num = 1
             use_num = None
             await message.reply(f'# <@{message.author.id}>錯了啦 原因:**使用者重複** 爛欸，下個數字為 {num}')
             return
            else:
               return