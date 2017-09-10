using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TacticToolkit.CSharp.Data
{
    public class PagedLoadResult<T>
    {
        public int ResultCount { get; set; }
        public int PageResultCount { get; set; }
        public int Page { get; set; }
        public int PageCount { get; set; }
        public DateTime LastUpdated { get; set; }
        public IEnumerable<T> Items { get; set; }
    }
}
