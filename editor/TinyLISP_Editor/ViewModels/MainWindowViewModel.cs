using CommonLib.Models;
using CommonLib.ViewModels;
using Prism.Mvvm;
using Reactive.Bindings;
using Reactive.Bindings.Extensions;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using TinyLISP_Editor.Models;

namespace TinyLISP_Editor.ViewModels
{
    public class MainWindowViewModel : ViewModelBase
    {
        public MainWindowViewModel(Window view, MainWindowModel model) : base(view, model)
        {
            LispSourceText = model.ToReactivePropertyAsSynchronized(m => m.LispSourceText);

            model.Load();
        }

        #region EventProperties

        #endregion

        #region Properties
        public ReactiveProperty<string> LispSourceText { get; set; }
        #endregion

        #region EventMethods

        #endregion
    }
}
