Add-Type -TypeDefinition @"
using System;
using System.Windows.Forms;
using System.Drawing;

public class HackedWindow : Form {
    private Timer timer;
    private int dx = 5, dy = 5;

    public HackedWindow() {
        this.Text = "HACKED";
        this.Size = new Size(300, 200);
        this.BackColor = Color.Black;
        this.ForeColor = Color.Red;
        this.FormBorderStyle = FormBorderStyle.None;
        this.StartPosition = FormStartPosition.Manual;
        this.Location = new Point(200, 200);
        
        Label hackedLabel = new Label();
        hackedLabel.Text = "HACKED";
        hackedLabel.Font = new Font("Arial", 24, FontStyle.Bold);
        hackedLabel.ForeColor = Color.Red;
        hackedLabel.AutoSize = true;
        this.Controls.Add(hackedLabel);

        timer = new Timer();
        timer.Interval = 50;
        timer.Tick += (sender, e) => MoveWindow();
        timer.Start();
    }

    private void MoveWindow() {
        Screen screen = Screen.PrimaryScreen;
        int maxX = screen.WorkingArea.Width - this.Width;
        int maxY = screen.WorkingArea.Height - this.Height;

        this.Left += dx;
        this.Top += dy;

        if (this.Left <= 0 || this.Left >= maxX) dx = -dx;
        if (this.Top <= 0 || this.Top >= maxY) dy = -dy;
    }

    [STAThread]
    public static void Main() {
        Application.Run(new HackedWindow());
    }
}
"@ -Language CSharp

[HackedWindow]::Main()
