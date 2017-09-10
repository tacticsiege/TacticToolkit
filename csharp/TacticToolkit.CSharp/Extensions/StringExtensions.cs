using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace TacticToolkit.CSharp.Extensions
{
    public static class StringExtensions
    {
        public static string Replace(this string before, IDictionary<string, string> replacements)
        {
            var after = before;
            foreach (var replacement in replacements)
            {
                after = after.Replace(replacement.Key, replacement.Value);
            }
            return after;
        }

        public static bool IsValidUrl(this string a)
        {
            //Regex from: https://mathiasbynens.be/demo/url-regex
            var regex = new Regex(
                "_^(?:(?:https?|ftp)://)(?:\\S+(?::\\S*)?@)?(?:(?!10(?:\\.\\d{1,3}){3})(?!127(?:\\.\\d{1,3}){3})(?!169\\.254(?:\\.\\d{1,3}){2})(?!192\\.168(?:\\.\\d{1,3}){2})(?!172\\.(?:1[6-9]|2\\d|3[0-1])(?:\\.\\d{1,3}){2})(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}(?:\\.(?:[1-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))|(?:(?:[a-z\\x{00a1}-\\x{ffff}0-9]+-?)*[a-z\\x{00a1}-\\x{ffff}0-9]+)(?:\\.(?:[a-z\\x{00a1}-\\x{ffff}0-9]+-?)*[a-z\\x{00a1}-\\x{ffff}0-9]+)*(?:\\.(?:[a-z\\x{00a1}-\\x{ffff}]{2,})))(?::\\d{2,5})?(?:/[^\\s]*)?$_iuS");
            return regex.IsMatch(a);
        }
    }
}
