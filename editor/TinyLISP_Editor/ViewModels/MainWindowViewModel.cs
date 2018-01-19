using CommonLib.Models;
using CommonLib.ViewModels;
using Prism.Commands;
using Prism.Mvvm;
using Reactive.Bindings;
using Reactive.Bindings.Extensions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using TinyLISP_Editor.Models;

namespace TinyLISP_Editor.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        MainWindowModel model;
        public MainWindowViewModel(Window view, MainWindowModel model) : base(view, model)
        {
            LispSourceText = model.ToReactivePropertyAsSynchronized(m => m.LispSourceText);
            LispOutText = model.ToReactivePropertyAsSynchronized(m => m.OutText);

            TinyLispRunClicked = new DelegateCommand(TinyLispRun_Clicked);

            this.model = model;
            model.Load();
        }

        #region EventProperties
        public ICommand TinyLispRunClicked { get; }
        #endregion

        #region Properties
        public ReactiveProperty<string> LispSourceText { get; set; }
        public ReactiveProperty<string> LispOutText { get; set; }
        #endregion

        #region EventMethods

        public void TinyLispRun_Clicked()
        {
            model.Run();
        }
        #endregion
    }
}
