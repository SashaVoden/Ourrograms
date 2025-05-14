$tabsToRestore = Get-Random -Minimum 1 -Maximum 3

for ($i = 0; $i -lt $tabsToRestore; $i++) {
    Add-Type -TypeDefinition @"
    using System;
    using System.Runtime.InteropServices;
    public class Keyboard {
        [DllImport("user32.dll")]
        public static extern void keybd_event(byte bVk, byte bScan, int dwFlags, int dwExtraInfo);
    }
"@ -Language CSharp

    # Симуляция Ctrl+Shift+T
    [Keyboard]::keybd_event(0x11, 0, 0, 0) # Ctrl
    [Keyboard]::keybd_event(0xA0, 0, 0, 0) # Shift
    [Keyboard]::keybd_event(0x54, 0, 0, 0) # T
    Start-Sleep -Milliseconds 50
    [Keyboard]::keybd_event(0x54, 0, 2, 0) # Release T
    [Keyboard]::keybd_event(0xA0, 0, 2, 0) # Release Shift
    [Keyboard]::keybd_event(0x11, 0, 2, 0) # Release Ctrl
    Start-Sleep -Seconds 1
}

Write-Host "Закрытые вкладки восстановлены!" -ForegroundColor Green
