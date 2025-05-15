Add-Type -TypeDefinition @"
using System;
using System.Windows.Forms;
using System.Drawing;

public class FlashingWindow : Form {
    private Timer timer;
    private Random rand = new Random();

    public FlashingWindow() {
        this.FormBorderStyle = FormBorderStyle.None;
        this.WindowState = FormWindowState.Maximized;
        this.TopMost = true;

        timer = new Timer();
        timer.Interval = 100; // Скорость смены цвета (в миллисекундах)
        timer.Tick += (sender, e) => ChangeColor();
        timer.Start();
    }

    private void ChangeColor() {
        this.BackColor = Color.FromArgb(rand.Next(256), rand.Next(256), rand.Next(256));
    }

    [STAThread]
    public static void Main() {
        Application.Run(new FlashingWindow());
    }
}
"@ -Language CSharp

[FlashingWindow]::Main()
