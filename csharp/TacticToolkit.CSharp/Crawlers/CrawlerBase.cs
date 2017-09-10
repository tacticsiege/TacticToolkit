using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using log4net;
using TacticToolkit.CSharp.Data;

namespace TacticToolkit.CSharp.Crawlers
{
    public abstract class CrawlerBase<T> : ICrawler<T>
    {
        protected ILog Log { get; set; }

        private TimeSpan DupeScanRange { get; } = TimeSpan.FromDays(5);

        protected IDataRepository<T> DataRepository { get; }
        protected IDataUtility<T> Utility { get; }

        protected string Name { get; }
        protected string NamePlural { get; }

        protected CrawlerBase(ICrawlerFactory<T> factory, string name)
            : this(factory, name, string.Empty)
        {
        }

        protected CrawlerBase(ICrawlerFactory<T> factory, string name, string namePlural)
        {
            DataRepository = factory.CreateRepository();
            Utility = factory.CreateUtility();

            Name = name;
            NamePlural = string.IsNullOrWhiteSpace(namePlural) ? $"{Name}s" : namePlural;
        }

        public IEnumerable<T> Run()
        {
            var sw = Stopwatch.StartNew();
            var savedMessage = $"did not save any {NamePlural}";
            var items = new List<T>();
            try
            {
                items.AddRange(Crawl());

                var numSaved = DataRepository.Save(items);
                savedMessage =
                    (numSaved >= 0)
                        ? "completed successfully"
                        : $"returned error code {numSaved}";

                // Filtering for duplicates is failing at times...
                // Using .Where(x => x.Text == "Example") doesn't always
                // match.  A few attempts to fix, this reactive measure
                // is cheap enough for now...
                Utility.Dedupe(DateTime.UtcNow.Subtract(DupeScanRange));
            }
            catch (Exception e)
            {
                Log.Error($"Exception thrown crawling {NamePlural}. Details below.");
                Log.Error(e);
            }

            sw.Stop();
            Log.Info($"{Name} Crawler {savedMessage}. Total runtime: {sw.Elapsed:hh:mm:ss}.");

            return items;
        }

        public abstract IEnumerable<T> Crawl();
    }
}
