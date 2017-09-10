using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using log4net;

namespace TacticToolkit.CSharp.Data
{
    public abstract class DataUtilityBase<T> : IDataUtility<T>
    {
        protected ILog Log { get; set; }

        private Func<DbContext> GetContext { get; set; }

        protected DataUtilityBase(Func<DbContext> contextFunction)
        {
            GetContext = contextFunction;
        }

        public int DupeCount()
        {
            using (var db = GetContext())
            {
                try
                {
                    var count = GetDupeCount(db);
                    return count.GetValueOrDefault(-1);
                }
                catch (ArgumentNullException argEx)
                {
                    Log.Error(argEx);
                    throw;
                }
                catch (InvalidOperationException opEx)
                {
                    Log.Error(opEx);
                    throw;
                }
                catch (Exception e)
                {
                    Log.Error(e);
                    throw;
                }
            }
        }

        public int Dedupe()
        {
            return Dedupe(DateTime.MinValue, DateTime.MaxValue);
        }

        public int Dedupe(DateTime since)
        {
            return Dedupe(since, DateTime.MaxValue);
        }

        public int Dedupe(DateTime since, DateTime until)
        {
            var expectedDupeCount = DupeCount();
            if (expectedDupeCount <= 0)
            {
                Log.Debug("No dupes were found.");
                return expectedDupeCount;
            }

            var dupeCount = 0;
            var sw = Stopwatch.StartNew();
            using (var db = GetContext())
            {
                db.Database.CommandTimeout = 1200;
                var dupes = GetDuplicates(since, until, db).ToList();
                Log.Debug($"Grouped Dupes in {sw.Elapsed.TotalSeconds}s. Found {dupes.Count()} duplicates.");

                sw.Restart();
                try
                {
                    var removed = RemoveDuplicates(dupes, db);

                    var saved = db.SaveChanges();
                    dupeCount = removed + saved;
                }
                catch (Exception e)
                {
                    Log.Error("Exception thrown trying to remove duplicates.");
                    Log.Error(e);
                    dupeCount = 0;
                }


                sw.Stop();
                if (dupeCount > 0)
                    Log.Debug($"Removed {dupeCount} duplicates in {sw.Elapsed.TotalSeconds}s.");

                var remainingDupeCount = DupeCount();
                if (remainingDupeCount <= 0) { return dupeCount; }

                Log.Debug($"At least {remainingDupeCount} duplicates still remain, deleting them...");
                var deleted = DeleteDupes(db);
                Log.Debug($"Deleted {deleted} duplicates.");
            }

            return dupeCount;
        }

        

        public int Scrub()
        {
            return Scrub(DateTime.MinValue);
        }

        public int Scrub(DateTime since)
        {
            var sw = Stopwatch.StartNew();
            using (var db = GetContext())
            {
                var set = GetItemsToScrub(since, db);
                ScrubItems(set);

                var saved = db.SaveChanges();
                sw.Stop();
                Log.Info($"Formatted {saved} items in {sw.Elapsed.TotalSeconds}s.");
                return saved;
            }
        }


        protected abstract IEnumerable<T> GetDuplicates(DateTime since, DateTime until, DbContext db);
        protected abstract int RemoveDuplicates(IEnumerable<T> dupes, DbContext db);
        protected abstract int? GetDupeCount(DbContext db);
        protected abstract int DeleteDupes(DbContext db);
        protected abstract void ScrubItems(IEnumerable<T> items);
        protected abstract IEnumerable<T> GetItemsToScrub(DateTime since, DbContext db);
    }
}
