using System.Collections.Generic;
using System.Text;
using log4net;
using TacticToolkit.CSharp.Extensions;

namespace TacticToolkit.CSharp.Text
{
    public static class TextReplacements
    {
        private static readonly ILog Log = LogManager.GetLogger(typeof(TextReplacements));

        #region Replacement Dictionary
        // lots of ansi replacements: http://www.alanwood.net/demos/ansi.html
        // not all are included here based on experience.
        private static readonly Dictionary<string, string> Replacements =
            new Dictionary<string, string>
            {
                {"&apos;", "'"},
                {"&amp;", "and"},
                {"<i>", string.Empty},
                {"</i>", string.Empty},
                {">", "-"},
                {"|", "-"},
                {"–", "-"},
                {"—", "-"},
                {"£", "LON$"},
                {"¡", "^!"},
                {"¢", "^cent"},
                {"…", "..."},
                {"--", "-"},
                {"¬", "^NOT"},
                {"¯", "-" },
                {"‘", "'"},
                {"’", "'"},
                {"´", "'"},
                {"·", "-"},
                {"•", "-"},
                {"²", "^2"},
                {"³", "^3"},
                {"“", "\""},
                {"”", "\""},
                {"‚", ","},
                {"€", "EUR$"},
                {"¥", "^yen"},
                {"ç", "c"},
                {"À", "A"},
                {"Á", "A"},
                {"Â", "A"},
                {"Ã", "A"},
                {"Ä", "A"},
                {"Å", "A"},
                {"Æ", "AE"},
                {"Ñ", "N"},
                {"à", "a"},
                {"â", "a"},
                {"á", "a"},
                {"ã", "a"},
                {"ä", "a"},
                {"å", "a"},
                {"é", "e"},
                {"è", "e"},
                {"ë", "e"},
                {"ê", "e"},
                {"ñ", "n"},
                {"™", "^TM"},
                {"œ", "ae"},
                {"©", "^copyright"},
                {"®", "^registered"},
                {"°", "^deg"},
                {"Ì", "I"},
                {"Í", "I"},
                {"Î", "I"},
                {"Ï", "I"},
                {"ì", "i"},
                {"í", "i"},
                {"î", "i"},
                {"ï", "i"},
                {"ö", "o"},
                {"ó", "o"},
                {"ô", "o"},
                {"õ", "o"},
                {"ò", "o"},
                {"ø", "o"},
                {"ú", "u"},
                {"ù", "u"},
                {"û", "u"},
                {"ü", "u"},
                {"ý", "y"},
                {"ÿ", "y"},
                {"½", "^half"},
                {"¼", "^quarter"},
                {"¾", "^(3/4)"},
                {"¿", "^?"},
                {"É", "E"},
                {"Ö", "O"},
                {"˜", "~"},
                {"×", "x"},
                {((char)160).ToString(), " "}
            };
        #endregion

        public static string RemoveControlCharacters(string headline)
        {
            var sb = new StringBuilder();
            for (var i = 0; i < headline.Length; i++)
            {
                var ch = headline[i];

                if (!char.IsControl(ch))
                    sb.Append(ch);
                else
                    Log.Warn($"Encountered Control Character: ({ch}).");
            }
            return sb.ToString();
        }

        public static string Apply(string text)
        {
            return text.Replace(Replacements);
        }


    }
}
