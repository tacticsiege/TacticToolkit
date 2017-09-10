using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TacticToolkit.CSharp.Data;

namespace TacticToolkit.CSharp.Crawlers
{
    public interface ICrawlerFactory<T>
    {
        IDataUtility<T> CreateUtility();
        IDataRepository<T> CreateRepository();
    }

    public abstract class CrawlerFactory<T> : ICrawlerFactory<T>
    {
        protected Func<DbContext> GetContextFunc { get; private set; }

        protected CrawlerFactory(Func<DbContext> contextFunction)
        {
            GetContextFunc = contextFunction;
        }
        public abstract IDataUtility<T> CreateUtility();
        public abstract IDataRepository<T> CreateRepository();
    }
}
