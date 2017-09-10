using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Data.Entity.Validation;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TacticToolkit.CSharp.Data
{
    public abstract class DataRepositoryBase<T> : RepositoryBase<DbContext>, IDataRepository<T> where T : class
    {
        private const int DefaultPageSize = 100;
        protected abstract string Name { get; }
        protected abstract string NamePlural { get; }
        protected abstract Func<T, DateTime> DateSelector { get; }

        protected DataRepositoryBase(Func<DbContext> contextFunction)
            : base(contextFunction)
        {
        }

        protected abstract DbSet<T> GetItems(DbContext db);

        public int Save(IEnumerable<T> items)
        {
            var numSaved = -1;
            using (var db = GetContext())
            {
                GetItems(db).AddRange(
                    items.Except(GetItems(db)).ToList());
                numSaved = SaveChanges(db);
            }

            return numSaved;
        }

        public IEnumerable<T> LoadAll()
        {
            IEnumerable<T> list;
            using (var db = GetContext())
            {
                list = GetItems(db)
                    .OrderByDescending(DateSelector)
                    .ToList();
            }

            return list;
        }

        //public PagedLoadResult<T> LoadRange(int count, int page, DateTime start, DateTime end)
        //{
        //    var result = new PagedLoadResult<T>();
        //    using (var db = GetContext())
        //    {
        //        result.Items = GetItems(db)
        //            .Where(x => DateSelector(x) > start && DateSelector(x) < end)
        //            .OrderByDescending(DateSelector)
        //            .Skip((page - 1) * count)
        //            .Take(count)
        //            .ToList();

        //        result.ResultCount = GetItems(db)
        //            .Count(x => DateSelector(x) > start && DateSelector(x) < end);
        //        result.LastUpdated = GetItems(db)
        //            .Where(x => DateSelector(x) > start && DateSelector(x) < end)
        //            .Max(DateSelector);
        //    }
        //    return result;
        //}



        public PagedLoadResult<T> Load(int count, int page)
        {
            if (count <= 0)
                count = DefaultPageSize;

            var result = LoadPagedItems(count, page);

            result.PageResultCount = count;
            result.Page = page;
            result.PageCount = result.ResultCount / count;

            return result;
        }

        private PagedLoadResult<T> LoadPagedItems(int count, int page)
        {
            var result = new PagedLoadResult<T>();
            using (var db = GetContext())
            {
                result.Items = GetItems(db)
                    .OrderByDescending(DateSelector)
                    .Skip((page - 1) * count)
                    .Take(count)
                    .ToList();
                result.ResultCount = GetItems(db).Count();
                result.LastUpdated = GetItems(db).Max(DateSelector);
            }
            return result;
        }

        // ReSharper disable once MemberCanBePrivate.Global, Reason: Useful in derived classes
        protected int SaveChanges(DbContext db)
        {
            var numSaved = -1;
            try
            {
                numSaved = db.SaveChanges();
            }
            catch (DbEntityValidationException dbEx)
            {
                LogEntityValidationException(dbEx);
            }
            catch (Exception e)
            {
                Log.Error(e);
                throw;
            }

            LogSaveResult(numSaved);

            return numSaved;
        }

        private void LogEntityValidationException(DbEntityValidationException dbEx)
        {
            Log.Error($"Validation error saving {NamePlural}.");
            foreach (var entityError in dbEx.EntityValidationErrors)
            {
                foreach (var validationError in entityError.ValidationErrors)
                {
                    Log.Error($"Property: {validationError.PropertyName}");
                    Log.Error($"Error: {validationError.ErrorMessage}");
                }
            }
        }

        private void LogSaveResult(int numSaved)
        {
            if (numSaved > 0)
            {
                Log.Info($"Saved {numSaved} {NamePlural}.");
            }
            else if (numSaved == 0)
            {
                Log.Info($"No {NamePlural} were saved.");
            }
            else
            {
                Log.Warn($"There were {numSaved} {NamePlural} saved, this should not be...");
            }
        }
    }
}
