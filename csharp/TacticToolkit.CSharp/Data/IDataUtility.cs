using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TacticToolkit.CSharp.Data
{
    public interface IDataUtility<T>
    {
        int DupeCount();
        int Dedupe();
        int Dedupe(DateTime since);
        int Dedupe(DateTime since, DateTime until);
        int Scrub();
        int Scrub(DateTime since);
    }
}
