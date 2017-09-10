using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TacticToolkit.CSharp.Crawlers
{
    public interface ICrawler<out T>
    {
        IEnumerable<T> Crawl();
    }
}
