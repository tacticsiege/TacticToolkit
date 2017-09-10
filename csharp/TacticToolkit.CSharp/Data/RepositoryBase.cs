using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using log4net;

namespace TacticToolkit.CSharp.Data
{
    public class RepositoryBase<T>
    {
        protected ILog Log { get; }
        protected Func<T> GetContext { get; }

        protected RepositoryBase(Func<T> contextFunction)
        {
            GetContext = contextFunction;
            Log = LogManager.GetLogger(GetType());
        }
    }
}
