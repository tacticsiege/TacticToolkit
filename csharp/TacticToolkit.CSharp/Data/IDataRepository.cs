using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TacticToolkit.CSharp.Data
{
    public interface IDataRepository<T>
    {
        int Save(IEnumerable<T> items);
        IEnumerable<T> LoadAll();
        PagedLoadResult<T> Load(int count, int page);
    }
}
