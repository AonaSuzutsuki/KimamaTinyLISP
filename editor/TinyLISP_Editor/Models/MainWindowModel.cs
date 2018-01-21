using CommonLib.Models;
using Prism.Mvvm;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TinyLISP_Editor.Models
{
    public class MainWindowModel : ModelBase
    {
        private string lispSourceText;
        public string LispSourceText
        {
            get => lispSourceText;
            set => SetProperty(ref lispSourceText, value);
        }

        private string outText;
        public string OutText
        {
            get => outText;
            set => SetProperty(ref outText, value);
        }


        Translator translator = new Translator();

        public void Load()
        {
            LispSourceText = "(defun factorial\n" +
                "	(lambda (n)\n" +
                "		(if (= n 0)\n" +
                "			1\n" +
                "			(* n (factorial (- n 1)))\n" +
                "		)\n" +
                "	)\n" +
                ")\n" +
                "(factorial 5)\n";
        }

        public void Run()
        {
            var text = LispSourceText;
            OutText = translator.Send(text);
        }
    }
}
