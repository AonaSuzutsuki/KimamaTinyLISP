using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TinyLISP_Editor.Models
{
    public class Translator
    {
        private string command = @"/c python ..\interpreter\echo.py ""{0}"" | ..\interpreter\parser | python ..\interpreter\run.py -l true -t true";
        private Process p;

        public Translator()
        {
            p = new Process();
        }

        public string Send(string text)
        {
            text = text.Replace("\r", " ").Replace("\n", " ");
            string arg = string.Format(command, text);
            p.StartInfo = new ProcessStartInfo()
            {
                FileName = Environment.GetEnvironmentVariable("ComSpec"),
                UseShellExecute = false,
                RedirectStandardError = true,
                RedirectStandardInput = false,
                RedirectStandardOutput = true,
                CreateNoWindow = true,
                Arguments = arg
            };
            p.Start();
            string results = p.StandardOutput.ReadToEnd();
            string error = p.StandardError.ReadToEnd();
            if (!error.Equals("\r\nparser successfully ended\r\n\r\n"))
                results += error;
            
            p.WaitForExit();
            p.Close();

            return results;
        }
    }
}
