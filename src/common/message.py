raw = """
<!DOCTYPE html>
<html>
<body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
<div style="width: 50%; background: #efefef; border-radius: 10px; padding: 10px;">
    <div style="margin: 0 auto; width: 90%; text-align: center;">
        <div style="margin: 30px auto; background: white; width: 90%; border-radius: 10px; padding: 50px; text-align: center;">
        <h2 style="background-color: rgba(0, 53, 102, 1); padding: 10px 10px; border-radius: 5px; color: white;">
        Подтвердите Ваш электронный адрес</h1>
        <h3 style="margin-bottom: 100px; font-size: 24px;">Здравствуйте <b style="text-transform: uppercase;">
        {{ messages.name }}</b>!</h3>
            <h3 style="margin-bottom: 20px; font-size: 24px;">Проверочный код:</h3>
            <h1 style="margin-bottom: 20px">{{ messages.code }}</h1>
            <p style="margin-bottom: 10px;">
            Пожалуйста, никому не пересылайте это сообщение, иначе безопасность Вашего аккаунта окажется под угрозой.
             </p>
             <p>Пользуйтесь с удовольствием! С уважение команда ManasUv</p>
        </div>
    </div>
</div>
</body>
</html>
"""

raw_response = """
    <!DOCTYPE html>
<html>
<body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
<div style="width: 50%; background: #efefef; border-radius: 10px; padding: 10px;">
    <div style="margin: 0 auto; width: 90%; text-align: center;">
        <div style="margin: 30px auto; background: white; width: 90%; border-radius: 10px; padding: 50px; text-align: center;">
        <h2 style="background-color: rgba(0, 53, 102, 1); padding: 10px 10px; border-radius: 5px; color: white;">
        Запрос на прием</h1>
        <h3 style="margin-bottom: 100px; font-size: 24px;">Здравствуйте <b style="text-transform: uppercase;">
        {{ messages.name }}</b>!</h3>
            <h3 style="margin-bottom: 20px; font-size: 24px;">Ваш запрос на прием был принят</h3><br>
            <h3 style="margin-bottom: 20px; font-size: 24px;">Ждем Вас в - {{  messages.time  }}</h3>
            <p style="margin-bottom: 10px;">
            Пожалуйста, никому не пересылайте это сообщение, иначе безопасность Вашего аккаунта окажется под угрозой.
             </p>
             <p>Пользуйтесь с удовольствием! С уважение команда ManasUv</p>
        </div>
    </div>
</div>
</body>
</html>
"""
